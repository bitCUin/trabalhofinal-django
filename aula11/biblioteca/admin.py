from django.contrib import admin
from .models import Autor, Livro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id','titulo','ano_publicacao','autor')
