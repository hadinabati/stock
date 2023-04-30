import datetime
from typing import Optional
from base.so_base import ObjectId, Model


class CreateSample(Model):
    name: Optional[str]
    properties: Optional[list]
    category_id :Optional[ObjectId]


class ListItem(Model):
    id: Optional[ObjectId]
    name: Optional[str]
    properties: Optional[list]
    create_date: Optional[datetime.datetime]
    active: Optional[bool]
    category_id :Optional[ObjectId]


class SimpleResponse(Model):
    Done: Optional[bool]
    Message: Optional[str]


class Deactivated(Model):
    id: Optional[ObjectId]


class ResponseList(Model):
    data : Optional[list[ListItem]]