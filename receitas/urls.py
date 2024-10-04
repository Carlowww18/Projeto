from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('receitas/search/', views.search, name="search"),
    path('receitas/category/<int:category_id>/',
         views.CategoryViewBase.as_view(), name="category"),
    path('receitas/<int:id>/', views.receitas, name="receitas"),
]