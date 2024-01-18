from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('project/', include('project_management.urls')),
    path('user/', include('user.urls')),
    path('database/', include('database.urls')),
]