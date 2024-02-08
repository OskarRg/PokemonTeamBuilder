from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('team-builder/', include('team_builder.urls')),
    path('comments/', include('comments.urls')),
]
