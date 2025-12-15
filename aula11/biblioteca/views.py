from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.views.decorators.http import require_POST
from .models import Livro, Autor
from django.urls import reverse
from django import forms

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'ano_publicacao', 'autor']

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar senha")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("As senhas não conferem.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

def registro(request):
    if request.user.is_authenticated:
        return redirect('biblioteca:lista_livros')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, f"Bem-vindo {user.first_name}!")
            return redirect('biblioteca:lista_livros')
    else:
        form = RegistroForm()
    return render(request, 'biblioteca/registro.html', {'form': form})

def fazer_login(request):
    if request.user.is_authenticated:
        return redirect('biblioteca:lista_livros')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta, {user.first_name}!")
                return redirect('biblioteca:lista_livros')
            else:
                messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = LoginForm()
    return render(request, 'biblioteca/login.html', {'form': form})

def fazer_logout(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso!")
    return redirect('biblioteca:lista_livros')

def lista_livros(request):
    if request.user.is_authenticated:
        livros = Livro.objects.select_related('autor', 'usuario').all()
    else:
        livros = Livro.objects.select_related('autor', 'usuario').all()
    return render(request, 'biblioteca/lista_livros.html', {'livros': livros})

@login_required(login_url='biblioteca:login')
def criar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user
            livro.save()
            messages.success(request, "Livro criado com sucesso!")
            return redirect(reverse('biblioteca:lista_livros'))
    else:
        form = LivroForm()
    return render(request, 'biblioteca/form_livro.html', {'form': form, 'titulo': 'Novo Livro'})

@login_required(login_url='biblioteca:login')
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if livro.usuario != request.user:
        messages.error(request, "Você não tem permissão para editar este livro.")
        return redirect('biblioteca:lista_livros')
    
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect(reverse('biblioteca:lista_livros'))
    else:
        form = LivroForm(instance=livro)
    return render(request, 'biblioteca/form_livro.html', {'form': form, 'livro': livro, 'titulo': 'Editar Livro'})

@login_required(login_url='biblioteca:login')
def apagar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if livro.usuario != request.user:
        messages.error(request, "Você não tem permissão para apagar este livro.")
        return redirect('biblioteca:lista_livros')
    
    if request.method == 'POST':
        livro.delete()
        messages.success(request, "Livro deletado com sucesso!")
        return redirect(reverse('biblioteca:lista_livros'))
    return render(request, 'biblioteca/confirm_delete.html', {'livro': livro})
