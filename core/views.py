import json
from datetime import datetime, timedelta
from django.db import connection

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# Upload/download
from django.views.generic import CreateView, ListView, TemplateView

from core.models import (Arq, Bol, Cliente, Funcionario, Ordem_Servico,
                        Chamado, Ven_Caixa, Ven_Formas, Fin_Banco, Fin_Conta, Fin_SubConta,
                        Ven_Fecha_Caixa, Con_Empresa)

from .forms import (ArqForm, BolForm , ChamadoForm, ClienteFunForm,
                    Ven_CaixaForm, Ven_FormasForm, Fin_BancoForm,
                    Fin_ContaForm, Fin_SubContaForm,
                    Ven_Fecha_CaixaForm, Con_EmpresaForm)

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
    return redirect("login_user")


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


# devsys - enviar direto para user (funcionario/cliente)
@login_required(login_url="/login/")
def devsys(request):
    """ Devsys. Verifica se é funcionario ou cliente."""
    usuario = request.user
    # select * from Funcionario where usuario_fun = usuario;
    funcionario = Funcionario.objects.filter(usuario_fun=usuario)

    if funcionario:
        return redirect("/devsys/funcionario")
    else:
        return redirect("/devsys/cliente")

    #return render(request, "devsys.html")


# VERIFICAR -> FAZER USUARIO SEPARADO 'usuario_funcionario' 'usuario_cliente' ????????
# PARA ACESSAR SOMENTE DA TABELA CORRESPONDENTE COM SOMENTE SEUS DADOS(hacker pode ver com ids)

# FUNCIONÁRIOS
# Mudado nome de lista_funcionarios para dados_funcionario
@login_required(login_url="/login/")
def dados_funcionario(request):
    """ Lista dados do funcionário."""
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.filter(usuario_fun=usuario_fun)

    except Exception:
        raise Http404()

    #if funcionario:
    if funcionario:
        # variáveis usadas no html:
        #Mudando variáveis e rotas...
        dados = {"funcionario": funcionario}

    else:
        raise Http404()

    return render(request, "devsys-funcionario.html", dados)


@login_required(login_url="/login/")
def funcionario(request):
    dados = {}
    #pegar usuário solicitando
    usuario = request.user
    id_funcionario = request.GET.get("id")
    if id_funcionario:
        funcionario = Funcionario.objects.get(id=id_funcionario)
        # se o mesmo funcionario.usuario_fun id igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if funcionario.usuario_fun == usuario:
            dados["funcionario"] = Funcionario.objects.get(id=id_funcionario)

    return render(request, "funcionario.html", dados)

# edita funcionario
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
        
    return redirect("funcionario")


@login_required(login_url="/login/")
def delete_funcionario(request, id_funcionario):
    # Fazer verificações como esta nas outras funções.
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.get(id=id_funcionario)
    except Exception:
        raise Http404()
    if usuario_fun == funcionario.usuario_fun:
        funcionario.delete()
    else:
        raise Http404()
    return redirect("/devsys")  # REDIRECIONAR CORRETAMENTE


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

    try:
        # Mesmo objeto em html
        # verificar se é um funcionário.
        funcionario = Funcionario.objects.filter(usuario_fun=usuario)

    except Exception:
        raise Http404()
    if funcionario:
        #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            # Com essa função de mostrar somente maiores ou menores da para esconder os registros
            # PARA APARECER AS ORDENS DE SERVIÇOS SOMENTE MAIORES -> (__gt) QUE A DATA ATUAL
            data_atual = datetime.now() - timedelta(
                days=365
            )  # para retornar com atrasados há 1 ano
            ordem_servico = Ordem_Servico.objects.filter(
                usuario_os=usuario, dt_agenda__gt=data_atual
            )  # __gt só Maior, __lt só Menor
            #__icontains sem case sensitive
            ordem_servico = ordem_servico.filter(responsavel__icontains=termo_pesquisa)
        else:
            data_atual = datetime.now() - timedelta(
                days=365
            )
            ordem_servico_list = Ordem_Servico.objects.filter(
                usuario_os=usuario, dt_agenda__gt=data_atual
            ).order_by('-dt_atualizada')
            paginator = Paginator(ordem_servico_list, 10)
            page = request.GET.get('page')
            ordem_servico = paginator.get_page(page)

            
        dados = {"ordem_servicos": ordem_servico}
    else:
        raise Http404()

    return render(request, "devsys-ordem-servicos.html", dados)

