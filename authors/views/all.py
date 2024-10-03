from django.shortcuts import render, redirect
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from receitas.models import Recipe


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
        return redirect(reverse('authors:login'))

    else:
        messages.info(request, 'Corrija os campos inválidos')

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'author/pages/login_view.html', {'form': form,
                                                            'form_action': reverse('authors:login_create')})

def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    
    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Error to validate form data')

    return redirect(reverse('authors:dashboard'))  

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
        )
    return render(request, 'author/pages/dashboard.html', {'recipes': recipes})
