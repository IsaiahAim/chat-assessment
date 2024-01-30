from .import views
from django.urls import path


urlpatterns = [
    path('register', views.create_user, name="create_user"),
    path('login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name="user_logout"),
    path('chat', views.chat_view, name="chat_view"),
]
