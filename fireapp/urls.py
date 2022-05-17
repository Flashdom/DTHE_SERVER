from django.urls import path
from .views import (
    HomePage,
    UserData,
    MlUserData
)

urlpatterns = [
    path('', HomePage.as_view(), name='main-view'),
    path('<uid>/', MlUserData.as_view(), name='userdata-view'),
]
