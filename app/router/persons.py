# from schema.user_schema import user_show
# from base import checking
import datetime

from bson import ObjectId
from fastapi import APIRouter

from database import mongodb as db
from instances import Mongo as variables
from schema import person_schema as model
from schema.user_schema import Response

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


@router.post('/create', response_model=model.SimpleResponse)
async def create(item: model.Create):
    response = model.SimpleResponse()

    try:

        counter = db.User_collection.count_documents(
            {
                variables.VariablesMongoDb.national_code: item.national_code
            }
        )
        if counter > 0:
            response.Done = False
            response.ErrorMassage = 'خطا در درج اطلاعات به دلیل تکراری بودن کد ملی'
            return response.dict()
        else:
            data = item.dict()
            data[variables.VariablesMongoDb.create_at] = datetime.datetime.now()
            data[variables.VariablesMongoDb.create_by] = ''
            data[variables.VariablesMongoDb.update_history] = []
            data[variables.VariablesMongoDb.active] = True
            data[variables.VariablesMongoDb.last_update] = ''
            res = db.User_collection.insert_one(data)
            if res.acknowledged:
                response.Done = True
                response.ErrorMassage = ''
            else:
                response.Done = False
                response.ErrorMassage = 'خطا در درج اطلاعات در دیتابیس'

            return response.dict()
    except Exception:
        response.Done = False
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.put('/update', response_model=model.SimpleResponse)
async def update(item: model.Update):
    response = model.SimpleResponse()
    try:
        data = db.User_collection.find_one({
            variables.VariablesMongoDb.id: ObjectId(item.id)
        })

        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$set": {
                    variables.VariablesMongoDb.national_code: item.national_code,
                    variables.VariablesMongoDb.name: item.name,
                    variables.VariablesMongoDb.role: item.role,
                    variables.VariablesMongoDb.family: item.family,
                    variables.VariablesMongoDb.position_id: item.position_id,
                    variables.VariablesMongoDb.grade_id: item.grade_id,
                    variables.VariablesMongoDb.last_update: datetime.datetime.now()

                }
            }
        )

        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$push": {
                    variables.VariablesMongoDb.update_history: {
                        variables.VariablesMongoDb.update_by: '',
                        variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                        variables.VariablesMongoDb.national_code: data[variables.VariablesMongoDb.national_code],
                        variables.VariablesMongoDb.name: data[variables.VariablesMongoDb.name],
                        variables.VariablesMongoDb.role: data[variables.VariablesMongoDb.role],
                        variables.VariablesMongoDb.family: data[variables.VariablesMongoDb.family],
                        variables.VariablesMongoDb.position_id: data[variables.VariablesMongoDb.position_id],
                        variables.VariablesMongoDb.grade_id: data[variables.VariablesMongoDb.grade_id],
                        variables.VariablesMongoDb.describe: "تغییر در مشخصات کاربر"

                    }
                }
            }
        )
        response.Done = True
        response.ErrorMassage = ''
        return response.dict()
    except Exception:
        response.Done = False
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.delete('/delete', response_model=model.SimpleResponse)
async def delete(item: model.Delete):
    response = model.SimpleResponse()
    try:
        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)

            },
            {
                "$set": {
                    variables.VariablesMongoDb.active: False
                }

            }

        )

        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$push": {
                    variables.VariablesMongoDb.update_history: {
                        variables.VariablesMongoDb.update_by: '',
                        variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                        variables.VariablesMongoDb.active: True,
                        variables.VariablesMongoDb.describe: "تفییر در فعالسازی کاربر به حالت خاموش"

                    }
                }
            }
        )
        response.Done = True
        response.ErrorMassage = ''
        return response.dict()
    except Exception:
        response.Done = False
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.patch('/active', response_model=model.SimpleResponse)
async def active(item: model.Delete):
    response = model.SimpleResponse()
    try:
        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: item.id

            },
            {
                "$set": {
                    variables.VariablesMongoDb.active: False
                }

            }
        )
        db.User_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(item.id)
            },
            {
                "$push": {
                    variables.VariablesMongoDb.update_history: {
                        variables.VariablesMongoDb.update_by: '',
                        variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                        variables.VariablesMongoDb.active: False,
                        variables.VariablesMongoDb.describe: "تفییر در فعالسازی کاربر به حالت فعال"

                    }
                }
            }
        )
        response.Done = True
        response.ErrorMassage = ''
        return response.dict()
    except Exception:
        response.Done = False
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.get('/list', response_model=model.ResponseList)
async def lists():
    response = model.ResponseList()
    try:
        final_list = []
        pipeline = [
            {
                "$match": {
                    "name": {
                        "$ne": "super_admin"
                    }
                }
            },
            {
                u"$lookup": {
                    u"from": u"roles",
                    u"localField": u"role",
                    u"foreignField": u"_id",
                    u"as": u"role_name"
                }
            },
            {
                u"$lookup": {
                    u"from": u"Position",
                    u"localField": u"position_id",
                    u"foreignField": u"_id",
                    u"as": u"position_name"
                }
            },
            {
                u"$lookup": {
                    u"from": u"Grade",
                    u"localField": u"grade_id",
                    u"foreignField": u"_id",
                    u"as": u"grade_name"
                }
            }
        ]
        data = db.User_collection.aggregate(pipeline=pipeline)
        for items in data:
            epoch = model.Lists()
            epoch.id = items[variables.VariablesMongoDb.id]
            epoch.name = items[variables.VariablesMongoDb.name]
            epoch.national_code = items[variables.VariablesMongoDb.national_code]
            epoch.role = items[variables.VariablesMongoDb.role]
            epoch.family = items[variables.VariablesMongoDb.family]
            epoch.active = items[variables.VariablesMongoDb.active]
            epoch.grade_id = items[variables.VariablesMongoDb.grade_id]
            epoch.grade_name = items[variables.VariablesMongoDb.grade_name][0][variables.VariablesMongoDb.name]
            epoch.position_id = items[variables.VariablesMongoDb.position_id]
            epoch.position_name = items[variables.VariablesMongoDb.position_name][0][variables.VariablesMongoDb.name]
            epoch.update_history = items[variables.VariablesMongoDb.update_history]
            epoch.role_name = items[variables.VariablesMongoDb.role_name][0][variables.VariablesMongoDb.name]
            final_list.append(epoch.dict())

        response.data = final_list
        response.Done = True
        return response.dict()
    except :
        response.Done = False
        response.data = []
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.get('/list/{filter}', response_model=model.ResponseList)
async def list_person(filter: str):
    try:
        response = model.ResponseList()
        final_list = []
        pipeline = [
            {
                "$match": {
                    u"name": {
                        u"$ne": u"super_admin"
                    }
                }
            },
            {
                u"$lookup": {
                    u"from": u"Position",
                    u"localField": u"position_id",
                    u"foreignField": u"_id",
                    u"as": u"position_name"
                }
            },
            {
                u"$lookup": {
                    u"from": u"Grade",
                    u"localField": u"grade_id",
                    u"foreignField": u"_id",
                    u"as": u"grade_name"
                }
            },
            {
                u"$match": {
                    u"$or": [
                        {
                            u"name": {
                                u"$regex": filter
                            }
                        },
                        {
                            u"family": {
                                u"$regex": filter
                            }
                        },
                        {
                            u"national_code": {
                                u"$regex": filter
                            }
                        },
                        {
                            u"grade_name.0.name": {
                                u"$regex": filter
                            }
                        },
                        {
                            u"position_name.0.name": {
                                u"$regex": filter
                            }
                        }
                    ]
                }
            }
        ]
        data = db.User_collection.aggregate(pipeline=pipeline)
        for items in data:
            epoch = model.Lists()
            epoch.name = items[variables.VariablesMongoDb.name]
            epoch.national_code = items[variables.VariablesMongoDb.national_code]
            epoch.role = items[variables.VariablesMongoDb.role]
            epoch.family = items[variables.VariablesMongoDb.family]
            epoch.active = items[variables.VariablesMongoDb.active]
            epoch.grade_id = items[variables.VariablesMongoDb.grade_id]
            epoch.grade_name = items[variables.VariablesMongoDb.grade_name][0][variables.VariablesMongoDb.name]
            epoch.position_id = items[variables.VariablesMongoDb.position_id]
            epoch.position_name = items[variables.VariablesMongoDb.position_name][0][variables.VariablesMongoDb.name]
            epoch.update_history = items[variables.VariablesMongoDb.update_history]
            final_list.append(epoch.dict())

        response.data = final_list
        response.Done = True
        response.ErrorMassage = ''
        return response.dict()

    except Exception:
        response.Done = False
        response.data = []
        response.ErrorMassage = 'خطای داخلی سرور'
        return response.dict()


