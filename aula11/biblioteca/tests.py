import pytest
from .models import Autor, Livro

@pytest.mark.django_db
def test_criar_livro():
    autor = Autor.objects.create(nome='Machado de Assis')
    livro = Livro.objects.create(titulo='Dom Casmurro', ano_publicacao=1899, autor=autor)

    assert livro.id is not None
    assert livro.autor == autor
    assert livro.titulo == 'Dom Casmurro'
