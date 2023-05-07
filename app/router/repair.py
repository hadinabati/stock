# from schema.user_schema import user_show
# from base import checking
import datetime
from fastapi import APIRouter
from database import mongodb as db
from schema import repair_schema as model
from instances import Mongo as variable
from bson import ObjectId

# from base.depency import basic_authenticate, Token, create_access_token, permissions


router = APIRouter()


@router.post('/create', response_model=model.SimpleResponse)
async def create(item: model.Create):
    response = model.SimpleResponse()

    count = db.stock_collection.count_documents(
        {
            variable.VariablesMongoDb.id: ObjectId(item.stock_id)
        }
    )
    if count > 0:

        data = item.dict()
        data[variable.VariablesMongoDb.is_updated] = False
        data[variable.VariablesMongoDb.update_history] = []
        data[variable.VariablesMongoDb.create_at] = datetime.datetime.now()
        data[variable.VariablesMongoDb.update_at] = datetime.datetime.now()

        res = db.repair_collection.insert_one(data)
        result = db.stock_collection.update_one(
            {
                variable.VariablesMongoDb.id: ObjectId(item.stock_id)
            },
            {
                "$push": {
                    variable.VariablesMongoDb.repair_history: res.inserted_id
                }
            }
        )

        if result.acknowledged:
            response.Done = True
            response.Message = 'گردش کار با موفقیت ثبت شد'

        else:
            response.Done = False
            response.Message = 'خطا در ثبت گردش کار'

        return response.dict()
    else:
        response.Done = False
        response.Message = 'کالایی با مشخصات وارد شده یافت نشده است'
        return response.dict()


@router.get('/list', response_model=model.ListItem)
async def all_list():
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
                u"from": u"activity",
                u"localField": u"activity_id",
                u"foreignField": u"_id",
                u"as": u"activity"
            }
        },
        {
            u"$lookup": {
                u"from": u"User",
                u"localField": u"id_of_creator",
                u"foreignField": u"_id",
                u"as": u"users"
            }
        }
    ]
    data = db.repair_collection.aggregate(pipeline=pipeline)
    final_list = []
    for item in data:
        epoch = model.Items()
        epoch.stock_id = item[variable.VariablesMongoDb.stock_id]
        epoch.stock_name = item[variable.VariablesMongoDb.stock][0][variable.VariablesMongoDb.name]
        epoch.description = item[variable.VariablesMongoDb.description]
        epoch.stock_updated = item[variable.VariablesMongoDb.stock_updated]
        epoch.properties = item[variable.VariablesMongoDb.properties]
        epoch.is_updated = item[variable.VariablesMongoDb.is_updated]
        epoch.create_at = item[variable.VariablesMongoDb.create_at]
        epoch.id_of_creator = item[variable.VariablesMongoDb.id_of_creator]
        epoch.updated_history = item[variable.VariablesMongoDb.update_history]
        epoch.name_of_creator = item[variable.VariablesMongoDb.users][0][variable.VariablesMongoDb.name]
        epoch.family_of_creator = item[variable.VariablesMongoDb.users][0][variable.VariablesMongoDb.family]
        epoch.id = item[variable.VariablesMongoDb.id]
        epoch.updated_at = item[variable.VariablesMongoDb.update_at]
        epoch.activity_name = item[variable.VariablesMongoDb.activity][0][variable.VariablesMongoDb.name]
        epoch.activity_id = item[variable.VariablesMongoDb.activity_id]

        final_list.append(epoch.dict())

    response = model.ListItem()
    response.data = final_list
    return response.dict()


@router.get('/list/stock/{id}', response_model=model.ListItem)
async def stock_repair_list(id: str):
    pipeline = [
        {
            u"$match": {
                u"stock_id": ObjectId(id)
            }
        },
        {
            u"$unwind": {
                u"path": u"$update_history"
            }
        },
        {
            u"$lookup": {
                u"from": u"activity",
                u"localField": u"update_history.activity_id",
                u"foreignField": u"_id",
                u"as": u"activity"
            }
        },
        {
            u"$unwind": {
                u"path": u"$activity"
            }
        },
        {
            u"$project": {
                u"name": u"$activity.name",
                u"update_history": u"$update_history",
                u"properties": u"$activity.properties",
                "update_at": "$update_at"
            }
        }
    ]
    data =list( db.repair_collection.aggregate(pipeline=pipeline))
    final_list = []
    for item in data:
        epoch = model.RepairListItem()
        epoch.name = item[variable.VariablesMongoDb.name]
        epoch.update_history = item[variable.VariablesMongoDb.update_history]
        epoch.activity_properties = item[variable.VariablesMongoDb.properties]
        epoch.update_at = item[variable.VariablesMongoDb.update_at]
        final_list.append(epoch.dict())

    response = model.ListItem()
    response.data = final_list
    return response.dict()


