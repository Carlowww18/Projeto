from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from . utils.receitas.factory import make_recipe

def home(request):
    return render(request, 'receitas/pages/home.html', {'recipes': [make_recipe() for _ in range(3)]},)

def receitas(request, id):
    return render(request, 'receitas/pages/receitas-views.html', {'recipe': make_recipe(),
                                                                  'is_detail_page': True,
                                                                  })
