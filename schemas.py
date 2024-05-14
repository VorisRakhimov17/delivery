from pydantic import BaseModel
from typing import Optional


class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "shoxrux13",
                "email": "woxrux6070@gmail.com",
                "password": "woxrux6070",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '50dd57077f52731f41c8ebbb53620f0de23b92a089b3bef96de3aafc6641d35e'


class LoginModel(BaseModel):
    username_or_email: str
    password: str

