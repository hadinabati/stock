from typing import Optional

from base.so_base import ObjectId, Model


class Create(Model):
    name: Optional[str]
    description: Optional[str]


class Items(Model):
    name: Optional[str]
    description: Optional[str]
    id: Optional[ObjectId]


class Lists(Model):
    item: Optional[list[Items]]


class Response(Model):
    Done: Optional[bool]
    Message: Optional[str]