# mostra campos ordem de serviço
@login_required(login_url="/login/")
def ordem_servico(request):
    id_ordem_servico = request.GET.get("id")
    # print(id_ordem_servico)
    dados = {}
    if id_ordem_servico:
        dados["ordem_servico"] = Ordem_Servico.objects.get(id=id_ordem_servico)
    return render(request, "ordem-servico.html", dados)

# submit ordem de serviço edita ou cria
@login_required(login_url="/login/")
def submit_ordem_servico(request):
    if request.POST:
        descricao = request.POST.get("descricao")
        dt_agenda = request.POST.get("dt_agenda")
        dt_pagamento = request.POST.get("dt_pagamento")
        equipamento = request.POST.get("equipamento")
        responsavel = request.POST.get("responsavel")
        valor = request.POST.get("valor")
        confirmar = request.POST.get("confirmar")
        finalizar = request.POST.get("finalizar")
        usuario_os = request.user
        print("confirmar: ", confirmar, " finalizar: ", finalizar)
        # django atribui 'id' no inicio do nome da tabela automaticamente
        id_ordem_servico = request.POST.get("id_ordem_servico")
        if confirmar == "on" and finalizar == None:
            confirmar = True
            finalizar = False
        elif finalizar == "on" and confirmar == None:
            confirmar = False
            finalizar = True
        elif confirmar == "on" and finalizar =="on":
            confirmar = True
            finalizar = True
        else:
            confirmar = False
            finalizar = False

        print("confirmar: ", confirmar, " finalizar: ", finalizar)
        # para editar pega o id_ordem_serviço no template HTML
        if id_ordem_servico:
            ordem_servico = Ordem_Servico.objects.get(id=id_ordem_servico)
            if ordem_servico.usuario_os == usuario_os:
                
                ordem_servico.descricao = descricao
                ordem_servico.dt_agenda = dt_agenda
                ordem_servico.dt_pagamento = dt_pagamento
                ordem_servico.responsavel = responsavel
                ordem_servico.equipamento = equipamento
                ordem_servico.valor = valor
                ordem_servico.confirmar = confirmar
                ordem_servico.finalizar = finalizar
                ordem_servico.save()
                print("confirmar: ", ordem_servico.confirmar, " finalizar: ", ordem_servico.finalizar)
        # senão, cria! Usado na mesma função.
        else:
            Ordem_Servico.objects.create(
                
                descricao=descricao,
                dt_agenda=dt_agenda,
                dt_pagamento=dt_pagamento,
                responsavel=responsavel,
                equipamento=equipamento,
                valor=valor,
                confirmar=confirmar,
                finalizar=finalizar,
                usuario_os=usuario_os, #pega user request
            )
        # print("confirmar: ", confirmar, " finalizar: ", finalizar)
    return redirect("ordem-servicos")


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
    return redirect("ordem-servicos")


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
    #id pesquisa
    termo_pesquisa = request.GET.get('pesquisa', None)
    # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
    if termo_pesquisa:
        arqs = Arq.objects.all()
        #__icontains sem case sensitive
        arqs = arqs.filter(titulo__icontains=termo_pesquisa)
    else:
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

#Update arquivo. ERRO Não altera arquivo
@login_required(login_url="/login/")
def update_arq(request, id):
    """ Atualiza Arquivo"""
    arq = Arq.objects.get(id=id)
    form = ArqForm(request.POST or None, instance=arq)
    if form.is_valid():
        form.save()
        return redirect("arq_list")
    return render(request, "arq_update.html", {"form": form, 'arq': arq})

@login_required(login_url="/login/")
def delete_arq(request, id):
    if request.method == "POST":
        arq = Arq.objects.get(id=id)
        arq.delete()
    return redirect("arq_list")


# Usando Class-Based Vieqw
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


@login_required(login_url="/login/")
def dados_cliente(request):
    """ Mostra dados do cliente."""
    usuario_cli = request.user
    try:
        # Mesmo objeto em html
        cliente = Cliente.objects.filter(usuario_cli=usuario_cli)
        # cliente = Cliente.objects.all()
    except Exception:
        raise Http404()
    if cliente:
        # variáveis usadas no html:
        dados = {"cliente": cliente}
    else:
        raise Http404()

    return render(request, "devsys-cliente.html", dados)


