from django.urls import path
from .import views






urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('logout', views.user_logout, name='user_logout'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('verify-info/',views.email_verification_info, name='email_verification_info'),
 
 
 

]








