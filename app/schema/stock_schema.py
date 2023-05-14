import datetime
from typing import Optional

from pydantic import Field

from base.so_base import ObjectId, Model


class HistoryItem(Model):
    date: Optional[str]
    request_id: Optional[ObjectId]
    result: Optional[str]
    token: Optional[str]
    description: Optional[str]


class Create(Model):
    name: Optional[str] = Field(default='name')
    is_consumer: Optional[bool]
    category_id: Optional[str]
    response_id: Optional[str]
    position_id: Optional[str]
    has_response: Optional[bool]
    stock_number: Optional[int]
    info: Optional[list]

    count :Optional[int]



class Update(Model):
    name: Optional[str]
    is_consumer: Optional[bool]
    id: Optional[ObjectId]
    category_id: Optional[str]
    response_id: Optional[str]
    active: Optional[bool]
    position_id: Optional[str]
    has_response: Optional[bool]
    stock_number: Optional[int]
    info: Optional[list]
    old_stock_number: Optional[int]
    count :Optional[int]


class Response(Model):
    Done: Optional[bool]
    Message: Optional[str]


class Delete(Model):
    id: Optional[ObjectId]
    active: Optional[bool]


class Item(Model):
    name: Optional[str]
    is_consumer: Optional[bool]
    create_date: Optional[datetime.datetime]
    category_id: Optional[ObjectId]
    category_name: Optional[str]
    response_id: Optional[ObjectId]
    response_name: Optional[str]
    active: Optional[bool]
    repair_history: Optional[list]
    position_id: Optional[ObjectId]
    position_name: Optional[str]
    has_response: Optional[bool]
    stock_number: Optional[int]
    id: Optional[ObjectId]
    info: Optional[list]
    update_history: Optional[list]
    count: Optional[int]
    properties: Optional[list]


class Lists(Model):
    items: Optional[list[Item]]


class CrashItem(Model):
    id: Optional[ObjectId]
    stock_id :Optional[ObjectId]
    name: Optional[str]
    Count: Optional[int]
    is_consumer: Optional[bool]
    update_history: Optional[list]
    response_name: Optional[str]
    position_name: Optional[str]
    response_id: Optional[ObjectId]
    position_id: Optional[ObjectId]


class CrashList(Model):
    items: Optional[list[CrashItem]]


class Accession(Model):
    number: Optional[int]
    stock_id: Optional[ObjectId] = Field(description='کالایی که باید الحاق شود')
    accession_number: Optional[ObjectId] = Field(description='ایدی کالایی که کالای الحاق شده به ان می باشد')


class Crash(Model):
    stock_id: Optional[ObjectId]
    number: Optional[int]



class AddStock(Model):
    stock_id: Optional[ObjectId]
    number: Optional[int]


class AddOrDeleteAccession(Model):
    add: Optional[bool]
    number: Optional[int]
    stock_id: Optional[ObjectId] = Field(description='کالایی که باید الحاق شود')
    accession_number: Optional[ObjectId] = Field(description='ایدی کالایی که کالای الحاق شده به ان می باشد')


class ConsumerListItem(Model):
    id :Optional[ObjectId]
    active : Optional[bool]
    name :Optional[str]
    serial :Optional[int]
    stock_number :Optional[int]
    use_number: Optional[int]
    crash_number: Optional[int]
    total_number: Optional[int]


class ConsumerList(Model):
    items :Optional[list[ConsumerListItem]]