@login_required(login_url="/login/")
def cliente(request):
    dados = {}
    # pegar usuario solicitando
    usuario = request.user
    id_cliente = request.GET.get("id")
    if id_cliente:
        cliente = Cliente.objects.get(id=id_cliente)
        # se o mesmo cliente.usuario_cliid igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if cliente.usuario_cli == usuario:
            dados["cliente"] = Cliente.objects.get(id=id_cliente)
    return render(request, "cliente.html", dados)

# editar cliente
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
        
    return redirect("/devsys/cliente")


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
    return redirect("/devsys")


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

# boletos clientes - pegar user id
@login_required(login_url="/login/")
def bol_clientes(request):
    """ Lista clientes. Usado para mostrar 'Lançar Boletos' pelo funcionário.
        Pegar id do cliente específico para mostrar o boleto no cliente - Função uploadb.
        Mostrar id e pegar mesmo id no uploadb."""
    usuario = request.user
    try:
        # Pegar foreingkey usuario_cli
        funcionario = Funcionario.objects.get(usuario_fun=usuario)

    except Exception:
        raise Http404()
    if funcionario:
        #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            bols = Bol.objects.all()
            #__icontains sem case sensitive
            bols = bols.filter(titulo__icontains=termo_pesquisa)
            cliente = Cliente.objects.all()
        else:
            bols = Bol.objects.all()
            cliente = Cliente.objects.all()
        dados = {"bols": bols, "cliente": cliente}

    else:
        raise Http404()

    return render(request, "upload_boletos_clientes.html", dados)


# FUNÇÕES DE UPLOAD - Boletos

@login_required(login_url="/login/")
def uploadb(request):
    """Função para carregar o boleto/arquivo para o 'cliente'.
    Essa função é chamada pelo funcionário (específico) lançar o boleto"""
    context = {}
    cliente = Cliente.objects.all()
    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "uploadb.html", {'cliente': cliente}, context)


@login_required(login_url="/login/")
def bol_list(request):
    usuario = request.user
    dados = {}
    try:
        cliente = Cliente.objects.filter(usuario_cli=usuario)
        
    except Exception:
        raise Http404()
    if cliente:
        #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            bols = Bol.objects.filter(cliente__in=cliente)
            #__icontains sem case sensitive
            bols = bols.filter(titulo__icontains=termo_pesquisa)
        else:
            # __in pode manipular querysets maiores que um (múltiplos registros de uma tabela).
            #Isso pode ser encontrado na seção de relacionamentos django Many-to_one da documentação. 
            #docs.djangoproject.com/en/2.0/topics/db/examples/many_to_one/
            bols = Bol.objects.filter(cliente__in=cliente)
        
        # se precisar dos dados do cliente
        dados = {"bols": bols, "cliente": cliente}
    else:
        raise Http404()

    return render(request, "bol_list.html", dados)


@login_required(login_url="/login/")
def upload_bol(request):
    """ Cria formulário de boleto e envia objeto cliente para pegar id. """
    if request.method == "POST":
        form = BolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("bol_clientes")
    else:
        form = BolForm()
    return render(request, "upload_bol.html", {"form": form})

#Update arquivo/boleto. ERRO Não altera arquivo
@login_required(login_url="/login/")
def update_bol(request, id):
    """ Atualiza Arquivo/boleto."""
    bol = Bol.objects.get(id=id)
    form = BolForm(request.POST or None, instance=bol)
    if form.is_valid():
        form.save()
        return redirect("bol_clientes")
    return render(request, "bol_update.html", {"form": form, 'bol': bol})

@login_required(login_url="/login/")
def delete_bol(request, id):
    if request.method == "POST":
        bol = Bol.objects.get(id=id)
        bol.delete()
    return redirect("bol_clientes")


class BolListView(ListView):
    model = Bol
    template_name = "class_bol_list.html"
    context_object_name = "bols"


class UploadBolView(CreateView):
    model = Bol
    form_class = BolForm
    success_url = reverse_lazy("class_bol_list")
    template_name = "upload_bol.html"


# -------------------------CHAMADO---------------------------------------------

# FUNÇÕES DE UPLOAD
@login_required(login_url="/login/")
def uploadchamado(request):
    """Essa função carrega o arquivo do cliente
       É chamada pelo cliente(específico) enviar o arquivo/chamado para o funcionário"""
    context = {}

    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "uploadchamado.html", context)

