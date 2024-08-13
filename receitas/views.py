from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'receitas/home.html', {'name': 'André'})

def sobre(request):
    return HttpResponse('sobre')

def contato(request):
    return HttpResponse('contato')
