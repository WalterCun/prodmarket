from ninja import Router, Schema
from django.http import HttpRequest
from typing import List, Optional
from decimal import Decimal
from orders.models import Order
from products.models import Product
from users.api import AuthBearer

router = Router()

class OrderIn(Schema):
    product_id: int
    quantity: float
    delivery_address: str
    delivery_notes: Optional[str] = None

class OrderOut(Schema):
    id: int
    consumer_id: int
    consumer_name: str
    product_id: int
    product_name: str
    quantity: float
    unit_price: float
    subtotal: float
    commission_amount: float
    total: float
    delivery_address: str
    status: str
    created_at: str
    
    @staticmethod
    def from_entity(o: Order):
        return OrderOut(
            id=o.id,
            consumer_id=o.consumer.id,
            consumer_name=o.consumer.get_full_name(),
            product_id=o.product.id,
            product_name=o.product.name,
            quantity=float(o.quantity),
            unit_price=float(o.unit_price),
            subtotal=float(o.subtotal),
            commission_amount=float(o.commission_amount),
            total=float(o.total),
            delivery_address=o.delivery_address,
            status=o.status,
            created_at=o.created_at.isoformat()
        )

@router.post("/", response=OrderOut, auth=AuthBearer())
def create_order(request: HttpRequest, data: OrderIn):
    product = Product.objects.get(id=data.product_id)
    
    if product.quantity_available < data.quantity:
        return {"error": "Cantidad no disponible"}
    
    order = Order(
        consumer=request.user,
        product=product,
        quantity=data.quantity,
        unit_price=product.price_per_unit,
        delivery_address=data.delivery_address,
        delivery_notes=data.delivery_notes or ""
    )
    order.calculate_totals()
    order.save()
    
    # Reserve quantity
    product.quantity_available -= data.quantity
    product.save()
    
    return OrderOut.from_entity(order)

@router.get("/", response=List[OrderOut], auth=AuthBearer())
def list_orders(request: HttpRequest, status: Optional[str] = None):
    orders = Order.objects.filter(consumer=request.user)
    if status:
        orders = orders.filter(status=status)
    return [OrderOut.from_entity(o) for o in orders]

@router.get("/as-producer", response=List[OrderOut], auth=AuthBearer())
def producer_orders(request: HttpRequest, status: Optional[str] = None):
    orders = Order.objects.filter(product__producer=request.user)
    if status:
        orders = orders.filter(status=status)
    return [OrderOut.from_entity(o) for o in orders]

@router.get("/{order_id}", response=OrderOut, auth=AuthBearer())
def get_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(id=order_id)
    return OrderOut.from_entity(order)

@router.post("/{order_id}/confirm", auth=AuthBearer())
def confirm_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(id=order_id, product__producer=request.user)
    order.status = 'confirmed'
    order.save()
    return {"success": True, "status": order.status}

@router.post("/{order_id}/cancel", auth=AuthBearer())
def cancel_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(id=order_id, consumer=request.user)
    if order.status not in ['pending', 'confirmed']:
        return {"error": "No se puede cancelar"}
    
    # Return quantity to product
    product = order.product
    product.quantity_available += order.quantity
    product.save()
    
    order.status = 'cancelled'
    order.save()
    return {"success": True, "status": order.status}

@router.get("/stats/summary", auth=AuthBearer())
def order_stats(request: HttpRequest):
    user = request.user
    
    # Consumer stats
    consumer_orders = Order.objects.filter(consumer=user)
    consumer_total = sum(float(o.total) for o in consumer_orders)
    
    # Producer stats
    producer_orders = Order.objects.filter(product__producer=user)
    producer_total = sum(float(o.subtotal) for o in producer_orders)
    producer_commission = sum(float(o.commission_amount) for o in producer_orders)
    
    return {
        "as_consumer": {
            "total_orders": consumer_orders.count(),
            "total_spent": consumer_total
        },
        "as_producer": {
            "total_orders": producer_orders.count(),
            "total_sales": producer_total,
            "commission_paid": producer_commission
        }
    }