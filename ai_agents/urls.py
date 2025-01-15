from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to manually trigger AI comment generation for a post
path('generate-comment/', views.generate_comment, name='generate_comment'),
]
