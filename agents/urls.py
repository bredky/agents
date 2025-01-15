from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('signin')),  # Default redirect to 'signin'
    path('users/', include('users.urls')),  # User-related routes
    path('', include('posts.urls')),  # Add the posts app URLs
    path('ai-agents/', include('ai_agents.urls')),
]
