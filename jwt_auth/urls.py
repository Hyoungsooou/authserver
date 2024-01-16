from django.urls import path
# ninja
from ninja import NinjaAPI
from jwt_auth.router.auth import router as jwt_router
# auth
api = NinjaAPI()

api.add_router('', jwt_router, tags=['auth'])


urlpatterns = [
    path('auth/', api.urls),
]
