import json
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# Upload/download
from django.views.generic import CreateView, ListView, TemplateView

from core.models import Bol, Cliente, Funcionario, Ordem_Servico

from .forms import ArqForm, BolForm
from .models import Arq, Bol

# def index(request):
#    return redirect('/agenda/')


def home(request):
    # return HttpResponse('Hello World!')
    # Usando render
    return render(request, "home.html")


def contact(request):
    return render(request, "contact.html")


def sistema(request):
    return render(request, "sistema.html")


def login_user(request):
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def submit_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("/devsys/")

        messages.error(request, "Usuário ou senha inválida.")

    return redirect("/login/")


# devsys
@login_required(login_url="/login/")
def devsys(request):
    """ devsys."""

    return render(request, "devsys.html")


# VERIFICAR -> FAZER USUARIO SEPARADO 'usuario_funcionario' 'usuario_cliente' ????????
# PARA ACESSAR SOMENTE DA TABELA CORRESPONDENTE COM SOMENTE SEUS DADOS(hacker pode ver com ids)
# FUNCIONÁRIOS

# Função reconhece se é funcionário ou não
# (Poderia reconhecer o login e entrar no ambiente correto)
@login_required(login_url="/login/")
def lista_funcionarios(request):
    """ Lista dos funcionários."""

    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.filter(usuario_fun=usuario_fun)

    except Exception:
        raise Http404()

    if funcionario:
        # funcionario = Funcionario.objects.all()
        # variáveis usadas no html:
        dados = {"funcionarios": funcionario}

    elif not funcionario:
        messages.info(request, "Você não é um(a) funcionário(a)!")
        return redirect("/devsys/")

    else:
        raise Http404()

    return render(request, "devsys-funcionarios.html", dados)


@login_required(login_url="/login/")
def funcionario(request):
    id_funcionario = request.GET.get("id")
    dados = {}
    if id_funcionario:
        dados["funcionario"] = Funcionario.objects.get(id=id_funcionario)

    return render(request, "funcionario.html", dados)


@login_required(login_url="/login/")
def submit_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone1 = request.POST.get("fone1")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario_fun = request.user
        id_funcionario = request.POST.get("id_funcionario")
        if id_funcionario:
            funcionario = Funcionario.objects.get(id=id_funcionario)
            if funcionario.usuario_fun == usuario_fun:
                funcionario.nome = nome
                funcionario.fone1 = fone1
                funcionario.endereco = endereco
                funcionario.cidade = cidade
                funcionario.cep = cep
                funcionario.uf = uf

                funcionario.save()
        # Evento.objects.filter(id=id_funcionario).update(nome=nome, endereco=endereco,fone1=fone1)
        else:
            Funcionario.objects.create(
                nome=nome,
                fone1=fone1,
                endereco=endereco,
                cidade=cidade,
                cep=cep,
                uf=uf,
                usuario_fun=usuario_fun,
            )
    return redirect("/devsys/funcionarios")


# REDIRECIONAR CORRETAMENTE - OK
@login_required(login_url="/login/")
def delete_funcionario(request, id_funcionario):
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.get(id=id_funcionario)
    except Exception:
        raise Http404()
    if usuario_fun == funcionario.usuario_fun:
        funcionario.delete()
    else:
        raise Http404()
    return redirect("/")  # REDIRECIONAR CORRETAMENTE


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
@login_required(login_url="/login/")
def json_lista_funcionario(request, id_usuario_fun):
    # request.user
    usuario_fun = User.objects.get(id=id_usuario_fun)
    funcionario = Funcionario.objects.filter(usuario_fun=usuario_fun).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(funcionario), safe=False)


# ------------------Ordem de Serviço-----------------------------

# Ordens de serviços
@login_required(login_url="/login/")
def lista_ordem_servicos(request):
    """ Lista das Ordens de Serviços."""

    usuario = request.user

    # já esta verificando em lista de funcionários. OK
    try:
        # Mesmo objeto em html
        # verificar se é um funcionário.
        funcionario = Funcionario.objects.filter(usuario_fun=usuario)

    except Exception:
        raise Http404()
    if funcionario:
        # Com essa função de mostrar somente maiores ou menores da para esconder os registros
        # PARA APARECER AS ORDENS DE SERVIÇOS SOMENTE MAIORES -> (__gt) QUE A DATA ATUAL
        data_atual = datetime.now() - timedelta(
            days=365
        )  # para retornar com atrasados há 1 ano
        ordem_servico = Ordem_Servico.objects.filter(
            usuario_os=usuario, dt_agenda__gt=data_atual
        )  # __gt só Maior, __lt só Menor
        # variáveis usadas no html:
        dados = {"ordem_servicos": ordem_servico}
    else:
        raise Http404()

    return render(request, "devsys-ordem-servicos.html", dados)


