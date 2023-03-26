from typing import Optional, List

from pydantic import BaseModel, Field

from base.so_base import ObjectId


class user_show(BaseModel):
    id: Optional[ObjectId] = Field()
    username: str
    role: Optional[List[str]]


class Credentials(BaseModel):
    username: str
    password: str


class LoginSchema(BaseModel):
    username: str = Field(default='str', description='username')
    passwords: str = Field(default='str', description='the passwords')


class Profile(BaseModel):
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


class Show(BaseModel):
    username: Optional[str] = Field()
    profile: Profile
    Error: Optional[bool] = False
    rele: Optional[List[str]]
    create_at: Optional[str]
    create_at: Optional[str]
