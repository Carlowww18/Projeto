from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('receitas/<int:id>/', views.receitas, name="receitas"),
]