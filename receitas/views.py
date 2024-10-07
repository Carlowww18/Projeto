import os
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from receitas.utils.pagination import make_pagination
from . models import Recipe, Category
from django.contrib import messages
from django.views.generic import ListView, DetailView


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

class CategoryListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'receitas/pages/category.html'

    def get_queryset(self, *args, **kwargs):
       qs = super().get_queryset(*args, **kwargs)
       category_id = self.kwargs.get('category_id')

       if category_id:
            qs = qs.filter(     
               category__id=category_id
            )
       return qs 
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({'recipes': page_obj,
                    'pagination_range': pagination_range,
                    })

        return ctx
    
class CategoryListView(CategoryListViewBase):
    template_name = 'receitas/pages/category.html'


class SearchListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'receitas/pages/search.html'

    def get_queryset(self, *args, **kwargs):
       qs = super().get_queryset(*args, **kwargs)
       search_term = self.request.GET.get('q', '').strip()

       if not search_term:
           raise Http404()

       qs = Recipe.objects.filter(
        Q(title__icontains = search_term) |
        Q(description__icontains = search_term),
        )

       return qs 
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        ctx.update({'page_title': f'Search for "{search_term}" | Recipes',
                                                          'search_term': search_term,
                                                          'additional_url_query':f'&q={search_term}' 
                                                          })

        return ctx
    

class SearchListView(SearchListViewBase):    
    template_name = 'receitas/pages/search.html'   


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'receitas/pages/receitas-views.html'