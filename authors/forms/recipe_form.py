from django import forms
from receitas.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
    title = forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'span'
        })
    )
    preparation_steps = forms.CharField(
        widget = forms.Textarea(attrs={
            'class': 'span'
        })
    )
    cover = forms.CharField(
        required=False,
        widget = forms.FileInput(attrs={
            'class': 'span'
        })
    )
    servings_unit = forms.CharField(
        widget = forms.Select(
            choices=(
                ('Porções', 'Porções'),
                ('Pessoas', 'Pessoas'),
                ('Pedaços', 'Pedaços')
            )
        )
    )
    preparation_time_unit = forms.CharField(
        widget = forms.Select(
            choices=(
                ('Minutos', 'Minutos'),
                ('Horas', 'Horas')
            )
        )
    )
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover']
