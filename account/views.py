from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.views.generic import CreateView, ListView, TemplateView

from core.models import Cliente, Funcionario

from core.forms import FuncionarioForm, ClienteForm


""" class register(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('account:registrar')
    template_name = 'register.html' """

# --------Registro Cliente-------------
@login_required(login_url="/login/")
def register_cliente(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            # depois que criar user redireciona para cadastro de cliente
            return redirect('account:cadastrar_cliente')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'register_cliente.html', {'form_usuario': form_usuario})

#Cadastrar Cliente
@login_required(login_url="/login/")
def cadastrar_cliente(request):
    """ Cria formulário cliente."""
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            novo = Cliente(**form.cleaned_data)
            novo.save()
            return redirect('funcionario')
    else:
        form = ClienteForm()
    return render(request, "cadastrar_cliente.html", {"form": form})

# --------Registro Funcionário-------------
@login_required(login_url="/login/")
def register_funcionario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('account:cadastrar_funcionario')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'register_funcionario.html', {'form_usuario': form_usuario})

@login_required(login_url="/login/")
def cadastrar_funcionario(request):
    """ Cria formulário funcionário."""
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            novo = Funcionario(**form.cleaned_data)
            novo.save()
            return redirect('funcionario')
    else:
        form = FuncionarioForm()
    return render(request, "cadastrar_funcionario.html", {"form": form})

# Alterar Senhas
@login_required(login_url='/login/')
def alterar_senha_cliente(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('/login/')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha_cliente.html', {'form_senha': form_senha})

@login_required(login_url='/login/')
def alterar_senha_funcionario(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('/login/')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha_funcionario.html', {'form_senha': form_senha})