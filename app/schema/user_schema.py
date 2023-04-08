from typing import Optional, List

from pydantic import  Field

from base.so_base import ObjectId ,Model


class user_show(Model):
    id: Optional[ObjectId] = Field()
    username: str
    role: Optional[List[str]]


class Credentials(Model):
    username: str
    password: str


class LoginSchema(Model):
    username: str = Field(default='str', description='username')
    passwords: str = Field(default='str', description='the passwords')


class Profile(Model):
    name: Optional[str] = Field(default='name')
    fname : Optional[str] = Field(default='name')
    username: Optional[str] = Field(default='username')
    passwords: Optional[str] = Field(default='password')
    national_code: Optional[str] = Field(default='national_code')
    grade: Optional[ObjectId] = Field(default='grade')
    position: Optional[ObjectId] = Field(default=' the position of job')
    describe: Optional[str] = Field(default='name')


class Register(LoginSchema):
    profile: Optional[Profile]
    role: List[ObjectId]


class Show(Model):
    username: Optional[str] = Field()
    profile: Profile
    Error: Optional[bool] = False
    rele: Optional[List[str]]
    create_at: Optional[str]
    create_at: Optional[str]

class Response(Model):
    Done: Optional[bool]
    ErrorMessage: Optional[str]
