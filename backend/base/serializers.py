from django.forms import model_to_dict
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import Product, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        product_data = model_to_dict(self.instance)
        if 'selling_price' in data and 'purchase_price' in data:
            if data['selling_price'] < data['purchase_price']:
                raise serializers.ValidationError("selling price must be greater than purchasing price")
        elif 'selling_price' in data:
            if data['selling_price'] < product_data['purchase_price']:
                raise serializers.ValidationError("selling price must be greater than purchasing price")
        elif 'purchase_price' in data:
            if data['purchase_price'] > product_data['selling_price']:
                raise serializers.ValidationError("selling price must be greater than purchasing price")
        return data


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ['id', '_id', 'name', 'username', 'email']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

    def get__id(self, obj):
        return obj.id



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'name', 'username', 'email', 'token', 'is_staff']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
