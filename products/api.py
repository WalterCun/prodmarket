from ninja import Router, Schema
from django.http import HttpRequest
from typing import List, Optional
from pydantic import Field
from products.models import Product, Category
from users.api import AuthBearer

router = Router()

class CategorySchema(Schema):
    id: int
    name: str
    description: Optional[str]

class ProductIn(Schema):
    name: str
    description: str
    product_type: str
    category_id: Optional[int] = None
    unit: str
    price_per_unit: float
    quantity_available: float
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ProductOut(Schema):
    id: int
    producer_id: int
    producer_name: str
    category_id: Optional[int]
    name: str
    description: str
    product_type: str
    unit: str
    price_per_unit: float
    quantity_available: float
    location: str
    status: str
    created_at: str
    
    @staticmethod
    def from_entity(p: Product):
        return ProductOut(
            id=p.id,
            producer_id=p.producer.id,
            producer_name=p.producer.get_full_name(),
            category_id=p.category_id,
            name=p.name,
            description=p.description,
            product_type=p.product_type,
            unit=p.unit,
            price_per_unit=float(p.price_per_unit),
            quantity_available=float(p.quantity_available),
            location=p.location,
            status=p.status,
            created_at=p.created_at.isoformat()
        )

@router.get("/categories", response=List[CategorySchema])
def list_categories(request: HttpRequest):
    return Category.objects.all()

@router.get("/", response=List[ProductOut])
def list_products(
    request: HttpRequest,
    product_type: Optional[str] = None,
    category_id: Optional[int] = None,
    status: str = 'available'
):
    products = Product.objects.filter(status=status)
    if product_type:
        products = products.filter(product_type=product_type)
    if category_id:
        products = products.filter(category_id=category_id)
    return [ProductOut.from_entity(p) for p in products]

@router.get("/{product_id}", response=ProductOut)
def get_product(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id)
    return ProductOut.from_entity(product)

@router.post("/", response=ProductOut, auth=AuthBearer())
def create_product(request: HttpRequest, data: ProductIn):
    if request.user.role != 'producer':
        return {"error": "Solo productores pueden crear productos"}
    
    product = Product.objects.create(
        producer=request.user,
        category_id=data.category_id,
        name=data.name,
        description=data.description,
        product_type=data.product_type,
        unit=data.unit,
        price_per_unit=data.price_per_unit,
        quantity_available=data.quantity_available,
        location=data.location,
        latitude=data.latitude,
        longitude=data.longitude
    )
    return ProductOut.from_entity(product)

@router.put("/{product_id}", response=ProductOut, auth=AuthBearer())
def update_product(request: HttpRequest, product_id: int, data: ProductIn):
    product = Product.objects.get(id=product_id, producer=request.user)
    
    for field in ['name', 'description', 'product_type', 'category_id', 'unit', 
                  'price_per_unit', 'quantity_available', 'location', 'latitude', 'longitude']:
        setattr(product, field, getattr(data, field))
    
    product.save()
    return ProductOut.from_entity(product)

@router.delete("/{product_id}", auth=AuthBearer())
def delete_product(request: HttpRequest, product_id: int):
    product = Product.objects.get(id=product_id, producer=request.user)
    product.delete()
    return {"success": True}

@router.get("/my-products", response=List[ProductOut], auth=AuthBearer())
def my_products(request: HttpRequest):
    products = Product.objects.filter(producer=request.user)
    return [ProductOut.from_entity(p) for p in products]