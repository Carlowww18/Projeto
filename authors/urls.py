from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view , name="register"),
    path('register/create/', views.register_create , name="register_create"),
    path('login/', views.login_view , name="login"),
    path('login/create/', views.login_create, name="login_create"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/recipe/create/',views.dashboard_recipe.as_view(), name="recipe_new"),
    path('dashboard/recipe/delete/',  views.dashboard_recipe.as_view(), name="dashboard_recipe_delete"),
    path('dashboard/recipe/<int:id>/edit/', views.dashboard_recipe.as_view(), name="dashboard_recipe_edit"),
]