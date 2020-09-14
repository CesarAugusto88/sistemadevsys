from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.views.generic import CreateView, ListView, TemplateView

from core.models import Cliente, Funcionario


""" class register(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('account:registrar')
    template_name = 'register.html' """

# --------Registro Cliente-------------
@login_required(login_url="/login/")
def register_clie(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            # depois que cadastrar redireciona para cadastro de cliente
            return redirect('account:cad_cliente')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'register_clie.html', {'form_usuario': form_usuario})

# mostra registro cliente
@login_required(login_url="/login/")
def register_cliente(request):
    id_cliente = request.GET.get("id")
    usuario = User.objects.all().order_by('-username')
    dados = {}
    if id_cliente:
        dados["cliente"] = Cliente.objects.get(id=id_cliente)
    return render(request, 'cadastrar_cliente.html', {'usuario': usuario}, dados)

# submit registro cliente
# colocar foreinkey usando id
@login_required(login_url="/login/")
def submit_register_cliente(request):
    # verificar com ID de usuario para restringir...
    # usuario = 
    if request.method == "POST":
        nome = request.POST.get("nome")
        razao_social = request.POST.get("razao_social")
        tipo_pessoa = request.POST.get("tipo_pessoa")
        cpf_cnpj= request.POST.get("cpf_cnpj")
        rg_ie = request.POST.get("rg_ie")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")
        email = request.POST.get("email")
        fone1 = request.POST.get("fone1")
        usuario_cli_id = request.POST.get("usuario_cli_id")
        Cliente.objects.create(
            nome=nome,
            razao_social=razao_social,
            tipo_pessoa=tipo_pessoa,
            cpf_cnpj=cpf_cnpj,
            rg_ie=rg_ie,
            endereco=endereco,
            cidade=cidade,
            cep=cep,
            uf=uf,
            email=email,
            fone1=fone1,
            usuario_cli_id=usuario_cli_id,
        )
    return redirect("/devsys/funcionario")


# --------Registro Funcionário-------------
@login_required(login_url="/login/")
def register_func(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('account:cad_funcionario')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'register_func.html', {'form_usuario': form_usuario})

# mostra registro funcionario
@login_required(login_url="/login/")
def register_funcionario(request):
    id_funcionario = request.GET.get("id")
    # ordena pelo ultimo, no caso o ID do ultimo cadastrado
    usuario = User.objects.all().order_by('-username')
    dados = {}
    if id_funcionario:
        dados["funcionario"] = Funcionario.objects.get(id=id_funcionario)
    return render(request, 'cadastrar_funcionario.html', {'usuario': usuario}, dados)


@login_required(login_url="/login/")
def submit_register_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone1 = request.POST.get("fone1")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")
        usuario_fun_id = request.POST.get("usuario_fun_id")
        Funcionario.objects.create(
            nome=nome,
            fone1=fone1,
            endereco=endereco,
            cidade=cidade,
            cep=cep,
            uf=uf,
            usuario_fun_id=usuario_fun_id
        )
    return redirect("/devsys/funcionario")