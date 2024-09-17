from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'author/pages/register_view.html', {'form': form,
                                                               'form_action': reverse('authors:register_create')})

def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])

    else:
        messages.info(request, 'Corrija os campos inválidos')

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'author/pages/login_view.html', {'form': form,
                                                            'form_action': reverse('authors:login_create')})

def login_create(request):
    return render(request, 'author/pages/login_view.html')