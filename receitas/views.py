from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from . models import Recipe

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'receitas/pages/home.html', {'recipes': recipes},)

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id = category_id).order_by('-id')
    return render(request, 'receitas/pages/home.html', {'recipes': recipes },)

def receitas(request, id):
    recipe = Recipe.objects.get(id = id)
    return render(request, 'receitas/pages/receitas-views.html', {'recipe': recipe,
                                                                  'is_detail_page': True,
                                                                  })
    