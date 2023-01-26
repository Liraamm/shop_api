from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly, permissions, IsAdminAuthPermission, IsAuthorPermission
from .serializers import ProductSerializer, CommentSerializer, RatingSerializer
from rest_framework import permissions

from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update',
        'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
            
        return super().get_permissions()


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


    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST', 'PATCH'], detail=True)
    def rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rating = Rating.objects.filter(author=request.user, post=pk).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'post':
                return Response('use PATCH method')
            elif rating and request.method == 'PATCH':
                serializer.create(serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response('rating saved')

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
            if not like.is_liked:
                like.delete()
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user, is_liked=True)
            message='liked'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()
