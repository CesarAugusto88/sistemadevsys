from auditlog.registry import auditlog
from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string
from devsys import settings


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
    bloqueado = models.CharField(max_length=3)
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
    # varchar 27 para bloquerar
    chave = models.CharField(max_length=27)
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
    equipamento = models.CharField(blank=True, null=True, max_length=255)
    total = models.FloatField(blank=True, null=True)
    inserir_produto = models.CharField(blank=True, null=True, max_length=2)
    sem_comissao = models.CharField(blank=True, null=True, max_length=2)
    comissao = models.CharField(blank=True, null=True, max_length=2)
    ref_caixa = models.IntegerField(blank=True, null=True)
    garantia = models.CharField(blank=True, null=True, max_length=2)
    recebido = models.CharField(blank=True, null=True, max_length=2)
    valor_pro = models.FloatField(blank=True, null=True)
    dt_pagamento = models.DateTimeField(blank=True, null=True)
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
    confirmar = models.BooleanField(default=False)
    finalizar = models.BooleanField(default=False)
    usuario_os = models.ForeignKey(User, on_delete=models.PROTECT)

    # classe Meta serve p/ modificar nomes para plural
    class Meta:
        verbose_name = "Ordem_Servico"
        verbose_name_plural = "Ordem_Servicos"
        # ordenar
        ordering = ["-dt_atualizada"]

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.descricao
    # Entrada
    def get_dt_entrada_os(self):
        """Mostra data de entrada formatada da OS."""
        return self.dt_entrada.strftime("%d/%m/%Y %H h : %M min")

    # Atualizada
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
        """Mostra data pagamento formatada da OS."""
        return self.dt_pagamento.strftime("%d/%m/%Y %H h : %M min")

    def get_pagamento_input_os(self):
        """ Data pagamento OS correta para template."""
        return self.dt_pagamento.strftime("%Y-%m-%dT%H:%M")

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
    #imagem = models.ImageField(upload_to="arq/imagens/", null=True, blank=True)

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
        #self.imagem.delete()
        super().delete(*args, **kwargs)


# Class para boletos upload/dowload
class Bol(models.Model):
    """Boleto/arquivo enviado do funcionário para o cliente."""
    titulo = models.CharField(max_length=30)
    assunto = models.CharField(max_length=50)
    boleto = models.FileField("Boleto/Arquivo", upload_to="bol/boletos/")
    #imagem = models.ImageField(upload_to="bol/imagens/", null=True, blank=True)
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
        #self.imagem.delete()
        super().delete(*args, **kwargs)


# Chamado feito por um cliente
class Chamado(models.Model):
    """Tabela de ordem de serviço com referencia de cliente e funcionário."""
    dt_entrada = models.DateTimeField("Data de Entrada", auto_now=True)
    nome_cliente = models.CharField("Nome do cliente", max_length=30)
    assunto = models.CharField(max_length=50)
    descricao = models.TextField(verbose_name = 'Descrição')
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

    #Emails
    def save(self, *args, **kwargs):
        super(Chamado, self).save(*args, **kwargs)
        data = {
            'cliente': self.nome_cliente, 'descricao': self.descricao, 'funcionario': self.funcionario.nome
        }
        plain_text = render_to_string('emails/cliente.txt', data)
        html_email = render_to_string('emails/cliente.html', data)
        # send_mail(
        #     'Chamado enviado.',
        #     plain_text,
        #     'cesar@devsys.com.br',
        #     ['contato@devsys.com.br', 'cesarcosta.augustos@gmail.com'],
        #     html_message=html_email,
        #     fail_silently=True, #False erro
        # )
        # mail_admins(
        #     'Chamado enviado.',
        #     plain_text,
        #     html_message=html_email,
        #     fail_silently=True, #False erro
        # )
        # print(plain_text)
        subject = "Chamado Enviado/Alterado"
        to = "contato@devsys.com.br"
        send_mail(
            subject, plain_text, settings.EMAIL_HOST_USER, [to], html_email
        )
        mail_admins(
            subject, plain_text, settings.EMAIL_HOST_USER
        )
    
    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        # ordenar
        ordering = ["dt_entrada"]
    
    #delete
    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        super().delete(*args, **kwargs)

    def get_dt_entrada_ch(self):
        """Mostra data de entrada formatada."""
        return self.dt_entrada.strftime("%d/%m/%Y %H h : %M min")

    def __str__(self):
        return f"{self.cliente.nome} {self.funcionario.nome}"


