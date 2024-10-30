from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.functions import Concat
from django.db.models import Q, F
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return  f'{self.id} -> {self.name}'
    
class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),
        )
    )

class Recipe(models.Model):
    objects = RecipeManager()
    choices_preparation = (
        ('Minutos', 'Minutos'),
        ('Horas', 'Horas'),
    )
    choices_servings = (
        ('Porções', 'Porções'),
        ('Pessoas', 'Pessoas'),
        ('Pedaços', 'Pedaços'),
    )
    title = models.CharField(max_length = 32)
    description = models.CharField(max_length=85)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65, choices=choices_preparation)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65, choices=choices_servings)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='receitas/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    tags = GenericRelation(Tag, related_query_name='recipes')

    def __str__(self):
        return  f'{self.id} -> {self.title}'
    
    def get_absolute_url(self):
        return reverse('recipes:receitas', args=(self.id,))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)