@router.get('/create_admin/{password}', response_model=Response)
async def admin(password: str):
    response = Response()
    if password == 'HADInabati0':

        final_list = []
        count = db.User_collection.count_documents(
            {
                variables.VariablesMongoDb.name: 'super_admin'
            }
        )

        if count > 0:
            data = db.route_collection.find()
            for item in data:
                final_list.append(item[variables.VariablesMongoDb.id])
            db.User_collection.update_one(
                {
                    variables.VariablesMongoDb.name: 'super_admin'
                },
                {
                    "$set":{
                        variables.VariablesMongoDb.role : final_list
                    }
                }
            )
            response.Done = True
            response.ErrorMessage = 'بروزرسانی انجام شد'
            return response.dict()
        else:
            data = db.route_collection.find()
            for item in data:
                final_list.append(item[variables.VariablesMongoDb.id])

            data = model.Create()
            data.name = 'super_admin'
            data.family = 'fava'
            data.role = final_list
            data.grade_id =''
            data.position_id = ''
            data.national_code = ''
            res =data.dict()
            res[variables.VariablesMongoDb.active] = True
            res[variables.VariablesMongoDb.create_at] = datetime.datetime.now()
            res[variables.VariablesMongoDb.create_by] =''
            res[variables.VariablesMongoDb.update_history] = []
            res[variables.VariablesMongoDb.last_update] = ''

            db.User_collection.insert_one(res)
            response.Done = True
            response.ErrorMessage = 'کاربر ثبت شد'
            return response.dict()

    else:
        response.Done = False
        response.ErrorMessage = 'خطای ورود'
        return response.dict()
