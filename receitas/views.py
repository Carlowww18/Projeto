from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
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
def search(request):

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(title__icontains = search_term) |
        Q(description__icontains = search_term),
    ).order_by('-id')
    
    return render(request, 'receitas/pages/search.html', {'page_title': f'Search for "{search_term}" | Recipes',
                                                          'recipes': recipes,
                                                          })