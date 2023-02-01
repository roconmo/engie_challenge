import logging
import pandas as pd
from constanst.constants import co2_emission_per_MWh, generation_ways, cost_priorities, gas_plant, load_objective, \
    wind_turbine, kerosine_plant
import json
import operator
import numpy as np
import datetime


def load_params():
    logging.basicConfig(filename=r'src\logs\extractor.log', level=logging.DEBUG)


def calculate_wind_resource(average_wind, pMax, efficiency):
    """
    Calculates the production of wind plants
    """
    return int(pMax * (average_wind/100) * efficiency)


#
def calculate_resource_capacity(pMax, efficiency, resource):

    if resource == wind_turbine:
        capacity = int(pMax * (efficiency/100))
    else:
        capacity = pMax * efficiency
    return capacity


# gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50%
# (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
def get_resource_cost(price_MWh, rec_efficiency, resource):
    """
    :param price_MWh:
    :param rec_efficiency:
    :param resource:
    :return: The cost of received resource
    """
    cost_MWh = 0

    # the wind_turbine doesn't have a production cost
    if resource != wind_turbine:
        efficiency = 100 / rec_efficiency
        cost_MWh = efficiency * price_MWh

    return cost_MWh


def get_price_MWh(resource_type, df_fuels):
    """
    This function receives a resource and looks in the dataframe df_fuels the price for this resource
    Args:
        resource_type: the resource we are consulting
        df_fuels: a dataframe with all the fuels information
    :return: price for the selected resource
    """
    if resource_type == gas_plant:
        price_MWh = df_fuels.iloc[0]['gas(euro/MWh)']
    elif resource_type == kerosine_plant:
        price_MWh = df_fuels.iloc[0]['kerosine(euro/MWh)']
    else:
        price_MWh = 0

    return price_MWh


def get_CO2_penalty(resource_type, resource_capacity):
    """
    ASSUMPTION: each MWh generated creates 0.3 ton of CO2.
    :param resource_type:
    :param resource_capacity:
    :return:
    """
    CO2_penalty = 0
    if resource_type == gas_plant:
        CO2_penalty = resource_capacity * co2_emission_per_MWh
    return CO2_penalty


def process_final_JSON(my_json):
    """

    :param my_json:
    :return:
    """

    jsonStr = json.dumps(my_json)

    data = json.loads(jsonStr)
    data.sort(key=operator.itemgetter('cost', 'efficiency', 'CO2_penalty'))

    logging.info(f'final json creation started: {datetime.datetime.now()}')
    sum_p = 0
    for i in data:
        for key, values in i.items():
            if key == 'p':
                if i.get('p') + sum_p > load_objective:
                    i['p'] = float(np.round(load_objective - sum_p, 5))
                    sum_p += load_objective - sum_p
                else:
                    if load_objective - sum_p > 0:
                        sum_p += (i.get('p'))
                    else:
                        i['p'] = int(0)

    for item in data:
        item.pop('cost')
        item.pop('efficiency')
        item.pop('CO2_penalty')
        item.pop('pmin')

    return data


def process_json(data):
    """
    This function receives a JSON and processes to get the resources needed to generate the load required. To do so,
    there is a dictionary called cost_priorities (in constants directory) to prioritize the resources by 'cost'
    'efficiency' and 'CO2_penalty'

    :return: the required json with the names of the resources and the amount of energy they should provide in key p.
    """
    logging.info(f'the API has been initialized: {datetime.datetime.now()}')
    df_plants = pd.DataFrame(data['powerplants'])
    fuels = data['fuels']
    fuels_dict = {k: [v] for k, v in fuels.items()}
    df_fuels = pd.DataFrame(fuels_dict)

    wind_percent = df_fuels.iloc[0]['wind(%)']
    results = []
    for key, value in cost_priorities.items():
        my_df = df_plants[df_plants['type'] == generation_ways[value]]
        for index, row in my_df.iterrows():
            pmax = row['pmax']
            resource_type = row['type']
            efficiency = wind_percent if resource_type == wind_turbine else row['efficiency']
            price_MWh = get_price_MWh(resource_type, df_fuels)
            resource_capacity = calculate_resource_capacity(pmax, efficiency, resource_type)

            results.append({
                "name": row['name'],
                "p": resource_capacity,
                'cost': get_resource_cost(price_MWh, efficiency, resource_type),
                'efficiency': efficiency,
                'CO2_penalty': get_CO2_penalty(resource_type, resource_capacity),
                "pmin": row['pmin']
            })
    logging.info(f'An intermediate JSON with name, p, cost, efficiency, cO2_penalty and pmin for each resource, '
                 f'has been created: {datetime.datetime.now()}')
    return process_final_JSON(results)


