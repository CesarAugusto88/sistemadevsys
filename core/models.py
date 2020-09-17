from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class DevSysManager(models.Manager):
    # usar search()
    def search(self, query):
        # return self.get_queryset().all()
        # busca com logico E. por padrão vírgula ',' é E
        # return self.get_queryset().filter(
        # 	name__icontains=query, description__icontains=query)
        # busca OU
        return self.get_queryset().filter(
            models.Q(dt_entrada__icontains=query)
            | models.Q(dt_agenda__icontains=query)
            | models.Q(descricao__icontains=query)
        )


class Funcionario(models.Model):
    """ Tabela para cadastro com as informações do funcionário."""

    referencial = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=20)
    rg = models.CharField(blank=True, null=True, max_length=20)
    salario = models.FloatField(blank=True, null=True)
    cargo = models.CharField(blank=True, null=True, max_length=20)
    endereco = models.CharField(max_length=60)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.EmailField(null=False, blank=False)
    endereco_co = models.CharField(blank=True, null=True, max_length=60)
    bairro_co = models.CharField(blank=True, null=True, max_length=30)
    cidade_co = models.CharField(blank=True, null=True, max_length=30)
    cep_co = models.CharField(blank=True, null=True, max_length=9)
    uf_co = models.CharField(blank=True, null=True, max_length=2)
    obs = models.CharField(blank=True, null=True, max_length=80)
    senha = models.CharField(blank=True, null=True, max_length=16)
    fone1 = models.CharField(max_length=16)
    fone2 = models.CharField(blank=True, null=True, max_length=20)
    porcentagem = models.FloatField(blank=True, null=True)
    desconto = models.FloatField(blank=True, null=True)
    ativo = models.SmallIntegerField(blank=True, null=True)
    dt_admissao = models.DateTimeField(blank=True, null=True)
    dt_nascimento = models.DateTimeField(blank=True, null=True)
    nome_comp = models.CharField(blank=True, null=True, max_length=160)
    ref_cidade = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_fun = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        # ordenar
        ordering = ["nome"]

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


