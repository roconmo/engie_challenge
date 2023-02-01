# CONSTANTS
# those with the lowest marginal costs are the first ones to be brought online to meet demand, and the plants with
# the highest marginal costs are the last to be brought on line
cost_priorities = {
    1: 'wind(%)',
    2: 'gas(euro/MWh)',
    3: 'kerosine(euro/MWh)'
}

generation_ways = {
    'gas(euro/MWh)': 'gasfired',
    'kerosine(euro/MWh)': 'turbojet',
    'wind(%)': 'windturbine'
}

co2_emission_per_MWh = 0.3
gas_plant = 'gasfired'
wind_turbine = 'windturbine'
kerosine_plant = 'turbojet'
load_objective = 480
