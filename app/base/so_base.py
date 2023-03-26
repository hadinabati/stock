from bson.errors import InvalidId
from pydantic import BaseModel, BaseConfig
from bson import ObjectId as BaseObjectId


class Model(BaseModel):
    """Inherited model from pydantic basemodel for custom validations."""

    class Config(BaseConfig):
        """Convert datetime and ObjectId to json readable values."""
        json_encoders = {
            BaseObjectId: str,
        }


class ObjectId(str):
    """Creating a ObjectId class for pydantic models."""

    @classmethod
    def validate(cls, value):
        """Validate given str value to check if good for being ObjectId."""
        try:
            return BaseObjectId(str(value))
        except InvalidId as e:
            raise ValueError("Not a valid ObjectId") from e

    @classmethod
    def __get_validators__(cls):
        yield cls.validate