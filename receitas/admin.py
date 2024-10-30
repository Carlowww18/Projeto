from django.contrib import admin
from . models import Category, Recipe
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag


class CategoryAdmin(admin.ModelAdmin):
    ...



admin.site.register(Category, CategoryAdmin)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_published']
    list_display_links =['title']
    search_fields = ['id', 'title', 'description']
    list_filter = ['category', 'author', 'is_published']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['tags']