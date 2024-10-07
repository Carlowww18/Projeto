from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('receitas/search/', views.SearchListView.as_view(), name="search"),
    path('receitas/category/<int:category_id>/',
         views.CategoryListView.as_view(), name="category"),
    path('receitas/<int:pk>/', views.RecipeDetail.as_view(), name="receitas"),
]