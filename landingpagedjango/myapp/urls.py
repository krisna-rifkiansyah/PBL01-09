from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import log_everything_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profilesecure/<str:token>/', views.profile_secure, name='profile_secure'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('post/', views.post, name='post'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logs/', log_everything_view, name='log_everything'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)