@login_required(login_url="/login/")
def ordem_servico(request):
    id_ordem_servico = request.GET.get("id")
    # print(id_ordem_servico)
    dados = {}
    if id_ordem_servico:
        dados["ordem_servico"] = Ordem_Servico.objects.get(id=id_ordem_servico)
    return render(request, "ordem-servico.html", dados)


@login_required(login_url="/login/")
def submit_ordem_servico(request):
    if request.POST:
        dt_entrada = request.POST.get("dt_entrada")
        descricao = request.POST.get("descricao")
        dt_agenda = request.POST.get("dt_agenda")
        dt_pagamento = request.POST.get("dt_pagamento")
        equipamento = request.POST.get("equipamento")
        responsavel = request.POST.get("responsavel")
        usuario_os = request.user

        # django atribui 'id' no inicio do nome da tabela automaticamente ou so 'id'?
        id_ordem_servico = request.POST.get("id_ordem_servico")
        # para editar pega o id_ordem_serviço no template HTML
        if id_ordem_servico:
            ordem_servico = Ordem_Servico.objects.get(id=id_ordem_servico)
            if ordem_servico.usuario_os == usuario_os:
                ordem_servico.dt_entrada = dt_entrada
                ordem_servico.descricao = descricao
                ordem_servico.dt_agenda = dt_agenda
                ordem_servico.dt_pagamento = dt_pagamento
                ordem_servico.responsavel = responsavel
                ordem_servico.equipamento = equipamento
                ordem_servico.save()
        # senão, cria!
        else:
            Ordem_Servico.objects.create(
                dt_entrada=dt_entrada,
                descricao=descricao,
                dt_agenda=dt_agenda,
                dt_pagamento=dt_pagamento,
                responsavel=responsavel,
                equipamento=equipamento,
                usuario_os=usuario_os,
            )

    return redirect("/devsys/ordem-servicos")


@login_required(login_url="/login/")
def delete_ordem_servico(request, id_ordem_servico):
    usuario_os = request.user
    try:
        ordem_servico = Ordem_Servico.objects.get(id=id_ordem_servico)
    except Exception:
        raise Http404()
    if usuario_os == ordem_servico.usuario_os:
        ordem_servico.delete()
    else:
        raise Http404()
    return redirect("/devsys/ordem-servicos")


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decorator
# @login_required(login_url='/login/')
def json_lista_ordem_servico(request, id_usuario_os):
    # request.user
    usuario_os = User.objects.get(id=id_usuario_os)
    ordem_servico = Ordem_Servico.objects.filter(usuario_os=usuario_os).values(
        "id", "dt_entrada"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(ordem_servico), safe=False)


# FUNÇÕES DE UPLOAD - Arquivos para BD Funcionarios

# class Home(TemplateView):
#    template_name = 'home.html'


@login_required(login_url="/login/")
def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "upload.html", context)


@login_required(login_url="/login/")
def arq_list(request):
    arqs = Arq.objects.all()
    return render(request, "arq_list.html", {"arqs": arqs})


@login_required(login_url="/login/")
def upload_arq(request):
    if request.method == "POST":
        form = ArqForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("arq_list")
    else:
        form = ArqForm()
    return render(request, "upload_arq.html", {"form": form})


@login_required(login_url="/login/")
def delete_arq(request, pk):
    if request.method == "POST":
        arq = Arq.objects.get(pk=pk)
        arq.delete()
    return redirect("arq_list")


class ArqListView(ListView):
    model = Arq
    template_name = "class_arq_list.html"
    context_object_name = "arqs"


class UploadArqView(CreateView):
    model = Arq
    form_class = ArqForm
    success_url = reverse_lazy("class_arq_list")
    template_name = "upload_arq.html"


# -------Cliente--------------------------
# Cliente vai ver seus dados e pode editar, fazer o mesmo para funcionários...

# CLIENTES - **** Somente cliente logado e usuario ADMIN ****