#Lista Chamado dos clientes
@login_required(login_url="/login/")
def chamado_list(request):
    """ Lista Chamado Cliente """
    usuario = request.user
    dados = {}
    try:
        cliente = Cliente.objects.get(usuario_cli=usuario)
        # funcionario = Funcionario.objects.all()
    except Exception:
        raise Http404()

    #NÃO ESTÁ PEGANDO O CLIENTE ESPECÍFICO QUE LANÇOU OS CHAMADOS
    # VERIFICAR TAMBÉM EM OUTRA FUNÇÕES
    if cliente:
        #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            chamados = Chamado.objects.filter(cliente=cliente)
            #__icontains sem case sensitive
            chamados = chamados.filter(assunto__icontains=termo_pesquisa)
        else:
            #OK esta pegando so os chamados referentes ao cliente que criou
            #***É preciso atribuir automaticamente o cliente_ch***
            chamados = Chamado.objects.filter(cliente=cliente)
            #print(cliente.nome)
        # se precisar dos dados do cliente
        dados = {"cliente": cliente, "chamados": chamados}
    else:
        raise Http404()

    return render(request, "chamado_list.html", dados)

#Lista Chamado para funcionários
@login_required(login_url="/login/")
def chamado_list_fun(request):
    """ Lista Chamado Para Funcionário Específico. """
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            chamados = Chamado.objects.filter(funcionario=funcionario)
            #__icontains sem case sensitive
            chamados = chamados.filter(nome_cliente__icontains=termo_pesquisa)
        else:
            chamados = Chamado.objects.filter(funcionario=funcionario)
        dados = {"funcionario": funcionario, "chamados": chamados}
    else:
        raise Http404()

    return render(request, "chamado_list_fun.html", dados)


@login_required(login_url="/login/")
def criar_chamado(request):
    """ Cria formulário do chamado e envia objeto cliente para pegar id.
    """
    usuario = request.user
    # é preciso pegar usuario com 'get' para atribuir em cliente de chamado.
    usuario_cli = Cliente.objects.get(usuario_cli=usuario)
    #print(usuario_cli)
    if request.method == "POST":
        form = ChamadoForm(request.POST, request.FILES)
        if form.is_valid():
            novo = Chamado(cliente=usuario_cli, **form.cleaned_data)
            # titulo = form.cleaned_data['titulo']
            # assunto = form.cleaned_data['assunto']
            # descricao = form.cleaned_data['descricao']
            # arquivo = form.cleaned_data['arquivo']
            # funcionario = form.cleaned_data['funcionario']
            # #cliente = form.cleaned_data['cliente']
            # novo = Chamado(
            #     titulo=titulo, assunto=assunto, descricao=descricao,
            #     arquivo=arquivo, funcionario=funcionario, cliente=usuario_cli #aceitar usuario request
            # )
            novo.save()
            return redirect("chamado_list")
    else:
        form = ChamadoForm()
    return render(request, "criar_chamado.html", {"form": form})

# Update Chamado
@login_required(login_url="/login/")
def update_chamado(request, id):
    """ Atualiza Chamado."""
    chamado = Chamado.objects.get(id=id)
    form = ChamadoForm(request.POST or None, instance=chamado)
    if form.is_valid():
        form.save()
        return redirect("chamado_list")
    return render(request, "chamado_update.html", {"form": form, 'chamado': chamado})

@login_required(login_url="/login/")
def delete_chamado(request, id):
    if request.method == "POST":
        chamado = Chamado.objects.get(id=id)
        chamado.delete()
    return redirect("chamado_list")


class ChamadoListView(ListView):
    model = Chamado
    template_name = "class_chamado_list.html"
    context_object_name = "chamados"


class UploadChamadoView(CreateView):
    model = Chamado
    form_class = ChamadoForm
    success_url = reverse_lazy("class_chamado_list")
    template_name = "criar_chamado.html"

################### Clientes para verificação no Funcionario ###########
#Lista clientes
@login_required(login_url="/login/")
def list_clientes(request):
    """ Lista clientes para Funcionários"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            clientes = Cliente.objects.all()
            #__icontains sem case sensitive
            clientes = clientes.filter(nome__icontains=termo_pesquisa)
        else:
            clientes = Cliente.objects.all()
        dados = {"funcionario": funcionario, "clientes": clientes}
    else:
        raise Http404()

    return render(request, "clientes_list_fun.html", dados)

# Update clientes
@login_required(login_url="/login/")
def update_clientes(request, id):
    """ Atualiza cliente."""
    cliente = Cliente.objects.get(id=id)
    form = ClienteFunForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("list_clientes")
    return render(request, "clientes_update_fun.html", {"form": form, 'cliente': cliente})

@login_required(login_url="/login/")
def delete_clientes(request, id):
    if request.method == "POST":
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
    return redirect("list_clientes")


################### Ven_Caixa Vendas do Caixa do Funcionário ###########
#### ATUALIZANDO - E FALTA CHAMAR NO URLs ######
@login_required(login_url="/login/")
def list_caixas(request):
    """ Lista Vendas do caixa do Funcionário"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            caixas = Ven_Caixa.objects.all()
            #__icontains sem case sensitive
            caixas = caixas.filter(nome_caixa__icontains=termo_pesquisa)
        else:
            caixas_list = Ven_Caixa.objects.filter().order_by(
                '-referencial')
            paginator = Paginator(caixas_list, 10)
            page = request.GET.get('page')
            caixas = paginator.get_page(page)

        dados = {"funcionario": funcionario, "caixas": caixas}
    else:
        raise Http404()

    return render(request, "list_caixas.html", dados)


