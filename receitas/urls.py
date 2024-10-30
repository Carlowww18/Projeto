from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('receitas/search/', views.SearchListView.as_view(), name="search"),
    path('receitas/category/<int:category_id>/',
         views.CategoryListView.as_view(), name="category"),
    path('receitas/<int:pk>/', views.RecipeDetail.as_view(), name="receitas"),
    path('receitas/api/v1/', views.RecipeListViewHomeApi.as_view(), name="receitas_api_v1"),
    path('receitas/api/v1/<int:pk>', views.RecipeDetailApi.as_view(), name="receitas_api_v1_detail"),
    path('receitas/theory', views.theory, name="receitas_theory"),
]