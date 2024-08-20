from django.test import TestCase
from django.urls import reverse, resolve
from receitas import views

class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_category_home_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 6})
        self.assertEqual(url, '/receitas/category/6/')

    def test_receita_home_url_is_correct(self):
        url = reverse('recipes:receitas', kwargs={'id': 1})
        self.assertEqual(url, '/receitas/1/')

class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 6}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):  
        view = resolve(reverse('recipes:receitas', kwargs={'id': 1}))
        self.assertIs(view.func, views.receitas)