# Função para mostrar total de comandas do caixa específico
@login_required(login_url="/login/")
def total_comandas(request):
    usuario = request.user
    dados = {}
    ref = request.GET.get("referencial")
    list_ = []
    sum_troco = 0
    sum_c = 0
    sum_d = 0
    sum_r_dinheiro = 0
    sum_r_che = 0
    sum_r_v_e = 0
    sum_r_desconto = 0
    sum_r_carteira = 0
    sum_total_dinheiro = 0
    sum_total_cheque = 0
    sum_rec_contas = 0
    forma_dinheiro = ''
    forma_cheque =''

    if ref:
        #### Fechamento de Caixa - total de comandas ###
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
        # Usando referencial de caixa: caixa.referencial
        caixa = Ven_Caixa.objects.get(referencial=ref)

        fecha_caixa = Ven_Fecha_Caixa.objects.all()
        sel = fecha_caixa.filter(ref_caixa=ref)
        # Querys
        # print(sel.query)
        for s in sel:
            if s.ref_saida:
                list_.append(s.ref_saida)

        # count esta somente com UM ref_saida, r_c ref_caixa
        count = sorted(set(list_))

        ### Troco ###
        for f in sel:
            if f.ref_caixa and f.ref_forma == 1 and f.troco == 'Sim':
                sum_troco = sum_troco + (f.valor - f.debito)
        # print(sum)

        ### Recebimentos ###
        for r in sel:
            if (r.valor and r.ref_caixa and r.ref_banco == 7 and
                (r.troco != 'Sim' or r.troco is None or r.troco =='Não')):
                if r.ref_forma == 1:  # Dinheiro
                    sum_r_dinheiro = sum_r_dinheiro + (r.valor - r.debito)
                if r.ref_forma == 2:  # Cheque
                    sum_r_che = sum_r_che + (r.valor - r.debito)
                if r.ref_forma == 3:  # Visa electron
                    sum_r_v_e = sum_r_v_e + (r.valor - r.debito)
                if r.ref_forma == 11:  # Desconto
                    sum_r_desconto = sum_r_desconto + (r.valor - r.debito)
                if r.ref_forma == 20:  # Carteira -> a prazo
                    sum_r_carteira = sum_r_carteira + (r.valor - r.debito)

        ### Recebimentos total ###
        for t in sel:
            if t.ref_forma != 20 and t.ref_banco == 7 and t.ref_caixa:
                sum_c = sum_c + (t.valor)
                sum_d = sum_d + (t.debito)

        # Transferencias - retiradas
        # select debito, b.nome
        # from Ven_Fecha_Caixa a
        # inner join ven_formas b on (a.ref_forma=b.referencial)
        # where a.complemento like ('%Transferência%') and a.ref_banco=1
        # order by a.ref_forma
        comp_transf = Ven_Fecha_Caixa.objects.filter(
                    complemento__contains='Transf')
        # print(comp_transf)
        for i in comp_transf:
            ref_t = Ven_Formas.objects.filter(referencial=i.ref_forma)
            for j in ref_t:
                if (i.ref_banco == 1 and i.ref_forma==j.referencial and
                    i.ref_caixa == caixa.referencial):
                    # Mostrar numa var no for no html
                    print(j.nome, i.debito, i.hora)
                    if j.nome == 'DINHEIRO':
                        forma_dinheiro = j.nome
                        sum_total_dinheiro = sum_total_dinheiro + i.debito
                    if j.nome == 'CHEQUE':
                        forma_cheque = j.nome
                        sum_total_cheque = sum_total_cheque + i.debito

        # recebimento de contas
        comp_rec_conta= Ven_Fecha_Caixa.objects.filter(
                complemento__contains='Rec. Conta:')
        for y in comp_rec_conta:
            if y.ref_caixa == caixa.referencial:
                sum_rec_contas = sum_rec_contas + y.valor

        dados = {"funcionario": funcionario, "total": len(count),
                    "caixa": caixa, "sum_troco": sum_troco,
                    "sum_c": sum_c, "sum_d": sum_d, "sum_s": (sum_c-sum_d),
                    "sum_r_dinheiro": sum_r_dinheiro, "sum_r_che": sum_r_che,
                    "sum_r_v_e": sum_r_v_e, "sum_r_desconto": sum_r_desconto,
                    "sum_r_carteira": sum_r_carteira,
                    "gaveta": (sum_r_dinheiro + sum_troco),
                    "sum_rec_contas": sum_rec_contas,
                    "forma_dinheiro": forma_dinheiro,
                    "forma_cheque": forma_cheque,
                    "sum_total_dinheiro": sum_total_dinheiro,
                    "sum_total_cheque": sum_total_cheque
                    }

    return render(request, "total_comandas.html", dados)


