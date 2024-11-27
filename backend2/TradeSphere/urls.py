from django.urls import path
from .views import home, register_user, login_user, get_user_details

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('user/', get_user_details, name='user_details'),
]
