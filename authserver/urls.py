from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('jwt_auth.urls')),
    path('admin/', admin.site.urls)
]
