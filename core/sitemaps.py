from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Snippet


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'login_user', 'logout_user', 'home', 'contact', 'sistema',
            'devsys', 'funcionario', 'ordem-servico', 'upload', 'arq_list',
            'upload_arq', 'cliente', 'uploadb', 'bol_list', 'upload_bol',
            'bol_clientes', 'uploadchamado', 'chamado_list', 'criar_chamado',
            'chamado_list_fun', 'list_clientes', 'list_caixas'
            ]

    def location(self, item):
            return reverse(item)


class SnippetSitemap(Sitemap):
    def items(self):
        return Snippet.objects.all()