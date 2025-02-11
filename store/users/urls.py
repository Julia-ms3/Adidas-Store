from django.urls import path
from users.views import UserLoginView, UserRegistrationView, UserProfileView, logout, EmailVerificationView


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/',UserRegistrationView.as_view() , name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('verification/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name = 'verification') #???
]
