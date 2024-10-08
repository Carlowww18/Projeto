# Generated by Django 5.1 on 2024-10-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0005_alter_recipe_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time_unit',
            field=models.CharField(choices=[('Minutos', 'Minutos'), ('Horas', 'Horas')], max_length=65),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='servings_unit',
            field=models.CharField(choices=[('Porções', 'Porções'), ('Pessoas', 'Pessoas'), ('Pedaços', 'Pedaços')], max_length=65),
        ),
    ]
