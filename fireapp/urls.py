from django.urls import path
from .views import (
    HomePage,
    UserData,
)

urlpatterns = [
    path('', HomePage.as_view(), name='main-view'),
    path('<uid>/', UserData.as_view(), name='userdata-view'),
]
