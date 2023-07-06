from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api.viewsets import ProductViewSet, SpecificationsListViewSet, SpecificationsCategoriesViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/specifications/', SpecificationsListViewSet.as_view(), name='specifications'),
    path('api/categories-specifications/', SpecificationsCategoriesViewSet.as_view(), name='categories-specifications'),
]
