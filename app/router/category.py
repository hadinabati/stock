# from schema.user_schema import user_show
# from base import checking
import datetime

from bson import ObjectId
from fastapi import APIRouter

from database import mongodb as db
from instances import Mongo as variables
from schema import category_schema as model

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


# ----------------------------- end importing --------------------------------------

# -----------------------------------------   starting routing ------------------------

@router.post('/create', response_model=model.Response)
async def create(item: model.Create):
    data = item.dict()
    data[variables.VariablesMongoDb.create_at] = datetime.datetime.now()
    response = model.Response()
    res = db.category_collection.insert_one(data).acknowledged
    if res:
        response.Done = True
        response.Message = 'اطلاعات با موفقیت ثبت شدند'
        return response.dict()
    else:
        response.Done = False
        response.Message = 'خطا در درج اطلاعات'
        return response.dict()


@router.put('/update', response_model=model.Response)
async def update(item: model.Items):
    response = model.Response()
    try:
        count = db.category_collection.update_one({'_id': ObjectId(item.id)}, {
            '$set': {variables.VariablesMongoDb.name: item.name,
                     variables.VariablesMongoDb.info: item.info,
                     variables.VariablesMongoDb.description: item.description,
                     variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                     variables.VariablesMongoDb.update_by: ''}
        }).matched_count
        if count > 0:
            response.Done = True
            response.Message = 'عملیات با موفقیت انجام شد'
            return response.dict()
        else:
            response.Done = False
            response.Message = 'موردی در دیتابیس یافت نشد'
            return response.dict()
    except IndexError:
        response.Done = False
        response.Message = 'خطا در انجام عملیات'
        return response.dict()


@router.get('/list', response_model=model.Lists)
async def lists():
    all_data = list(db.category_collection.find())
    response = model.Lists()
    final_list = []
    for item in all_data:
        epoch = model.Items()
        epoch.info = item[variables.VariablesMongoDb.info]
        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.name = item[variables.VariablesMongoDb.name]
        epoch.description = item[variables.VariablesMongoDb.description]
        final_list.append(epoch.dict())
    response.item = final_list
    #
    return response.dict()


@router.get('/list/{id}', response_model=model.Lists)
async def list_item(id: str):
    all_data = list(db.category_collection.find(
        {variables.VariablesMongoDb.id: ObjectId(id)}
    ))
    response = model.Lists()
    final_list = []
    for item in all_data:
        epoch = model.Items()
        epoch.info = item[variables.VariablesMongoDb.info]
        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.name = item[variables.VariablesMongoDb.name]
        epoch.description = item[variables.VariablesMongoDb.description]
        final_list.append(epoch.dict())
    response.item = final_list
    #
    return response.dict()
