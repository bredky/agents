from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to manually trigger AI comment generation for a post
path('generate-comment/', views.generate_comment, name='generate_comment'),
path('create-bot/', views.create_bot, name='create_bot'),
path('my-bots/', views.bot_list, name='bot_list'),
]
