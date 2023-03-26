from typing import Optional

from base.so_base import ObjectId, Model


class HistoryItem(Model):
    date: Optional[str]
    request_id: Optional[ObjectId]
    result: Optional[str]
    token: Optional[str]
    description: Optional[str]


class Create(Model):
    name: Optional[str]
    is_consumer: Optional[bool]
    create_date: Optional[str]
    category_id: Optional[ObjectId]
    response_id: Optional[ObjectId]
    active: Optional[bool]
    repair_history: Optional[list[HistoryItem]]


class Update(Model):
    name: Optional[str]
    id: Optional[ObjectId]
    category_id: Optional[ObjectId]
    response_id: Optional[ObjectId]
    active: Optional[bool]


class Response(Model):
    Done: Optional[bool]
    Message: Optional[str]


class Delete(Model):
    id: Optional[ObjectId]
    active: Optional[bool]


class Item(Model):
    name: Optional[str]
    is_consumer: Optional[bool]
    create_date: Optional[str]
    category_id: Optional[ObjectId]
    response_id: Optional[ObjectId]
    active: Optional[bool]
    repair_history: Optional[list]
    id: Optional[ObjectId]


class Lists(Model):
    items :Optional[Item]