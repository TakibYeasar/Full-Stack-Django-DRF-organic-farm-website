# Generated by Django 5.0 on 2024-01-09 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_article_slug_alter_articlescategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='articlescategory',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, default=''),
        ),
    ]