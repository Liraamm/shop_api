from rest_framework import serializers
from .models import *

class CategorySerializer(serializers. ModelSerializer):
    class Meta:
        model = Category
        fields  = ('title',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title',)

class OrdersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Orders
        fields = '__all__'
