# from schema.user_schema import user_show
# from base import checking
import datetime

from bson import ObjectId
from fastapi import APIRouter

from database import mongodb as db
from instances import Mongo as variables
from schema import stock_schema as model

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
            data[name.category_id] = ObjectId(item.category_id)
            data[name.repair_history] = []
            data[name.update_history] = []
            data[name.accession_history] = []
            data[name.active] = True
            data[name.health] = True
            data[name.accession] = []
            data[name.create_date] = datetime.datetime.now()

            if item.has_response is True:
                person_data = db.User_collection.find_one({name.id: ObjectId(item.response_id)})

                data[name.response_id] = ObjectId(item.response_id)
                data[name.position_id] = ObjectId(person_data[name.position_id])
            else:
                super_admin_data = db.User_collection.find_one({
                    name.name: name.super_admin
                })
                data[name.response_id] = ObjectId(super_admin_data[name.id])
                data[name.position_id] = ObjectId(item.position_id)

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
                            "Description": "شماره اموال تغییر نکرده است",
                            variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                            variables.VariablesMongoDb.users: '',
                            variables.VariablesMongoDb.type: 'Edit',
                            variables.VariablesMongoDb.count: last_data[variables.VariablesMongoDb.count]
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
                                "Description": "شماره اموال تغییر کرده است",
                                variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                                variables.VariablesMongoDb.users: '',
                                variables.VariablesMongoDb.type: 'Edit',
                                variables.VariablesMongoDb.count: last_data[variables.VariablesMongoDb.count]
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
        },
        {
            "$lookup": {
                "from": "User",
                "localField": "response_id",
                "foreignField": "_id",
                "as": "response_name"
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
        items.properties = item["category_name"][0]['info']
        items.response_name = item["response_name"][0]['name'] + ' -' + item["response_name"][0]['family']
        items.position_name = item["position_name"][0]['name']
        items.count = item['count']
        final_data.append(items.dict())
    response.items = final_data
    return response.dict()


@router.get('/list_single', response_model=model.Lists)
async def single_list(text: str):
    number = -1
    try:
        number = int(text)
    except:
        pass

    pipeline = [
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
                u"from": u"Category",
                u"localField": u"category_id",
                u"foreignField": u"_id",
                u"as": u"category_name"
            }
        },
        {
            u"$lookup": {
                u"from": u"User",
                u"localField": u"response_id",
                u"foreignField": u"_id",
                u"as": u"response_name"
            }
        },
        {
            u"$match": {
                u"$or": [
                    {
                        u"name": {
                            "$regex": text
                        }
                    },
                    {
                        u"stock_number": int(number)
                    },
                    {
                        u"position_name.0.name": {
                            "$regex": text
                        }
                    },
                    {
                        u"category_name.0.name": {
                            "$regex": text
                        }
                    },
                    {
                        u"response_name.0.name": {
                            "$regex": text
                        }
                    },
                    {
                        u"response_name.0.family": {
                            "$regex": text
                        }
                    }
                ]
            }
        }
    ]
    data = db.stock_collection.aggregate(pipeline=pipeline)
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
        items.properties = item["category_name"][0]['info']
        items.response_name = item["response_name"][0]['name'] + ' -' + item["response_name"][0]['family']
        items.position_name = item["position_name"][0]['name']
        items.count = item['count']
        final_data.append(items.dict())
    response.items = final_data
    return response.dict()


@router.get('/list_is_consumer', response_model=model.Lists)
async def single_list(text: int, is_consumer: bool):
    pipeline = [
        {
            u"$match": {
                'is_consumer': is_consumer
            }
        },
        {
            u"$match": {
                u"stock_number": text
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
                u"from": u"Category",
                u"localField": u"category_id",
                u"foreignField": u"_id",
                u"as": u"category_name"
            }
        },
        {
            u"$lookup": {
                u"from": u"User",
                u"localField": u"response_id",
                u"foreignField": u"_id",
                u"as": u"response_name"
            }
        },

    ]
    data = db.stock_collection.aggregate(pipeline=pipeline)
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
        items.properties = item["category_name"][0]['info']
        items.response_name = item["response_name"][0]['name'] + ' -' + item["response_name"][0]['family']
        items.position_name = item["position_name"][0]['name']
        items.count = item['count']
        final_data.append(items.dict())
    response.items = final_data
    return response.dict()


