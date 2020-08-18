from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, TemplateView

from core.models import Cliente, Funcionario

""" class register(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('account:registrar')
    template_name = 'register.html' """

@login_required(login_url="/login/")
def register(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('account:registrar')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'register.html', {'form_usuario': form_usuario})


# importar models de cliente e funcionario e cadastrar junto
@login_required(login_url="/login/")
def submit_register_cliente(request):
    if request.POST:
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
        usuario_cli = request.POST.get("usuario_cli")
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
            usuario_cli=usuario_cli,
        )

    """ if request.POST:
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
        usuario_cli = request.POST.get("usuario_cli")
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
            usuario_cli=usuario_cli,
        ) """
    return redirect("/account/registrar")


@login_required(login_url="/login/")
def submit_register_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone1 = request.POST.get("fone1")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")
        usuario = request.user
        Funcionario.objects.create(
            nome=nome,
            fone1=fone1,
            endereco=endereco,
            cidade=cidade,
            cep=cep,
            uf=uf,
            usuario_fun=usuario,
        )
    return redirect("/account/registrar")