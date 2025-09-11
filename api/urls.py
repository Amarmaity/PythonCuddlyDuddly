from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, register_view, login_view

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    #  path("home/", home_view, name="home"),
]
