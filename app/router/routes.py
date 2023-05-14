# from schema.user_schema import user_show
# from base import checking

import requests
from fastapi import APIRouter, Request

from database import mongodb as db
from instances import Mongo as variables
from schema import routes_schema as model

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


@router.post('/check', response_model=model.Response)
async def set_endpoints(request: Request):
    # print(request.url.path)
    response = model.Response()
    try:
        url = variables.VariablesMongoDb.urls + 'openapi.json'
        print(url)
        data = requests.get('http://127.0.0.1:8000/openapi.json').json()
        all_key: dict = data['paths']
        route_address = all_key.keys()
        for item in route_address:
            address = item
            second: dict = all_key[item]
            methods: dict = second.keys()
            method_name = list(methods)[0]
            tag = all_key[item][method_name][variables.VariablesMongoDb.tags][0]
            summery = all_key[item][method_name][variables.VariablesMongoDb.summary]
            counter = db.route_collection.count_documents(
                {
                    variables.VariablesMongoDb.address: address
                }
            )
            if counter > 0:
                db.route_collection.update_one(
                    {
                        variables.VariablesMongoDb.address: address
                    },
                    {
                        "$set": {
                            variables.VariablesMongoDb.address: address,
                            variables.VariablesMongoDb.MethodName: method_name,
                            variables.VariablesMongoDb.TagName: tag,
                            variables.VariablesMongoDb.summary: summery,

                        }
                    }
                )
            else:
                db.route_collection.insert_one({
                    variables.VariablesMongoDb.address: address,
                    variables.VariablesMongoDb.MethodName: method_name,
                    variables.VariablesMongoDb.TagName: tag,
                    variables.VariablesMongoDb.summary: summery,
                })

        response.Done = True
        response.ErrorMessage = ''
        return response.dict()

    except Exception:
        response.Done = False
        response.ErrorMessage = 'خطای داخلی سرور'
        return response.dict()


@router.get('/lists', response_model=model.ListResponse)
async def lists():
    data = db.route_collection.find()
    response = model.ListResponse()
    final_list = []
    for item in data:
        epoch = model.List()
        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.address = item[variables.VariablesMongoDb.address]
        epoch.summary = item[variables.VariablesMongoDb.summary]
        epoch.TagName = item[variables.VariablesMongoDb.TagName]
        final_list.append(epoch.dict())

    response.data = final_list
    return response.dict()
