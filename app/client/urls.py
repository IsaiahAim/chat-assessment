from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewset


app_name = "clients"
router = DefaultRouter()
router.register("", ClientViewset)

urlpatterns = [
    path("", include(router.urls))
]