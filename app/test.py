from typing import Optional
from base.so_base import ObjectId, Model
from pydantic import Field


class Test(Model):
    name: Optional[bool] = Field(default='name')


item = Test()
print(item.name)