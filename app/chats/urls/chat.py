from django.urls import path
from ..views import ConversationView

app_name = "chat"

urlpatterns = [
    path("", ConversationView.as_view())
]