@router.get('/list/{person_id}', response_model=model.ListItem)
async def person_list(person_id: str):
    pipeline = [
        {
            u"$match": {
                u"id_of_creator": ObjectId(person_id)
            }
        },
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
                u"from": u"activity",
                u"localField": u"activity_id",
                u"foreignField": u"_id",
                u"as": u"activity"
            }
        },
        {
            u"$lookup": {
                u"from": u"User",
                u"localField": u"id_of_creator",
                u"foreignField": u"_id",
                u"as": u"users"
            }
        }
    ]

    data = db.repair_collection.aggregate(pipeline=pipeline)
    final_list = []
    for item in data:
        epoch = model.Items()
        epoch.stock_id = item[variable.VariablesMongoDb.stock_id]
        epoch.stock_name = item[variable.VariablesMongoDb.stock][0][variable.VariablesMongoDb.name]
        epoch.description = item[variable.VariablesMongoDb.description]
        epoch.stock_updated = item[variable.VariablesMongoDb.stock_updated]
        epoch.properties = item[variable.VariablesMongoDb.properties]
        epoch.is_updated = item[variable.VariablesMongoDb.is_updated]
        epoch.create_at = item[variable.VariablesMongoDb.create_at]
        epoch.id_of_creator = item[variable.VariablesMongoDb.id_of_creator]
        epoch.updated_history = item[variable.VariablesMongoDb.update_history]
        epoch.name_of_creator = item[variable.VariablesMongoDb.users][0][variable.VariablesMongoDb.name]
        epoch.family_of_creator = item[variable.VariablesMongoDb.users][0][variable.VariablesMongoDb.family]
        epoch.id = item[variable.VariablesMongoDb.id]
        epoch.updated_at = item[variable.VariablesMongoDb.update_at]
        epoch.activity_name = item[variable.VariablesMongoDb.activity][0][variable.VariablesMongoDb.name]
        epoch.activity_id = item[variable.VariablesMongoDb.activity_id]

        final_list.append(epoch.dict())

    response = model.ListItem()
    response.data = final_list
    return response.dict()


@router.put('/update', response_model=model.SimpleResponse)
async def update(item: model.Update):
    response = model.SimpleResponse()
    check = db.repair_collection.find_one(
        {
            variable.VariablesMongoDb.id: ObjectId(item.id)
        }
    )
    if check[variable.VariablesMongoDb.is_updated]:
        response.Done = False
        response.Message = 'گزارش فعالیت تنها یکبار می تواند تغییر کند'
        return response.dict()
    else:
        res1 = db.repair_collection.update_one(
            {
                variable.VariablesMongoDb.id: item.id
            },
            {
                "$set": {
                    variable.VariablesMongoDb.is_updated: True,
                    variable.VariablesMongoDb.description: item.description,
                    variable.VariablesMongoDb.properties: item.properties,
                    variable.VariablesMongoDb.activity_id: item.activity_id,
                }
            }
        )
        res2 = db.repair_collection.update_one(
            {
                variable.VariablesMongoDb.id: item.id
            },
            {
                "$push": {
                    variable.VariablesMongoDb.update_history: {
                        variable.VariablesMongoDb.description: check[variable.VariablesMongoDb.description],
                        variable.VariablesMongoDb.properties: check[variable.VariablesMongoDb.properties],
                        variable.VariablesMongoDb.activity_id: check[variable.VariablesMongoDb.activity_id],
                    }
                }
            }
        )
    if res1.matched_count + res2.matched_count > 1:
        response.Done = True
        response.Message = 'تغییرات با موفقیت انجام شد'
    else:
        response.Done = True
        response.Message = 'تغییرات با موفقیت انجام شد'

    return response.dict()
