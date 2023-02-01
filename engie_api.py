from fastapi import Request, FastAPI
from functions.utils import load_params, process_json
import uvicorn

app = FastAPI()

#########################################################################################
# https://fastapi.tiangolo.com/es/tutorial/body-multiple-params/#singular-values-in-body


# async def root1(request: Request):
@app.post("/productionplan")
async def get_body(request: Request):
    """
    This endpoint receives a POST of which the body contains a list of resources to be analyzed to get the most
    effective energy to satisfy the load demand
    :param request:
    :return:
    """
    aux = await request.json()
    my_json = process_json(aux)
    return my_json


if __name__ == '__main__':
    load_params()
    uvicorn.run("engie_api:app", port=8500, log_level="info")






