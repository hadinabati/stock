from typing import Optional

from base.so_base import Model, ObjectId


class Response(Model):
    Done: Optional[bool]
    ErrorMessage: Optional[str]


class List(Model):
    id: Optional[ObjectId]
    address: Optional[str]
    TagName: Optional[str]
    summary: Optional[str]


class ListResponse(Model):
    data: Optional[list[List]]
