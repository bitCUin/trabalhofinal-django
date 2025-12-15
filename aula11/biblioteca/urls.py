from django.urls import path
from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('novo/', views.criar_livro, name='criar_livro'),
    path('<int:pk>/editar/', views.editar_livro, name='editar_livro'),
    path('<int:pk>/apagar/', views.apagar_livro, name='apagar_livro'),
    path('login/', views.fazer_login, name='login'),
    path('logout/', views.fazer_logout, name='logout'),
    path('registro/', views.registro, name='registro'),
]
