from dataclasses import field
from rest_framework import serializers
from .models import MasterProduct, User
from .models import Seller


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProduct
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "user_type", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        field = "__all__"