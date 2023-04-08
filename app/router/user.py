from fastapi import APIRouter, Depends, HTTPException
from schema.user_schema import Register , user_show , Response
from base import checking
import datetime
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import pytz
from database import mongodb as db
from base.depency import basic_authenticate, Token, create_access_token, permissions
from  Accsess import info_acsess
from instances import Mongo as variables


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

# @router.post('/register')
# async def registers(*,
#                     current_user: user_show = Depends(permissions(info_acsess.admin)), item: Register):
#     try:
#
#         count = db.User_collection.count({'username': item.username})
#         data = item.dict()
#         if count > 0:
#             data['Error'] = True
#             return {
#                 'done' :False
#             }
#         else:
#             passwords = checking.hash_passing(passwords=item.passwords)
#             data['passwords'] = passwords
#             data['create_time'] = today_date
#             data['create_by'] = current_user.id
#             db.User_collection.insert_one(data)
#             return {
#                 'done' :True
#             }
#     except Exception as e:
#         raise HTTPException(status_code=505, detail={'error':e})
#



@router.post('/login')
async def Login(current_user: user_show = Depends(basic_authenticate)):
    data = {
        "sub": str(current_user.id),
        "username": current_user.username,
        "scope": [*current_user.role, "authenticated"]
    }
    access_token = create_access_token(data)
    return Token(access_token=access_token, token_type="bearer")



