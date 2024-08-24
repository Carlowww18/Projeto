from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from receitas.utils.pagination import make_pagination_range
from . models import Recipe

def home(request):
    recipes = Recipe.objects.all().order_by('-id')


    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 6)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )


    return render(request, 'receitas/pages/home.html', {
        'recipes': page_obj, 
        'pagination_range': pagination_range
    })

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