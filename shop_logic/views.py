from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from .models import *
from .serializers import *

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields =['product']
    search_fields = ['category__slug', 'published_at']
    ordering_fields = ['published_at', 'title']