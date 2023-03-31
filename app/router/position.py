# from schema.user_schema import user_show
# from base import checking
import datetime

import pytz
from fastapi import APIRouter
from persiantools.jdatetime import JalaliDate, JalaliDateTime

from database import mongodb as db
from schema import postion_schema as model
from bson import ObjectId

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()

# ----------------------------- end importing --------------------------------------

collection = db.User_collection
today_date = JalaliDate(JalaliDate.today()).strftime("%Y_%m_%d")
date_spilted = today_date.split('_')
hour = datetime.datetime.now().hour
miniute = datetime.datetime.now().minute
times = '{}:{}'.format(hour, miniute)
prz = JalaliDateTime(int(date_spilted[0]), int(date_spilted[1]), int(date_spilted[2]), hour, miniute, 0, 0,
                     pytz.utc).strftime("%c")
name_of_day = prz.split(' ')[0]


# -----------------------------------------   starting routing ------------------------

@router.post('/create', response_model=model.Response)
async def create(item: model.Create):
    data = item.dict()
    data['Create_at'] = datetime.datetime.now()
    response = model.Response()
    res = db.position_collection.insert_one(data).acknowledged
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
        count = db.position_collection.update_one({'_id': ObjectId(item.id)}, {
            '$set': {'name': item.name,
                     'description': item.description,
                     'updated_at': datetime.datetime.now(),
                     'updated_by': ''}
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
    all_data = list(db.position_collection.find())
    response = model.Lists()
    final_list = []
    for item in all_data:
        epoch = model.Items()
        epoch.id = item['_id']
        epoch.name = item['name']
        epoch.description = item['description']
        final_list.append(epoch.dict())
    response.item = final_list
    #
    return response.dict()