@router.get('/consumer_list', response_model=model.ConsumerList)
async def consumer_list():
    pipeline = []
    data = db.stock_collection.aggregate(pipeline=pipeline)
    final_list =[]
    for item in data :
        epoch = model.ConsumerListItem()
        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.name = item[variables.VariablesMongoDb.name]
        epoch.stock_number = item[variables.VariablesMongoDb.stock_number]
        epoch.use_number = item[variables.VariablesMongoDb.use_number]
        epoch.crash_number = item[variables.VariablesMongoDb.crash_number]
        epoch.un_uses_number = item[variables.VariablesMongoDb.un_uses_number]
        epoch.total_number = item[variables.VariablesMongoDb.total_number]
        final_list.append(epoch.dict())

    response = model.ConsumerList()
    response.items = final_list
    return  response.dict()

@router.get('/crash_list', response_model=model.CrashList)
async def crash_list():
    pipeline = [
        {
            u"$lookup": {
                u"from": u"Stock",
                u"localField": u"stock_id",
                u"foreignField": u"_id",
                u"as": u"stock"
            }
        },
        {
            u"$lookup": {
                u"from": u"User",
                u"localField": u"stock.0.response_id",
                u"foreignField": u"_id",
                u"as": u"user"
            }
        },
        {
            u"$lookup": {
                u"from": u"Position",
                u"localField": u"stock.0.position_id",
                u"foreignField": u"_id",
                u"as": u"position"
            }
        },
        {
            u"$unwind": {
                u"path": u"$position"
            }
        },
        {
            u"$unwind": {
                u"path": u"$user"
            }
        },
        {
            u"$unwind": {
                u"path": u"$stock"
            }
        },
        {
            u"$project": {
                u"count": u"$count",
                u"stock_id": u"$stock_id",
                u"is_consumer": u"$is_consumer",
                u"update_history": u"$update_history",
                u"response_id": u"$stock.response_id",
                u"name": u"$stock.name",
                u"position_name": u"$position.name",
                u"position_id": u"$stock.position_id",
                u"response_name": u"$user.name"
            }
        }
    ]
    data  = db.crash_collection.aggregate(pipeline=pipeline)
    final_list =[]
    for item in data :
        epoch = model.CrashItem()

        epoch.id = item[variables.VariablesMongoDb.id]
        epoch.is_consumer = item[variables.VariablesMongoDb.is_consumer]
        epoch.Count = item[variables.VariablesMongoDb.count]
        epoch.update_history = item[variables.VariablesMongoDb.update_history]
        epoch.stock_id = item[variables.VariablesMongoDb.stock_id]
        epoch.name = item[variables.VariablesMongoDb.name]
        epoch.position_id = item[variables.VariablesMongoDb.position_id]
        epoch.position_name = item[variables.VariablesMongoDb.position_name]
        epoch.response_name = item[variables.VariablesMongoDb.response_name]
        epoch.response_id = item[variables.VariablesMongoDb.response_id]
        final_list.append(epoch.dict())

    response = model.CrashList()
    response.items = final_list
    return  response.dict()



