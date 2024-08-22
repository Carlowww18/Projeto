from django.test import TestCase
from django.urls import reverse


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

    def test_recipe_search_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/receitas/search/')
