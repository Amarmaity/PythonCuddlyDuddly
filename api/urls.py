from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
# router.register(r'products', ProductViewSet)


app_name = 'api'



urlpatterns = [
    path('', include(router.urls)),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    #  path("home/", home_view, name="home"),
]
