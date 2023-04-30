# from schema.user_schema import user_show
# from base import checking
import datetime
from fastapi import APIRouter
from database import mongodb as db
from schema import activities_schema as model
from instances import Mongo as variable
from bson import ObjectId

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


@router.post('/create', response_model=model.SimpleResponse)
async def create(item: model.CreateSample):
    response = model.SimpleResponse()
    count = db.activity_collection.count_documents({
        variable.VariablesMongoDb.name: item.name
    })
    if count > 0:
        response.Done = False
        response.Message = 'نام انتخابی تکراری است'
        return response.dict()
    else:
        data = item.dict()
        data[variable.VariablesMongoDb.create_at] = datetime.datetime.now()
        data[variable.VariablesMongoDb.create_by] = ''
        data[variable.VariablesMongoDb.active] = True
        db.activity_collection.insert_one(data)

        response.Done = True
        response.Message = 'عملیات با موفقیت انحام شد'

        return response.dict()


@router.delete('/delete', response_model=model.SimpleResponse)
async def delete(item: model.Deactivated):
    response = model.SimpleResponse()
    res = db.activity_collection.update_one(
        {
            variable.VariablesMongoDb.id: ObjectId(item.id)
        },
        {
            "$set": {
                variable.VariablesMongoDb.active: False
            }
        })

    if res.matched_count > 0:
        response.Done = True
        response.Message = 'عملیات تغییر حالت با موفقیت انجام شد'
    else:
        response.Done = False
        response.Message = 'موردی برای تغییر یافت نشد'

    return response.dict()


@router.put('/active', response_model=model.SimpleResponse)
async def active(item: model.Deactivated):
    response = model.SimpleResponse()
    res = db.activity_collection.update_one(
        {
            variable.VariablesMongoDb.id: ObjectId(item.id)
        },
        {
            "$set": {
                variable.VariablesMongoDb.active: True
            }
        })

    if res.matched_count > 0:
        response.Done = True
        response.Message = 'عملیات تغییر حالت با موفقیت انجام شد'
    else:
        response.Done = False
        response.Message = 'موردی برای تغییر یافت نشد'

    return response.dict()


@router.get('/list', response_model=model.ResponseList)
async def lists():
    data = db.activity_collection.find()
    final_list = []
    for item in data:
        epoch = model.ListItem()
        epoch.id = item[variable.VariablesMongoDb.id]
        epoch.name = item[variable.VariablesMongoDb.name]
        epoch.properties = item[variable.VariablesMongoDb.properties]
        epoch.active = item[variable.VariablesMongoDb.active]
        epoch.create_date = item[variable.VariablesMongoDb.create_at]
        epoch.category_id = item[variable.VariablesMongoDb.category_id]
        final_list.append(epoch.dict())

    response = model.ResponseList()
    response.data = final_list
    return response.dict()


@router.get('/list/{category_id}', response_model=model.ResponseList)
async def list_of_category_id(
        category_id: str
):
    data = db.activity_collection.find(
        {
            variable.VariablesMongoDb.category_id: ObjectId(category_id)
        }
    )
    final_list = []
    for item in data:
        epoch = model.ListItem()
        epoch.id = item[variable.VariablesMongoDb.id]
        epoch.name = item[variable.VariablesMongoDb.name]
        epoch.properties = item[variable.VariablesMongoDb.properties]
        epoch.active = item[variable.VariablesMongoDb.active]
        epoch.create_date = item[variable.VariablesMongoDb.create_at]
        final_list.append(epoch.dict())

    response = model.ResponseList()
    response.data = final_list
    return response.dict()
