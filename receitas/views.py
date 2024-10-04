import os
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from receitas.utils.pagination import make_pagination
from . models import Recipe, Category
from django.contrib import messages
from django.views.generic import ListView


PER_PAGE = os.environ.get('PER_PAGE', 6)

class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'receitas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
       qs = super().get_queryset(*args, **kwargs)
       qs = qs.filter(
           is_published = True
       )

       return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})

        return ctx
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'receitas/pages/home.html'

class CategoryViewBase(ListView):
    model = Category, Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'receitas/pages/category.html'

    def get_category(self, category_id):
        recipes = Recipe.objects.filter(category__id = category_id)

        return recipes

    def get_queryset(self, recipes):
       qs = super().get_queryset(recipes)
       qs = qs.filter(     
           id=self.get_category(recipes),
       )
       return qs #ARRUMAR ESSA MERDA DE VIEWS
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({'recipes': page_obj,
                    'pagination_range': pagination_range,
                    })

        return ctx

def home(request):
    recipes = Recipe.objects.all().order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'receitas/pages/home.html', {
        'recipes': page_obj, 
        'pagination_range': pagination_range,
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id = category_id).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'receitas/pages/category.html', {
        'recipes': page_obj, 
        'pagination_range': pagination_range,
        'tile': f'{recipes[0].category.name} - Category |'
    })   

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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    
    return render(request, 'receitas/pages/search.html', {'page_title': f'Search for "{search_term}" | Recipes',
                                                          'search_term': search_term,
                                                          'recipes': page_obj,
                                                          'pagination_range': pagination_range,
                                                          'additional_url_query':f'&q={search_term}' 
                                                          })