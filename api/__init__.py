from ninja import NinjaAPI
from users.api import router as users_router
from products.api import router as products_router
from orders.api import router as orders_router

api = NinjaAPI()

api.add_router("/users", users_router)
api.add_router("/products", products_router)
api.add_router("/orders", orders_router)

@api.get("/health")
def health(request):
    return {"status": "ok", "service": "ProdMarket API"}