class Cliente(models.Model):
    """ Tabela para cadastro com as informações do cliente."""

    referencial = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=60)
    razao_social = models.CharField(max_length=60)
    tipo_pessoa = models.CharField(max_length=1)
    cpf_cnpj = models.CharField(max_length=20)
    rg_ie = models.CharField(max_length=20)
    endereco = models.CharField(max_length=60)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    ref_cidade = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=9)
    uf = models.CharField(max_length=2)
    email = models.EmailField(null=False, blank=False)
    endereco_co = models.CharField(blank=True, null=True, max_length=60)
    bairro_co = models.CharField(blank=True, null=True, max_length=30)
    cidade_co = models.CharField(blank=True, null=True, max_length=30)
    cep_co = models.CharField(blank=True, null=True, max_length=9)
    uf_co = models.CharField(blank=True, null=True, max_length=2)
    obs = models.CharField(blank=True, null=True, max_length=80)
    senha = models.CharField(blank=True, null=True, max_length=16)
    fone1 = models.CharField(max_length=16)
    fone2 = models.CharField(blank=True, null=True, max_length=20)
    contato = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    estado = models.CharField(blank=True, null=True, max_length=2)
    celular = models.CharField(blank=True, null=True, max_length=16)
    desconto = models.FloatField(blank=True, null=True)
    etiquetas = models.FloatField(blank=True, null=True)
    dt_nascimento = models.DateTimeField(blank=True, null=True)
    dt_cadastro = models.DateTimeField(blank=True, null=True)
    ref_escola = models.IntegerField(blank=True, null=True)
    ref_clisubgrupo = models.IntegerField(blank=True, null=True)
    valor_permitido = models.FloatField(blank=True, null=True)
    dias_vencimento = models.FloatField(blank=True, null=True)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    fax = models.CharField(blank=True, null=True, max_length=16)
    contato2 = models.CharField(blank=True, null=True, max_length=30)
    complemento_co = models.CharField(blank=True, null=True, max_length=30)
    fax_r = models.CharField(blank=True, null=True, max_length=16)
    fone1_r = models.CharField(blank=True, null=True, max_length=16)
    fone2_r = models.CharField(blank=True, null=True, max_length=16)
    bloqueado = models.CharField(blank=True, null=True, max_length=3)
    funcionario_cadastrou = models.IntegerField(blank=True, null=True)
    ativo = models.SmallIntegerField(blank=True, null=True)
    endereco_out = models.CharField(blank=True, null=True, max_length=60)
    bairro_out = models.CharField(blank=True, null=True, max_length=30)
    cidade_out = models.CharField(blank=True, null=True, max_length=30)
    cep_out = models.CharField(blank=True, null=True, max_length=9)
    uf_out = models.CharField(blank=True, null=True, max_length=2)
    numero = models.CharField(blank=True, null=True, max_length=6)
    ref_municipios = models.IntegerField(blank=True, null=True)
    ref_terceiros = models.IntegerField(blank=True, null=True)
    maladireta = models.CharField(blank=True, null=True, max_length=3)
    ref_religiao = models.IntegerField(blank=True, null=True)
    ref_estado_civil = models.IntegerField(blank=True, null=True)
    ref_sacramento = models.IntegerField(blank=True, null=True)
    ref_banco = models.IntegerField(blank=True, null=True)
    agencia = models.CharField(blank=True, null=True, max_length=10)
    dv = models.CharField(blank=True, null=True, max_length=3)
    conta = models.CharField(blank=True, null=True, max_length=16)
    dv_conta = models.CharField(blank=True, null=True, max_length=3)
    valor_debito = models.FloatField(blank=True, null=True)
    dia_debito = models.DateTimeField(blank=True, null=True)
    dia_venc = models.DateTimeField(blank=True, null=True)
    ref_endereco = models.CharField(blank=True, null=True, max_length=240)
    ref_vendedor = models.IntegerField(blank=True, null=True)
    dt_ultima_venda = models.DateTimeField(blank=True, null=True)
    simples_nacional = models.CharField(blank=True, null=True, max_length=3)
    ref_pesquisa = models.IntegerField(blank=True, null=True)
    comissao = models.CharField(blank=True, null=True, max_length=3)
    email2 = models.EmailField(null=True, blank=True)
    sexo = models.CharField(blank=True, null=True, max_length=9)
    nacionalidade = models.CharField(blank=True, null=True, max_length=40)
    cidade_nasci = models.CharField(blank=True, null=True, max_length=120)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    numero_co = models.CharField(blank=True, null=True, max_length=6)
    porc_desconto = models.FloatField(blank=True, null=True)
    aviso_sobre_produtos = models.CharField(
        blank=True, null=True, max_length=3
    )
    estado_civil = models.CharField(blank=True, null=True, max_length=15)
    senha = models.CharField(blank=True, null=True, max_length=6)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_cli = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        # ordenar
        ordering = ["nome"]

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


