from typing import Optional

from pydantic import Field

from base.so_base import ObjectId, Model
from schema.routes_schema import List as model_route


class Create(Model):
    name: Optional[str]
    items: Optional[list[ObjectId]]


class Update(Model):
    id: Optional[ObjectId]
    name: Optional[ObjectId]
    items: Optional[list]


class Change(Model):
    id: Optional[ObjectId]



class Response(Model):
    Done: Optional[bool]
    ErrorMessage: Optional[str]


class Lists(Model):
    id: Optional[ObjectId]
    name: Optional[str]
    items: Optional[list]
    active: Optional[bool]


class ResponseList(Model):
    data: Optional[list[Lists]]


class ResponseId(Model):
    name: Optional[str] = Field(default='')
    active: Optional[bool] = Field(default=None)
    items: Optional[list[model_route]]