############ VENDAS CAIXA #############################
class Ven_Caixa(models.Model):
    """ Tabela de Vendas do Caixa."""
    referencial = models.IntegerField(null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)
    troco =  models.FloatField(null=True, blank=True)
    ref_fun = models.IntegerField(null=True, blank=True)
    fechado = models.CharField(max_length=1, null=True, blank=True)
    hora_fechamento = models.DateTimeField(null=True, blank=True)
    nome_caixa = models.CharField(max_length=10, null=True, blank=True)
    saldo_final =  models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Venda Caixa"
        verbose_name_plural = "Venda Caixas"
        # ordenar
        ordering = ["-referencial"]

    # data
    def get_dt(self):
        """Mostra data de entrada formatada da OS."""
        return self.data.strftime("%d/%m/%Y Hora: %H:%M")

    def __str__(self):
        return f"{self.data}"


class Ven_Formas(models.Model):
    referencial = models.IntegerField(null=True, blank=True)
    nome = models.CharField(max_length=30, null=True, blank=True)
    tipo = models.CharField(max_length=1, null=True, blank=True)
    prazo = models.IntegerField(null=True, blank=True)
    parcelas = models.IntegerField(null=True, blank=True)
    taxa =  models.FloatField(null=True, blank=True)
    ref_conta = models.IntegerField(null=True, blank=True)
    ref_subconta = models.IntegerField(null=True, blank=True)
    contas_receber = models.IntegerField(null=True, blank=True)
    vl_minimo =   models.FloatField(null=True, blank=True)
    codigo_fiscal = models.IntegerField(null=True, blank=True)
    controle_cheque = models.IntegerField(null=True, blank=True)
    ref_banco = models.IntegerField(null=True, blank=True)
    ref_sic = models.IntegerField(null=True, blank=True)
    emissor = models.CharField(max_length=30, null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    maquina = models.CharField(max_length=50, null=True, blank=True)
    parcelado = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Venda Forma"
        verbose_name_plural = "Venda Formas"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.referencial}"


class Fin_Banco(models.Model):
    """Banco para referencia em Fecha Caixa"""
    referencial = models.IntegerField()
    banco = models.CharField(max_length=30)
    n_banco = models.CharField(max_length=14)
    n_agencia = models.CharField(max_length=14)
    n_conta = models.CharField(max_length=14)
    digito_conta = models.CharField(max_length=1)
    carteira = models.CharField(max_length=2)
    multa_diaria = models.FloatField(null=True, blank=True)
    multa_por_atraso =  models.FloatField(null=True, blank=True)
    mensagem = models.CharField(max_length=240)
    instrucao1 = models.CharField(max_length=240)
    instrucao2 = models.CharField(max_length=240)
    boleto = models.CharField(max_length=3)
    relacao_banco = models.CharField(max_length=80)
    digito_agencia = models.CharField(max_length=1)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.banco}"


class Fin_Conta(models.Model):
    """Conta para referencia em Fecha Caixa"""
    referencial = models.IntegerField()
    conta = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.conta}"



class Fin_SubConta (models.Model):
    """SubConta para referencia em Fecha Caixa"""
    referencial = models.IntegerField()
    ref_conta = models.ForeignKey(
        "Fin_Conta", on_delete=models.PROTECT
        )
    subconta = models.CharField(max_length=30)
    credito =  models.FloatField(null=True, blank=True)
    debito = models.FloatField(null=True, blank=True)
    pagar = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name = "SubConta"
        verbose_name_plural = "SubContas"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.subconta}"


