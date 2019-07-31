from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'datamanager'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='datamanager/login.html'), name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:username>/newdata/', views.newdata, name='newdata'),
    path('datalist/', views.datalist, name='datalist'),
    path('recommandation', views.recommandation, name='recommandation'),
    path('<int:geoid>/', views.detail, name='detail'),
    path('google/', views.google, name='google'),
    path('heat/', views.heat, name='heat'),
    path('<int:geoid>/deleteComment/<str:context>', views.deleteComment, name='deleteComment'),
    path('search', views.search, name='search'),
]