# Função mostra se é cliente ou não
# (Poderia reconhecer o login e entrar no seu ambiente correto)
@login_required(login_url="/login/")
def lista_clientes(request):
    """ Lista dos clientes."""

    usuario_cli = request.user

    try:
        # Mesmo objeto em html
        cliente = Cliente.objects.filter(usuario_cli=usuario_cli)
        # cliente = Cliente.objects.all()
    except Exception:
        raise Http404()
    if cliente:
        dados = {"clientes": cliente}
        # variáveis usadas no html:
        # Colocar IF para verificar cliente e assim mostrar os dados... Mesmo para funcionario.
    # com elif ou message no empty for template
    # melhor aqui no views pois ja está validando
    elif not cliente:
        messages.info(request, "Você não é um(a) cliente!")
        return redirect("/devsys/")

    else:
        raise Http404()

    return render(request, "devsys-clientes.html", dados)


@login_required(login_url="/login/")
def cliente(request):
    id_cliente = request.GET.get("id")
    dados = {}
    if id_cliente:
        dados["cliente"] = Cliente.objects.get(id=id_cliente)
    return render(request, "cliente.html", dados)


@login_required(login_url="/login/")
def submit_cliente(request):
    if request.POST:
        nome = request.POST.get("nome")
        celular = request.POST.get("celular")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario_cli = request.user
        id_cliente = request.POST.get("id_cliente")
        if id_cliente:
            cliente = Cliente.objects.get(id=id_cliente)
            if cliente.usuario_cli == usuario_cli:
                cliente.nome = nome
                cliente.celular = celular
                cliente.endereco = endereco
                cliente.cidade = cidade
                cliente.cep = cep
                cliente.uf = uf
                cliente.save()
        else:
            Cliente.objects.create(
                nome=nome,
                celular=celular,
                endereco=endereco,
                cidade=cidade,
                cep=cep,
                uf=uf,
                usuario_cli=usuario_cli,
            )
    return redirect("/devsys/clientes")


@login_required(login_url="/login/")
def delete_cliente(request, id_cliente):
    usuario_cli = request.user
    try:
        cliente = Cliente.objects.get(id=id_cliente)
    except Exception:
        raise Http404()
    if usuario_cli == cliente.usuario_cli:
        cliente.delete()
    else:
        raise Http404()
    return redirect("/devsys/clientes")


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
# @login_required(login_url='/login/')
def json_lista_cliente(request, id_usuario):
    # request.user
    usuario_cli = User.objects.get(id=id_usuario)
    cliente = Cliente.objects.filter(usuario_cli=usuario_cli).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(cliente), safe=False)

@login_required(login_url="/login/")
def clientes(request):
    """ Lista clientes."""
    #pegar somente usuario admin
    usuario_admin = request.user

    try:
        # Mesmo objeto em html
        cliente = Cliente.objects.all()

    except Exception:
        raise Http404()
    if usuario_admin:
        dados = {"clientes": cliente}
        # variáveis usadas no html:
        # Colocar IF para verificar cliente e assim mostrar os dados... Mesmo para funcionario.
    # com elif ou message no empty for template
    # melhor aqui no views pois ja está validando
    elif not cliente:
        messages.info(request, "Você não é um(a) administrador(a)!")
        return redirect("/devsys/")

    else:
        raise Http404()

    return render(request, "upload_boletos_clientes.html", dados)


# FUNÇÕES DE UPLOAD - Boletos - construindo - *somente para cliente logado

@login_required(login_url="/login/")
def uploadb(request):
    """Função para carregar o arquivo boleto para o cliente.
    Essa função é chamada pelo funcionário (específico) lançar o boleto"""
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "uploadb.html", context)

# TODO: pegar e colocar cada boleto específico de cada cliente
@login_required(login_url="/login/")
def bol_list(request):
    bols = Bol.objects.all()
    return render(request, "bol_list.html", {"bols": bols})


@login_required(login_url="/login/")
def upload_bol(request):
    if request.method == "POST":
        form = BolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("bol_list")
    else:
        form = BolForm()
    return render(request, "upload_bol.html", {"form": form})


@login_required(login_url="/login/")
def delete_bol(request, pk):
    if request.method == "POST":
        bol = Bol.objects.get(pk=pk)
        bol.delete()
    return redirect("bol_list")


class BolListView(ListView):
    model = Bol
    template_name = "class_bol_list.html"
    context_object_name = "bols"


class UploadBolView(CreateView):
    model = Bol
    form_class = BolForm
    success_url = reverse_lazy("class_bol_list")
    template_name = "upload_bol.html"
