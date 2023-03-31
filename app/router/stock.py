# from schema.user_schema import user_show
# from base import checking
import datetime

from fastapi import APIRouter
from Time import local_time
from instances import Mongo as variables
from database import mongodb as db
from schema import stock_schema as model
from bson import ObjectId

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


# ----------------------------- end importing --------------------------------------

# ----------------------------- starting routing -----------------------------------


@router.post('/create', response_model=model.Response)
async def create(item: model.Create):
    response = model.Response()
    name = variables.VariablesMongoDb()
    try:
        counter = db.stock_collection.count_documents(
            {
                name.stock_number: item.stock_number
            }
        )
        if counter > 0:
            response.Done = False
            response.Message = 'کالا از قبل ثبت شده است'
            return response.dict()
        else:
            data = item.dict()
            data[name.repair_history] = []
            data[name.update_history] = []
            data[name.create_date] = datetime.datetime.now()
            res = db.stock_collection.insert_one(data).acknowledged
            if res:
                response.Done = True
                response.Message = 'عملیا تبا موفقیت انجام شد'
                return response.dict()
            else:
                response.Done = False
                response.Message = 'خطا در درج اطلاعات در دیتابیس'
                return response.dict()
    except ValueError:
        response.Done = False
        response.Message = 'خطا در سرور'
        return response.dict()


@router.put('/update', response_model=model.Response)
async def update(items: model.Update):
    response = model.Response()
    try:
        last_data = db.stock_collection.find_one(
            {
                "_id": ObjectId(items.id)
            }
        )
        if items.stock_number == items.old_stock_number:
            pipline = [
                {
                    "$match": {
                        "_id": ObjectId(items.id)
                    }
                },
                {
                    "$set": {
                        "name": items.name,
                        "category_id": items.category_id,
                        "response_id": items.response_id,
                        "active": items.active,
                        "position_id": items.position_id,
                        "has_response": items.has_response,
                        "info": items.info,
                        "update_at": datetime.datetime.now(),
                        "update_by": "",
                        "is_consumer": items.is_consumer
                    }
                },

            ]
            # correct stock with  old stock_number
            db.stock_collection.aggregate(pipeline=pipline)
            db.stock_collection.update_one(
                {
                    "_id": ObjectId(items.id)
                },
                {
                    "$push": {
                        "update_history": {
                            "name": last_data["name"],
                            "category_id": last_data["category_id"],
                            "response_id": last_data["response_id"],
                            "active": last_data["active"],
                            "position_id": last_data["position_id"],
                            "has_response": last_data["has_response"],
                            "info": last_data["info"],
                            "is_consumer": last_data["is_consumer"],
                            "stock_number": last_data["stock_number"],
                            "Description": "شماره اموال تغییر نکرده است"

                        }
                    }
                }
            )

            response.Done = True
            response.Message = 'عملیات با موفقیت انجام شد'
            return response.dict()

            # correct stock with new stock_number
        else:
            count = db.stock_collection.count_documents({
                "stock_number": items.stock_number
            })
            if count > 0:
                response.Done = False
                response.Message = 'شماره اموال مربوط به کالای دیگری است'
                return response.dict()
            else:
                res = db.stock_collection.update_one(
                    {
                        "_id": ObjectId(items.id)
                    },
                    {
                        "$set": {
                            "name": items.name,
                            "category_id": items.category_id,
                            "response_id": items.response_id,
                            "active": items.active,
                            "position_id": items.position_id,
                            "has_response": items.has_response,
                            "info": items.info,
                            "update_at": datetime.datetime.now(),
                            "update_by": "",
                            "is_consumer": items.is_consumer,
                            "stock_number": items.stock_number,
                        }
                    },

                )
                db.stock_collection.update_one(
                    {
                        "_id": ObjectId(items.id)
                    },
                    {
                        "$push": {
                            "update_history": {
                                "name": last_data["name"],
                                "category_id": last_data["category_id"],
                                "response_id": last_data["response_id"],
                                "active": last_data["active"],
                                "position_id": last_data["position_id"],
                                "has_response": last_data["has_response"],
                                "info": last_data["info"],
                                "is_consumer": last_data["is_consumer"],
                                "stock_number": last_data["stock_number"],
                                "Description": "شماره اموال تغییر کرده است"
                            }
                        }
                    }
                )

                if res.matched_count > 0:
                    response.Done = True
                    response.Message = 'عملیات با موفقیت انجام شد'
                    return response.dict()
                else:
                    response.Done = False
                    response.Message = 'موردی برای تغییر یافت نشده است'
                    return response.dict()

    except IndexError:
        response.Done = False
        response.Message = 'خطا در سرور '
        return response.dict()


@router.get('/list', response_model=model.Lists)
async def lists():
    pipline = [
        {
            "$lookup": {
                "from": "Category",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category_name"
            }

        },
        {
            "$lookup": {
                "from": "Position",
                "localField": "position_id",
                "foreignField": "_id",
                "as": "position_name"
            }
        }
    ]
    data = db.stock_collection.aggregate(pipeline=pipline)
    response = model.Lists()
    final_data = []
    for item in data:
        items = model.Item()
        items.id = item['_id']
        items.name = item['name']
        items.is_consumer = item['is_consumer']
        items.create_date = item['create_date']
        items.category_id = item['category_id']
        items.response_id = item['response_id']
        items.active = item['active']
        items.repair_history = item['repair_history']
        items.position_id = item['position_id']
        items.has_response = item['has_response']
        items.stock_number = item['stock_number']
        items.info = item['info']
        items.update_history = item['update_history']
        items.category_name = item["category_name"][0]['name']
        # items.response_name = item["response_name"][0]['name']
        items.response_name = ''
        items.position_name = item["position_name"][0]['name']
        final_data.append(items.dict())
    response.items = final_data
    return response.dict()
