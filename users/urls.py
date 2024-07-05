from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('deposit/', views.deposit, name='deposit'),
    path('profile/', views.profileUser, name='profile'),
    path('update_profile/', views.updateProfileUser, name='update_profile'),
]
