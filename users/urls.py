from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from users import views


app_name = "users"


urlpatterns = [
    path('', views.LoginUser.as_view(), name='home'),  # Main page
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileUser.as_view(), name='my_profile'),
    path('emplpfile/', views.ProfileEmpl.as_view(), name='emplpfile'),

    path('register/', views.RegisterUser.as_view(), name='register'),
 ]
