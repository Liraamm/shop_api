from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly, IsStaffOrTargetUser, permissions

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

class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrdersSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)