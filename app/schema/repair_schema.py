import datetime
from typing import Optional
from base.so_base import ObjectId, Model


class Create(Model):
    id_of_creator: Optional[ObjectId]
    activity_id: Optional[ObjectId]
    description: Optional[str]
    stock_updated: Optional[bool]
    properties: Optional[list]
    stock_id: Optional[ObjectId]


class Update(Model):
    id: Optional[ObjectId]
    activity_id: Optional[ObjectId]
    description: Optional[str]
    properties: Optional[list]


class Items(Model):
    id: Optional[ObjectId]
    stock_id: Optional[ObjectId]
    stock_name: Optional[str]
    id_of_creator: Optional[ObjectId]
    name_of_creator: Optional[str]
    family_of_creator: Optional[str]
    activity_id: Optional[ObjectId]
    activity_name: Optional[str]
    description: Optional[str]
    stock_updated: Optional[bool]
    properties: Optional[list]
    is_updated: Optional[bool]
    updated_history: Optional[Create]
    create_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ListItem(Model):
    data: Optional[list]


class SimpleResponse(Model):
    Done: Optional[bool]
    Message: Optional[str]


class ItemRepairList(Model):
    activity_id: Optional[ObjectId]
    description: Optional[str]
    properties: Optional[list]


class RepairListItem(Model):
    name: Optional[str]
    update_history: Optional[ItemRepairList]
    activity_properties: Optional[list]
    update_at :Optional[datetime.datetime]
