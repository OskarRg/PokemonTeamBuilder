from django.urls import path
from .views import UserLoginAPIView, UserLogoutAPIView, UserCreateAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('signup/', UserCreateAPIView.as_view(), name='signup'),
]
