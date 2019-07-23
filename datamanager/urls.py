from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'datamanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='datamanager/login.html'), name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:geoid>/', views.detail, name='detail'),
    path('<int:geoid>/results/', views.results, name='results'),
]