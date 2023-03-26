# from schema.user_schema import user_show
# from base import checking
import datetime

import pytz
from fastapi import APIRouter
from persiantools.jdatetime import JalaliDate, JalaliDateTime

from database import mongodb as db
from schema import grade_schema as Model

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

@router.post('/create' , response_model=Model.Response)
async  def create(item : Model.Create):
    data = item.dict()
    data['Create_at'] = datetime.datetime.now()
    response = Model.Response()
    res = db.grade_collection.insert_one(data).acknowledged
    if res :
        response.Done = True
        response.Message = 'اطلاعات با موفقیت ثبت شدند'
        return  response.dict()
    else:
        response.Done = False
        response.Message = 'خطا در درج اطلاعات'
        return response.dict()


@router.put('/update' , response_model=Model.Response)
async  def Update(item : Model.Items):
    pass




@router.get('/list' , response_model=Model.Lists)
async  def lists():
    all_data = list(db.grade_collection.find())
    response = Model.Lists()
    final_list =[]
    for item in all_data :
        epoch = Model.Items()
        epoch.id = item['_id']
        epoch.name = item['name']
        epoch.description = item['description']
        final_list.append(epoch.dict())
    response.item = final_list
    return  response.dict()