@router.patch('/accession_add_remove', response_model=model.Response)
async def accession_add_remove(data: model.AddOrDeleteAccession):
    response = model.Response()
    pipeline = [
        {
            u"$match": {
                u"_id": ObjectId(data.stock_id)
            }
        },
        {
            u"$unwind": {
                u"path": u"$accession_history"
            }
        },
        {
            u"$match": {
                u"accession_history.accession_id": ObjectId(data.accession_number)
            }
        }
    ]
    stock_db = list(db.stock_collection.aggregate(pipeline=pipeline))
    if len(stock_db) > 0:

        if data.add == True:

            x =db.stock_collection.update_one(
                {
                    "accession_history.accession_id": ObjectId(data.accession_number),
                    variables.VariablesMongoDb.id: ObjectId(data.stock_id)
                },
                {
                    "$set": {
                        "accession_history.$.count": stock_db[0][variables.VariablesMongoDb.accession_history][
                                                                variables.VariablesMongoDb.count] + data.number,
                        variables.VariablesMongoDb.count: stock_db[0][variables.VariablesMongoDb.count] - data.number
                    },

                }
            )
            y =2


        else:

            db.stock_collection.update_one(
                {
                    "accession_history.accession_id": ObjectId(data.accession_number),
                    variables.VariablesMongoDb.id: ObjectId(data.stock_id)
                },
                {
                    "$set": {
                        "accession_history.$.count": stock_db[0][variables.VariablesMongoDb.accession_history][
                                                                variables.VariablesMongoDb.count] - data.number,
                        variables.VariablesMongoDb.count: stock_db[0][variables.VariablesMongoDb.count] + data.number
                    },

                }
            )

        response.Done = True
        response.Message = 'عملیات با موفقیت انجام شد'
        return response.dict()
    else:
        response.Done = False
        response.Message = 'کالایی با مشخصات وارد شده یافت نشده است'
        return response.dict()