# VEN_FORMAS #
@login_required(login_url="/login/")
def list_formas(request):
    """ Lista Formas Vendas"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            formas = Ven_Formas.objects.all()
            #__icontains sem case sensitive
            formas = formas.filter(nome__icontains=termo_pesquisa)
        else:
            formas_list = Ven_Formas.objects.filter().order_by(
                '-referencial')
            paginator = Paginator(formas_list, 10)
            page = request.GET.get('page')
            formas = paginator.get_page(page)
            # formas = Ven_Formas.objects.all()
        dados = {"formas": formas}
    else:
        raise Http404()

    return render(request, "list_formas.html", dados)


# Fin_Banco #
@login_required(login_url="/login/")
def list_bancos(request):
    """ Lista Bancos"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            bancos = Fin_Banco.objects.all()
            #__icontains sem case sensitive
            bancos = bancos.filter(banco__icontains=termo_pesquisa)
        else:
            bancos = Fin_Banco.objects.all()
        dados = {"bancos": bancos}
    else:
        raise Http404()

    return render(request, "list_bancos.html", dados)


# Fin_Conta #
@login_required(login_url="/login/")
def list_contas(request):
    """ Lista Contas"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            contas = Fin_Conta.objects.all()
            #__icontains sem case sensitive
            contas = contas.filter(conta__icontains=termo_pesquisa)
        else:
            contas = Fin_Conta.objects.all()
        dados = {"contas": contas}
    else:
        raise Http404()

    return render(request, "list_contas.html", dados)


# Fin_SubConta #
@login_required(login_url="/login/")
def list_subcontas(request):
    """ Lista SubContas"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            subcontas = Fin_SubConta.objects.all()
            #__icontains sem case sensitive
            subcontas = subcontas.filter(subconta__icontains=termo_pesquisa)
        else:
            subcontas = Fin_SubConta.objects.all()
        dados = {"subcontas": subcontas}
    else:
        raise Http404()

    return render(request, "list_subcontas.html", dados)


# Ven_Fecha_Caixa # Somente o fecha caixa
@login_required(login_url="/login/")
def list_fecha_caixas(request):
    """ Lista SubContas"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            fecha_caixas = Ven_Fecha_Caixa.objects.all()
            #__icontains sem case sensitive
            fecha_caixas = fecha_caixas.filter(
                                    referencial__icontains=termo_pesquisa)
        else:
            fecha_caixas_list = Ven_Fecha_Caixa.objects.filter().order_by(
                '-referencial')
            paginator = Paginator(fecha_caixas_list, 10)
            page = request.GET.get('page')
            fecha_caixas = paginator.get_page(page)
            # fecha_caixas = Ven_Fecha_Caixa.objects.all()
        dados = {"fecha_caixas": fecha_caixas}
    else:
        raise Http404()

    return render(request, "list_fecha_caixas.html", dados)



# Con_Empresa #
@login_required(login_url="/login/")
def list_con_empresas(request):
    """ Lista Con_Empresas"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
         #id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            con_empresas = Con_Empresa.objects.all()
            #__icontains sem case sensitive
            con_empresas = con_empresas.filter(
                            nome__icontains=termo_pesquisa)
        else:
            con_empresas = Con_Empresa.objects.all()
        dados = {"empresas": con_empresas}
    else:
        raise Http404()

    return render(request, "list_con_empresas.html", dados)