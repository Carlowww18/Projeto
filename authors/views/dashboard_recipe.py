from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from authors.forms import AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from receitas.models import Recipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
            login_required(login_url='authors:login', redirect_field_name='next'),
            name='dispatch'
)
class dashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_recipe(self, id=None):
         recipe = None

         if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id=id
            ).first()

            if not recipe:
                raise Http404()
            
            return recipe
            
    def render_recipe(self, form):
        return render(self.request, 'author/pages/dashboard_recipe.html', {'form': form})
                                                                    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe) 
        return self.render_recipe(form)
     
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        
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

        return self.render_recipe(form)

@method_decorator(
            login_required(login_url='authors:login', redirect_field_name='next'),
            name='dispatch'
) 
class DashboardRecipeDelete(dashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        if recipe:
            recipe.delete()
            messages.success(self.request, 'Receita deletada com sucesso.')
        else:
            messages.error(self.request, 'Receita não encontrada.')
        return redirect(reverse('authors:dashboard'))