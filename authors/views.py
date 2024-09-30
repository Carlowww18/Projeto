from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, AuthorRecipeForm
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

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        id=id
        ).first()
    
    if not recipe:
        raise Http404()
    form = AuthorRecipeForm(
        request.POST or None,
        request.FILES or None,
        instance=recipe,
        )
    
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'author/pages/dashboard_recipe.html', {'recipe': recipe,
                                                                  'form': form})


@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_new(request):
    if request.method == 'POST':
        form = AuthorRecipeForm(request.POST, request.FILES)

        title = request.POST.get('title')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        servings = request.POST.get('servings')


        if title == description:
            messages.error(request, 'O título e a descrição não podem ser iguais')
            return redirect(reverse('authors:recipe_new'))  
        if len(title) <= 3:
            messages.error(request, 'O título não pode ter menos que 5 caracteres')
            return redirect(reverse('authors:recipe_new'))  
        if int(preparation_time) < 0 or int(servings) < 0:
            messages.error(request, 'Números negativos  não são permitidos')
            return redirect(reverse('authors:recipe_new'))  
        else: 
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                messages.success(request, 'Nova receita cadastrada com sucesso')
                return redirect(reverse('authors:recipe_new'))  
    else:
        form = AuthorRecipeForm()

    return render(request, 'author/pages/dashboard_recipe.html', {'form': form})

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        id=id
        ).first()
    
    if not recipe:
        raise Http404()
    recipe.delete()
    messages.success(request, 'Deleted successfully')
    return redirect(reverse('authors:dashboard'))