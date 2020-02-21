from django.urls import path
from . import views


urlpatterns = [
    path('', views.accountsHome, name="accountshome"),
    path('user/', views.userPage, name="user-page"),#customer
    # path('prouser/', views.prouserPage, name="prouser-page"),
    path('admin/', views.adminPage, name="admin-page"),
    path('accountsetting/', views.accountSettings, name="accountsetting"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
]