from typing import Optional
from pydantic import Field

from base.so_base import Model, ObjectId


class Create(Model):
    name: Optional[str]
    family: Optional[str]
    national_code: Optional[str]
    position_id: Optional[ObjectId]
    grade_id: Optional[ObjectId]
    role: Optional[ObjectId]


class Update(Model):
    id: Optional[ObjectId]
    name: Optional[str]
    family: Optional[str]
    national_code: Optional[str]
    position_id: Optional[ObjectId]
    grade_id: Optional[ObjectId]
    role: Optional[ObjectId]


class Delete(Model):
    id: Optional[ObjectId]


class Lists(Model):
    id: Optional[ObjectId]
    name: Optional[str]
    family: Optional[str]
    national_code: Optional[str]
    position_id: Optional[ObjectId]
    position_name: Optional[str]
    grade_name: Optional[str]
    grade_id: Optional[ObjectId]
    role: Optional[ObjectId]
    role_name :Optional[str]
    active: Optional[bool]
    update_history: Optional[list]


class SimpleResponse(Model):
    Done: Optional[bool]
    ErrorMassage: Optional[str]


class ResponseList(Model):
    Done: Optional[bool]
    data: Optional[list[Lists]]
    ErrorMassage: Optional[str] = Field(default='')
