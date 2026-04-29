from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.utils import timezone








urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('alan',views.alan,name='alan'),
    path('profile/update/', views.update_profile, name="update_profile"),
    path('emergency-contact/add/', views.yakin_ekle, name="yakin_ekle"),
    path('category/<category>/', views.getPathByCategory, name='category_by_name'),
    path('delete-contact/<int:contact_id>/', views.delete_emergency_contact, name='delete_contact'),
    path('send-safe-email/', views.send_safe_email, name='send_safe_email'),
    path('send-emergency-email/', views.send_emergency_email, name='send_emergency_email'),
    path('destek/', views.destek, name='destek'),
]








