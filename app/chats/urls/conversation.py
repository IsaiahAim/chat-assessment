from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import ConversationViewset


app_name = "conversation"
router = DefaultRouter()
router.register("", ConversationViewset)

urlpatterns = [
    path("", include(router.urls))
]