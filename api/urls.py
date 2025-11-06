from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api import views
from .views import SellerViewSet, register_view, login_view, logout

# DRF Router for viewsets
router = DefaultRouter()
router.register(r'sellers', SellerViewSet, basename='seller')

app_name = 'api'

urlpatterns = [
    # ---------- API ViewSets ----------
    path('', include(router.urls)),

    # ---------- Auth Views ----------
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),

    # ---------- JWT Authentication ----------
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
