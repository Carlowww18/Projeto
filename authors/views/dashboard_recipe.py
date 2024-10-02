from django.views import View
from django.shortcuts import render, redirect
from authors.forms import AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from receitas.models import Recipe

class dashboard_recipe(View):
    def get_recipe(self, id):
         recipe = None

         if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id=id
            ).first()

            if not recipe:
                raise Http404()
            
    def render_recipe(self, form):
        return render(self.request, 'author/pages/dashboard_recipe.html', {'form': form})
                                                                    
        
    def get(self, request, id):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe) 
        return self.render_recipe(form)
     
    def post(self, request, id):
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