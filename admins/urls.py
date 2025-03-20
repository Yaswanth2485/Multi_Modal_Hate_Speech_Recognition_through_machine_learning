from django.urls import path
from . import views


urlpatterns = [
    path('AdminLogin/',views.AdminLogin, name='AdminLogin'),
    path("AdminLoginCheck/", views.AdminLoginCheck, name="AdminLoginCheck"),
    path("AdminHome/", views.AdminHome, name="AdminHome"),
    path('RegisterUsersView/', views.RegisterUsersView, name='RegisterUsersView'),
    path('activate_user/',views.activate_user,name = 'activate_user'),
    path('BlockUser/', views.BlockUser, name='BlockUser'),
    path('UnblockUser-user/', views.UnblockUser, name='UnblockUser'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),

   
  



   
]