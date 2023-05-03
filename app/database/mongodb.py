import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
database = myclient["fava"]
User_collection = database["User"]
grade_collection = database['Grade']
position_collection = database['Position']
stock_collection = database['Stock']
category_collection = database['Category']
route_collection = database['routes']
roles_collection = database['roles']
activity_collection = database['activity']
repair_collection  = database['repair']
crash_collection  = database['crash']