class Ven_Fecha_Caixa(models.Model):
    referencial = models.IntegerField(null=True, blank=True)
    ref_saida = models.IntegerField(null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)
    ref_forma = models.IntegerField(null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    complemento = models.CharField(max_length=40,
                                    null=True, blank=True)
    ref_caixa = models.IntegerField(null=True, blank=True)
    debito =  models.FloatField(null=True, blank=True)
    saldo =  models.FloatField(null=True, blank=True)
    ref_entrada =  models.IntegerField(null=True, blank=True)
    cheque = models.CharField(max_length=10, null=True, blank=True)
    n_documento = models.CharField(
                            max_length=20, null=True, blank=True)
    ref_servicos = models.IntegerField(null=True, blank=True)
    ref_banco = models.IntegerField(null=True, blank=True)
    ref_conta = models.IntegerField(null=True, blank=True)
    ref_subconta = models.IntegerField(null=True, blank=True)
    arquivo_morto = models.CharField(
                            max_length=2, null=True, blank=True)
    codigo_fiscal = models.IntegerField(null=True, blank=True)
    ref_pagar = models.IntegerField(null=True, blank=True)
    val_servicos = models.FloatField(null=True, blank=True)
    val_peca =  models.FloatField(null=True, blank=True)

    desconto =  models.FloatField(null=True, blank=True)
    data_compensado = models.DateTimeField(null=True, blank=True)
    ref_cliente = models.IntegerField(null=True, blank=True)
    troco = models.CharField(max_length=3, null=True, blank=True)
    local = models.CharField(max_length=7, null=True, blank=True)
    ref_subconta2 = models.IntegerField(null=True, blank=True)
    ref_subconta3 = models.IntegerField(null=True, blank=True)
    comissao = models.CharField(max_length=1, null=True, blank=True)
    vl_comissao =  models.FloatField(null=True, blank=True)
    ref_receber = models.IntegerField(null=True, blank=True)
    ref_fun = models.IntegerField(null=True, blank=True)
    ref_cheque = models.IntegerField(null=True, blank=True)
    hora = models.CharField(max_length=8, null=True, blank=True)
    ref_pagamento = models.IntegerField(null=True, blank=True)
    ref_transf_caixa = models.IntegerField(null=True, blank=True)
    ref_setor = models.IntegerField(null=True, blank=True)
    ref_locacao = models.IntegerField(null=True, blank=True)
    ref_pag = models.IntegerField(null=True, blank=True)
    ref_mesa = models.IntegerField(null=True, blank=True)
    ref_garcom = models.IntegerField(null=True, blank=True)
    ref_empresa = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Venda Fecha Caixa"
        verbose_name_plural = "Venda Fecha Caixas"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.referencial}"

    # data
    def get_data(self):
        """Mostra data formatada."""
        return self.data.strftime("%d/%m/%Y")


class Con_Empresa(models.Model):
    referencial = models.IntegerField()
    nome = models.CharField(max_length=60)
    razao_social = models.CharField(max_length=60)
    tipo = models.CharField(max_length=1, null=True, blank=True)

    cnpj = models.CharField(max_length=20)
    ie = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=60, null=True, blank=True)
    bairro = models.CharField(max_length=30, null=True, blank=True)
    ref_cidade = models.IntegerField(null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    site = models.CharField(max_length=60, null=True, blank=True)
    tel1 = models.CharField(max_length=11, null=True, blank=True)
    tel2 = models.CharField(max_length=11, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    numero = models.CharField(max_length=6, null=True, blank=True)
    ref_municipios = models.IntegerField(null=True, blank=True)
    numero_nfe = models.CharField(max_length=16, null=True, blank=True)
    senha_email = models.CharField(max_length=16, null=True, blank=True)
    n_nfe = models.FloatField(null=True, blank=True)
    complemento = models.CharField(max_length=80, null=True, blank=True)
    nfe_regime = models.CharField(max_length=16, null=True, blank=True)
    im = models.CharField(max_length=20, null=True, blank=True)
    cnpj_sft = models.CharField(max_length=20, null=True, blank=True)
    ass_ap_com = models.CharField(max_length=400, null=True, blank=True)
    caminho_xml_gravacao = models.CharField(
        max_length=240, null=True, blank=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        # ordenar
        ordering = ["-referencial"]

    def __str__(self):
        return f"{self.referencial}"


auditlog.register(Funcionario)
auditlog.register(Cliente)
auditlog.register(Ordem_Servico)
auditlog.register(Arq)
auditlog.register(Bol)
auditlog.register(Chamado)
