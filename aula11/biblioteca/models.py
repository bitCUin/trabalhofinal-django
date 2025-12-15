from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo
