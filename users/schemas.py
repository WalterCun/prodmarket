from ninja import Schema
from typing import Optional
from pydantic import EmailStr

class UserCreate(Schema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = 'consumer'
    phone: Optional[str] = None
    farm_name: Optional[str] = None
    farm_location: Optional[str] = None

class LoginSchema(Schema):
    email: EmailStr
    password: str

class AuthBearer(Schema):
    pass