class Ordem_Servico(models.Model):
    """Tabela de ordem de serviço com referencia de cliente e funcionário."""

    referencial = models.IntegerField(blank=True, null=True)
    # ref_cliente = models.IntegerField()
    # ref_funcionario = models.IntegerField()
    # Criado foreinkey - Arrumar para aceitar nos templates
    ref_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name="Cliente",
        blank=True,
        null=True,
    )
    ref_funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        verbose_name="Funcionário",
        blank=True,
        null=True,
    )
    dt_entrada = models.DateTimeField("Data de Entrada", auto_now_add=True)
    dt_atualizada = models.DateTimeField("Data Atualizada", auto_now=True)
    valor = models.FloatField(blank=True, null=True)
    descricao = models.CharField(max_length=255)
    efetuado = models.CharField(blank=True, null=True, max_length=255)
    ref_status = models.IntegerField(blank=True, null=True)
    ref_setor = models.IntegerField(blank=True, null=True)
    dt_agenda = models.DateTimeField(verbose_name="Data Agendada")
    horario = models.CharField(blank=True, null=True, max_length=12)
    equipamento = models.CharField(blank=True, null=True, max_length=60)
    total = models.FloatField(blank=True, null=True)
    inserir_produto = models.CharField(blank=True, null=True, max_length=2)
    sem_comissao = models.CharField(blank=True, null=True, max_length=2)
    comissao = models.CharField(blank=True, null=True, max_length=2)
    ref_caixa = models.IntegerField(blank=True, null=True)
    garantia = models.CharField(blank=True, null=True, max_length=2)
    recebido = models.CharField(blank=True, null=True, max_length=2)
    valor_pro = models.FloatField(blank=True, null=True)
    dt_pagamento = models.DateField(blank=True, null=True)
    data_entrada = models.DateTimeField(blank=True, null=True)
    marca = models.CharField(blank=True, null=True, max_length=20)
    modelo = models.CharField(blank=True, null=True, max_length=20)
    ref_marca = models.IntegerField(blank=True, null=True)
    ref_modelo = models.IntegerField(blank=True, null=True)
    ref_fornecedor = models.IntegerField(blank=True, null=True)
    n_nota = models.CharField(blank=True, null=True, max_length=40)
    dt_nota = models.DateTimeField(blank=True, null=True)
    n_serie = models.CharField(blank=True, null=True, max_length=30)
    aprovado = models.CharField(blank=True, null=True, max_length=3)
    dt_conclusao = models.DateTimeField(blank=True, null=True)
    data_servicos = models.DateTimeField(blank=True, null=True)
    responsavel = models.CharField(blank=True, null=True, max_length=50)
    ref_fun2 = models.IntegerField(blank=True, null=True)
    uso = models.CharField(blank=True, null=True, max_length=3)
    nao_autorizado = models.CharField(blank=True, null=True, max_length=3)
    solucao = models.CharField(blank=True, null=True, max_length=80)
    ref_prioridade = models.IntegerField(blank=True, null=True)
    dt_finalizacao = models.DateTimeField(blank=True, null=True)
    km_atual = models.FloatField(blank=True, null=True)
    fone_resp = models.CharField(blank=True, null=True, max_length=16)
    solucao = models.CharField(blank=True, null=True, max_length=80)
    ref_cor = models.IntegerField(blank=True, null=True)
    sinal = models.FloatField(blank=True, null=True)
    placa = models.CharField(blank=True, null=True, max_length=8)
    desconto = models.FloatField(blank=True, null=True)
    ref_animal = models.IntegerField(blank=True, null=True)
    ref_terceiro = models.IntegerField(blank=True, null=True)
    hr_entrega = models.CharField(blank=True, null=True, max_length=5)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_os = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p/ modificar nomes para plural
    class Meta:
        verbose_name = "Ordem_Servico"
        verbose_name_plural = "Ordem_Servicos"
        # ordenar
        ordering = ["dt_atualizada"]

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.descricao
    #Entrada
    def get_dt_entrada_os(self):
        """Mostra data de entrada formatada da OS."""
        return self.dt_entrada.strftime("%d/%m/%Y %H h : %M min")

    #Atualizada
    def get_dt_atualizada_os(self):
        """Mostra data atualizada formatada da OS."""
        return self.dt_atualizada.strftime("%d/%m/%Y %H h : %M min")

    def get_dt_agenda_os(self):
        """Mostra data agendada formatada da OS."""
        return self.dt_agenda.strftime("%d/%m/%Y %H h : %M min")

    def get_agenda_input_os(self):
        """ Data agendada de OS correta para template."""
        return self.dt_agenda.strftime("%Y-%m-%dT%H:%M")

    def get_dt_pagamento_os(self):
        """Mostra data do pagamento formatada da OS."""
        return self.dt_agenda.strftime("%d/%m/%Y")

    def get_pagamento_input_os(self):
        """ Entrada da data do pagamento da OS correta para template."""
        return self.dt_agenda.strftime("%Y-%m-%d")

    def get_ordem_servico_atrasada(self):
        """ Mostra datas agendadas atrasadas em cor vermelha 
        no devsys-ordemservicos.html"""
        if self.dt_agenda < datetime.now():
            return True
        else:
            return False


