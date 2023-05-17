# from schema.user_schema import user_show
# from base import checking
import datetime

from bson import ObjectId
from fastapi import APIRouter

from database import mongodb as db
from instances import Mongo as variables
from schema import role_schema as model
from schema.routes_schema import List

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


@router.post('/create', response_model=model.Response)
async def create(item: model.Create):
    response = model.Response()
    try:
        count = db.roles_collection.count_documents(
            {
                variables.VariablesMongoDb.name: item.name
            }
        )
        if count > 0:
            response.Done = False
            response.ErrorMessage = 'نام نقش تکراری است'
            return response.dict()
        else:
            data = item.dict()
            data[variables.VariablesMongoDb.active] = True
            db.roles_collection.insert_one(data)
            response.Done = True
            response.ErrorMessage = ''
            return response.dict()

    except Exception:
        response.Done = False
        response.ErrorMessage = 'خطای داخلی سرور'
        return response.dict()


@router.get('/lists', response_model=model.ResponseList)
async def lists():
    data = db.roles_collection.find(
        {
            "name":{"$ne":"super_admin"}
        }
    )
    response = model.ResponseList()
    final_list = []
    for item in data:
        epoch = model.Lists()
        epoch.name = item[variables.VariablesMongoDb.name]
        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.items = item[variables.VariablesMongoDb.items]
        epoch.active = item[variables.VariablesMongoDb.active]
        final_list.append(epoch.dict())
    response.data = final_list
    return response.dict()


@router.get('/lists/{id}', response_model=model.ResponseId)
async def list_id(id: str):
    pipline = [
        {
            u"$match": {
                u"_id": ObjectId(id)
            }
        },
        {
            u"$unwind": {
                u"path": u"$items"
            }
        },
        {
            u"$lookup": {
                u"from": u"routes",
                u"localField": u"items",
                u"foreignField": u"_id",
                u"as": u"items"
            }
        }
    ]
    response = model.ResponseId()
    data = list(db.roles_collection.aggregate(pipeline=pipline))
    response.name = data[0][variables.VariablesMongoDb.name]
    response.active = data[0][variables.VariablesMongoDb.active]
    final_list = []
    for item in data:
        epoch = List()
        epoch.id = item[variables.VariablesMongoDb.items][0][variables.VariablesMongoDb.id]
        epoch.address = item[variables.VariablesMongoDb.items][0][variables.VariablesMongoDb.address]
        epoch.TagName = item[variables.VariablesMongoDb.items][0][variables.VariablesMongoDb.TagName]
        epoch.summary = item[variables.VariablesMongoDb.items][0][variables.VariablesMongoDb.summary]
        final_list.append(epoch.dict())

    response.items = final_list
    return response.dict()


@router.delete('/deleted', response_model=model.Response)
async def deactivate(item: model.Change):
    response = model.Response()
    try:
        res = db.roles_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$set":{
                    variables.VariablesMongoDb.active : False ,
                    variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                    variables.VariablesMongoDb.update_by: ''
                }
            }
        )
        if res.matched_count > 0:
            response.Done = True
            response.ErrorMessage = ''
        else:
            response.Done = False
            response.ErrorMessage = 'موردی برای تغییر یافت نشد'

        return response.dict()

    except Exception:
        response.Done = False
        response.ErrorMessage = 'موردی برای تغییر یافت نشد',
        return response.dict()



@router.patch('/activated', response_model=model.Response)
async def activated(item: model.Change):
    response = model.Response()
    try:
        res = db.roles_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$set":{
                    variables.VariablesMongoDb.active : True,
                    variables.VariablesMongoDb.update_at :datetime.datetime.now(),
                    variables.VariablesMongoDb.update_by :''
                }
            }
        )
        if res.matched_count > 0:
            response.Done = True
            response.ErrorMessage = ''
        else:
            response.Done = False
            response.ErrorMessage = 'موردی برای تغییر یافت نشد'

        return response.dict()

    except Exception:
        response.Done = False
        response.ErrorMessage = 'موردی برای تغییر یافت نشد',
        return response.dict()


@router.put('/update', response_model=model.Response)
async def update(item: model.Update):
    response = model.Response()
    try:
        res = db.roles_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$set":{
                    variables.VariablesMongoDb.name :item.name,
                    variables.VariablesMongoDb.items :item.items
                }
            }
        )
        if res.matched_count > 0:
            response.Done = True
            response.ErrorMessage = ''
        else:
            response.Done = False
            response.ErrorMessage = 'موردی برای تغییر یافت نشد'

        return response.dict()

    except Exception:
        response.Done = False
        response.ErrorMessage = 'موردی برای تغییر یافت نشد',
        return response.dict()
