from ninja import Router
from django.contrib.auth import authenticate
from django.http import HttpRequest
from .schemas import *

router = Router()

@router.post("/register")
def register(request: HttpRequest, data: UserCreate):
    if User.objects.filter(username=data.email).exists():
        return {"error": "Email ya registrado"}
    
    user = User.objects.create_user(
        username=data.email,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
        phone=data.phone
    )
    
    if data.role == 'producer' and data.farm_name:
        ProducerProfile.objects.create(
            user=user,
            farm_name=data.farm_name,
            farm_location=data.farm_location or ""
        )
    
    return {"id": user.id, "email": user.email, "role": user.role}

@router.post("/login")
def login(request: HttpRequest, data: LoginSchema):
    user = authenticate(username=data.email, password=data.password)
    if not user:
        return {"error": "Credenciales inválidas"}
    
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role
    }

@router.get("/me", auth=AuthBearer())
def me(request: HttpRequest):
    user = request.user
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "phone": user.phone
    }