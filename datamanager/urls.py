from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:geoid>/', views.detail, name='detail'),
    path('<int:geoid>/results/', views.results, name='results'),
]