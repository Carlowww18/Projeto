from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'receitas/pages/home.html', {'name': 'André'})
