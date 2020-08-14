from django.contrib import admin
from django.urls import path, re_path
from core import views
from django.views.generic import RedirectView

# do projeto Upload
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 

urlpatterns = [
    # -----------------------------------------------------------------------
    path("admin/", admin.site.urls),
    path("devsys/", views.devsys, name="devsys"),
    # ------------funcionarios-----------------------------------------------
    #Mudar urls para nao criar mais de um funcionario/ no mesmo login

    path("devsys/funcionario", views.dados_funcionario, name="funcionario"),
    path("devsys/lista/<int:id_funcionario>/", views.json_lista_funcionario),
    path("devsys/func/", views.funcionario),
    path("devsys/func/submit", views.submit_funcionario),
    path(
        "devsys/func/delete/<int:id_funcionario>/",
        views.delete_funcionario, name="del_funcionario"
    ),
    # ----------ordem de serviço --------------------------------------------
    path(
        "devsys/ordem-servicos",
        views.lista_ordem_servicos,
        name="ordem-servicos",
    ),
    path(
        "devsys/lista/<int:id_ordem_servico>/", views.json_lista_ordem_servico
    ),
    path("devsys/ordem-servico/", views.ordem_servico, name="ordem-servico"),
    path("devsys/ordem-servico/submit", views.submit_ordem_servico),
    path(
        "devsys/ordem-servico/delete/<int:id_ordem_servico>/",
        views.delete_ordem_servico,
        name="id-ordem-servico",
    ),
    # Upload - Arquivos
    path("devsys/upload/", views.upload, name="upload"),
    path("devsys/arqs/", views.arq_list, name="arq_list"),
    path("devsys/arqs/upload/", views.upload_arq, name="upload_arq"),
    path("devsys/arqs/<int:pk>/", views.delete_arq, name="delete_arq"),
    # Verificar para retirar class/arqs...:
    path(
        "devsys/class/arqs/",
        views.ArqListView.as_view(),
        name="class_arq_list",
    ),
    path(
        "devsys/class/arqs/upload/",
        views.UploadArqView.as_view(),
        name="class_upload_arq",
    ),
    # -----------cliente-----------------------------------------------------
    path("devsys/cliente", views.dados_cliente, name="cliente"),
    path("devsys/lista/<int:id_cliente>/", views.json_lista_cliente),
    path("devsys/clie/", views.cliente),
    path("devsys/clie/submit", views.submit_cliente),
    path("devsys/clie/delete/<int:id_cliente>/", views.delete_cliente, name="del_cliente"),
    # Registrar/cadastrar cliente
    path("devsys/cliente/register", views.register, name="register"),


    # ------------Boletos-Cliente-------------------------------------------
    path("devsys/uploadb/", views.uploadb, name="uploadb"),
    path("devsys/bols/", views.bol_list, name="bol_list"),
    path("devsys/bols/upload/", views.upload_bol, name="upload_bol"),
    path("devsys/bols/<int:pk>/", views.delete_bol, name="delete_bol"),
    # -- Urls com views para listar todos os clientes do banco.
    path("devsys/bols/clientes", views.clientes, name="todos_clientes"),

    # Verificar para retirar class/...:
    path(
        "devsys/class/bols/",
        views.BolListView.as_view(),
        name="class_bol_list",
    ),
    path(
        "devsys/class/bols/upload/",
        views.UploadBolView.as_view(),
        name="class_upload_bol",
    ),
    # --------------redireciona para HOME---------------------------
    path("", views.home, name="home"),
    path("", RedirectView.as_view(url="/home/")),
    path("contato/", views.contact, name="contact"),
    path("sistemas/", views.sistema, name="sistema"),
    # -----------------------------------------------------------------------
    # path('', views.index), #com a função em views
    # Com url normal redireciona para /devsys/
    # Comentado redirect para devsys para usar home
    # path('', RedirectView.as_view(url='/devsys/')),
    path("login/", views.login_user, name="login_user"),
    path("login/submit", views.submit_login),
    path("logout/", views.logout_user, name="logout_user"),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Do projeto Upload. Verificar para DEBUG:
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
