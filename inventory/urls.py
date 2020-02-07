from django.urls import path, include
from rest_framework import routers
from inventory.views import ProductViewSet


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
