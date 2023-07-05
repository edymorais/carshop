from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carshop import settings
from products.api.viewsets import ProductViewSet, SpecificationsViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('specifications', SpecificationsViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
