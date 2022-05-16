from django.contrib import admin
from django.urls import path, include
from fireapp import views

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('fireapp.urls')),
]
