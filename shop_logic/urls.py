from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('category',CategoryViewSet)
router.register('article', ArticleViewSet)
router.register('orders', OrdersViewSet)

urlpatterns = [
    path('', include(router.urls))
]