#bots/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_bot/', views.create_bot, name='create_bot'),
    path('chat/', views.chat_api, name='chat_api'),
    path('ask/', views.ask_api, name='ask_api'),
    path('delete_bots/', views.delete_bots, name='delete_bots'),
    
]