# Class para arquivos upload/dowload
class Arq(models.Model):
    titulo = models.CharField(max_length=30)
    assunto = models.CharField(max_length=50)
    arquivo = models.FileField(upload_to="arq/aquivos/")
    imagem = models.ImageField(upload_to="arq/imagens/", null=True, blank=True)

    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        # ordenar
        ordering = ["titulo"]

    def __str__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        self.imagem.delete()
        super().delete(*args, **kwargs)


# Class para boletos upload/dowload
class Bol(models.Model):
    titulo = models.CharField(max_length=30)
    assunto = models.CharField(max_length=50)
    boleto = models.FileField(upload_to="bol/boletos/")
    imagem = models.ImageField(upload_to="bol/imagens/", null=True, blank=True)
    # referência para cada Cliente ter seus proprios boletos
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.PROTECT, related_name='boletos'
        )

    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"
        # ordenar
        ordering = ["titulo"]

    def __str__(self):
        return self.cliente.nome

    def delete(self, *args, **kwargs):
        self.boleto.delete()
        self.imagem.delete()
        super().delete(*args, **kwargs)


# Chamado feito por um cliente
class Chamado(models.Model):
    """Tabela de ordem de serviço com referencia de cliente e funcionário."""
    dt_entrada = models.DateTimeField("Data de Entrada", auto_now=True)
    titulo = models.CharField(max_length=30)
    assunto = models.CharField(max_length=50)
    descricao = models.CharField(max_length=254)
    arquivo = models.FileField(
        upload_to="chamado/arquivos/", null=True, blank=True
        )
    # referência do cliente para o funcionário dos chamados
    funcionario = models.ForeignKey(
        "Funcionario", on_delete=models.PROTECT, related_name='funcionario'
        )
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.PROTECT, related_name='cliente'
        )
    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        # ordenar
        ordering = ["dt_entrada"]

    def __str__(self):
        return f"{self.cliente.nome}{self.funcionario.nome}"

    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        super().delete(*args, **kwargs)

    def get_dt_entrada_ch(self):
        """Mostra data de entrada formatada."""
        return self.dt_entrada.strftime("%d/%m/%Y %H h : %M min")




""" Para cadastrar visitantes e por FOTOS...
class Visitante(models.Model):
    referencial = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=20)
    rg = models.CharField(blank=True, null=True, max_length=20)
    dt_nascimento = models.DateTimeField(blank=True, null=True)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    endereco = models.CharField(max_length=60)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    ref_cidade = models.IntegerField(blank=True, null=True)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.CharField(blank=True, null=True, max_length=60)
    endereco_co = models.CharField(blank=True, null=True, max_length=60)
    bairro_co =  models.CharField(blank=True, null=True, max_length=30)
    cidade_co = models.CharField(blank=True, null=True, max_length=30)
    cep_co = models.CharField(blank=True, null=True, max_length=9)
    uf_co = models.CharField(blank=True, null=True, max_length=2)
    obs = models.CharField(blank=True, null=True, max_length=80)
    senha = models.CharField(blank=True, null=True, max_length=16)
    fone1 = models.CharField(max_length=16)
    fone2 = models.CharField(blank=True, null=True, max_length=20)
    ativo = models.SmallIntegerField(blank=True, null=True)
    nome_comp = models.CharField(blank=True, null=True, max_length=160)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_vis = models.ForeignKey(User, on_delete=models.CASCADE)


    # classe Meta serve p/ modificar nomes para plurar(criei no plural)
    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        #ordenar
        ordering = ['nome']


    def __str__(self):

        return self.nome """
