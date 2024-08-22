from django.test import TestCase
from django.urls import reverse, resolve
from receitas import views
from receitas.models import Category, Recipe, User


class RecipeHomeViewTest(TestCase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 6}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):  
        view = resolve(reverse('recipes:receitas', kwargs={'id': 1}))
        self.assertIs(view.func, views.receitas)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'receitas/pages/home.html')