@router.patch('/add_consumer_stock', response_model=model.Response)
async def add_consumer_stock(data: model.AddStock):
    response = model.Response()
    check = db.stock_collection.find_one({
        variables.VariablesMongoDb.active: True,
        variables.VariablesMongoDb.is_consumer: True,
        variables.VariablesMongoDb.id: ObjectId(data.stock_id)
    })
    if check is None:
        response.Done = False
        response.Message = 'کالایی یافت نشد'
        return response.dict()

    res = db.stock_collection.update_one(
        {
            variables.VariablesMongoDb.id: ObjectId(data.stock_id)
        },
        {
            "$set": {
                variables.VariablesMongoDb.count: check[variables.VariablesMongoDb.count] + data.number
            },
            "$push": {
                variables.VariablesMongoDb.update_history: {
                    variables.VariablesMongoDb.name: check[variables.VariablesMongoDb.name],
                    variables.VariablesMongoDb.category_id: check[variables.VariablesMongoDb.category_id],
                    variables.VariablesMongoDb.response_id: check[variables.VariablesMongoDb.response_id],
                    variables.VariablesMongoDb.active: check[variables.VariablesMongoDb.active],
                    variables.VariablesMongoDb.position_id: check[variables.VariablesMongoDb.position_id],
                    variables.VariablesMongoDb.has_response: check[variables.VariablesMongoDb.has_response],
                    variables.VariablesMongoDb.info: check[variables.VariablesMongoDb.info],
                    variables.VariablesMongoDb.is_consumer: check[variables.VariablesMongoDb.is_consumer],
                    variables.VariablesMongoDb.stock_number: check[variables.VariablesMongoDb.stock_number],
                    variables.VariablesMongoDb.users: '',
                    variables.VariablesMongoDb.count: data.number,
                    variables.VariablesMongoDb.type: 'Add',
                    variables.VariablesMongoDb.description: "اضافه کردن موجودی به انبار"
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
        response.Message = 'خطا در بروز رسانی'
        return response.dict()


@router.put('/accession', response_model=model.Response)
async def accession(data: model.Accession):
    response = model.Response()
    stock_count = db.stock_collection.find_one(
        {variables.VariablesMongoDb.id: data.stock_id}
    )
    countable = stock_count[variables.VariablesMongoDb.count]
    if data.number > countable:
        response.Done = False
        response.Message = 'تعداد ارجاع به کالا بیش از مقدار آن در انبار است'
        return response.dict()

    db.stock_collection.update_one(
        {
            variables.VariablesMongoDb.id: ObjectId(data.accession_number)
        },
        {
            "$push": {
                variables.VariablesMongoDb.accession: {
                    variables.VariablesMongoDb.stock_id: data.stock_id
                }
            },

        }
    )
    db.stock_collection.update_one(
        {
            variables.VariablesMongoDb.id: ObjectId(data.stock_id)
        },
        {
            "$set": {
                variables.VariablesMongoDb.count: countable - data.number
            },
            "$push": {
                variables.VariablesMongoDb.accession_history: {
                    variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                    variables.VariablesMongoDb.users: '',
                    variables.VariablesMongoDb.accession_id: data.accession_number,
                    variables.VariablesMongoDb.count: data.number

                }
            }

        }
    )
    response.Done = True
    response.Message = 'عملیات با موفقیت انجام شد'
    return response.dict()


@router.put('/crash', response_model=model.Response)
async def crash(data: model.Crash):
    response = model.Response()
    check_consumer = list(db.stock_collection.find(
        {
            variables.VariablesMongoDb.id: ObjectId(data.stock_id),
            variables.VariablesMongoDb.active: True
        }
    ))
    if len(check_consumer) > 0:
        consumer = check_consumer[0][variables.VariablesMongoDb.is_consumer]
        number = 1
        if consumer:
            number = data.number
        else:
            db.stock_collection.update_one({
                variables.VariablesMongoDb.id: ObjectId(data.stock_id),
            },
                {
                    "$set": {variables.VariablesMongoDb.active: False}
                })
        check_gt_ziro = check_consumer[0][variables.VariablesMongoDb.count] - number
        if check_gt_ziro < 0:
            response.Done = False
            response.Message = 'تعداد کالای خراب شده بیش از مقدار آن در انبار می باشد '
            return response.dict()

        db.stock_collection.update_one(
            {
                variables.VariablesMongoDb.id: ObjectId(data.stock_id),
            },
            {
                '$set': {
                    variables.VariablesMongoDb.count: check_consumer[0][variables.VariablesMongoDb.count] - number
                }
            }
        )

        check_crash_inserted_before = list(db.crash_collection.find(
            {
                variables.VariablesMongoDb.stock_id: ObjectId(data.stock_id),
            }
        ))
        if len(check_crash_inserted_before) > 0:
            db.crash_collection.update_one(
                {
                    variables.VariablesMongoDb.stock_id: ObjectId(data.stock_id),
                },
                {
                    "$set": {
                        variables.VariablesMongoDb.count: check_crash_inserted_before[0][
                                                              variables.VariablesMongoDb.count] + number
                    },
                    "$push": {
                        variables.VariablesMongoDb.update_history:
                            {variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                             variables.VariablesMongoDb.users: '',
                             variables.VariablesMongoDb.count: number,
                             variables.VariablesMongoDb.description: data.description,
                             variables.VariablesMongoDb.add: True}

                    }
                }
            )
        else:
            db.crash_collection.insert_one(
                {
                    variables.VariablesMongoDb.count: number,
                    variables.VariablesMongoDb.stock_id: ObjectId(data.stock_id),
                    variables.VariablesMongoDb.is_consumer: consumer,
                    variables.VariablesMongoDb.update_history: [
                        {variables.VariablesMongoDb.update_at: datetime.datetime.now(),
                         variables.VariablesMongoDb.users: '',
                         variables.VariablesMongoDb.count: number,
                         variables.VariablesMongoDb.description: data.description,
                         variables.VariablesMongoDb.add: True}
                    ]

                }
            )

        response.Done = True
        response.Message = 'عملیات با موفقیت انجام شد'
        return response.dict()

    else:
        response.Done = False
        response.Message = 'کالایی با مشخصات وارد شده یافت نشد'
        return response.dict()
