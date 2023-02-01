# Engie challenge

This challenge uses FastAPI to create a JSON. 

To run the code, create an enviroment and then, run the following code in the enviromnet to install the requirementes file

```
pip install -r requirements.txt
```

To run the API:
```
uvicorn.run("engie_api:app", port=8888, log_level="info")
```
Once the API is running, wirthe the following in the browser to see the documentation about the endpoints:

```
example: http://127.0.0.1:8888/docs
```
All the constants are in a file called src/constants/constants.py

The main function is
```
def process_json(data):
```
This function receives a JSON and processes to get the resources needed to generate the load required. To do so,
there is a dictionary called cost_priorities (in src/constants/constants.py) to prioritize the resources by 'cost'
Returns the required json with the names of the resources and the amount of energy they should provide in key p.
 
this API generates a json file with the required information:

example:
[{'name': 'windpark1', 'p': 90},
 {'name': 'windpark2', 'p': 21},
 {'name': 'gasfiredbig1', 'p': 243.8},
 {'name': 'gasfiredbig2', 'p': 125.2},
 {'name': 'gasfiredsomewhatsmaller', 'p': 0.0},
 {'name': 'tj1', 'p': 0.0}]





