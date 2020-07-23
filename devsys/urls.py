from django.contrib import admin
from django.urls import path
from core import views
from django.views.generic import RedirectView

# do projeto Upload
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Upload
    # Verificar para retirar somente upload sem download:
    path('devsys/upload/', views.upload, name='upload'),
    
    path('devsys/arqs/', views.arq_list, name='arq_list'),
    path('devsys/arqs/upload/', views.upload_arq, name='upload_arq'),
    path('devsys/arqs/<int:pk>/', views.delete_arq, name='delete_arq'),
   
    # Verificar para retirar class/arqs...:
    path('devsys/class/arqs/', views.ArqListView.as_view(), name='class_arq_list'),
    path('devsys/class/arqs/upload/', views.UploadArqView.as_view(), name='class_upload_arq'),

    #-----------------------------------------------------------------------
    path('admin/', admin.site.urls),
    path('devsys/', views.devsys, name='devsys'),
    #------------funcionarios-----------------------------------------------
    path('devsys/funcionarios', views.lista_funcionarios, name='funcionarios'),
    path('devsys/lista/<int:id_funcionario>/', views.json_lista_funcionario),
    path('devsys/funcionario/', views.funcionario),
    path('devsys/funcionario/submit', views.submit_funcionario),
    path('devsys/funcionario/delete/<int:id_funcionario>/', views.delete_funcionario),

    #-----------cliente-----------------------------------------------------
    path('devsys/clientes', views.lista_clientes, name='clientes'),
    path('devsys/lista/<int:id_cliente>/', views.json_lista_cliente),
    path('devsys/cliente/', views.cliente),
    path('devsys/cliente/submit', views.submit_cliente),
    path('devsys/cliente/delete/<int:id_cliente>/', views.delete_cliente),
    
    #----------ordem de serviço --------------------------------------------
    path('devsys/ordem-servicos', views.lista_ordem_servicos, name='ordem-servicos'),
    path('devsys/lista/<int:id_ordem_servico>/', views.json_lista_ordem_servico),
    path('devsys/ordem-servico/', views.ordem_servico, name='ordem-servico'),
    path('devsys/ordem-servico/submit', views.submit_ordem_servico),
    path('devsys/ordem-servico/delete/<int:id_ordem_servico>/', views.delete_ordem_servico, name='id-ordem-servico'),

    #--------------redireciona para HOME---------------------------
    path('', views.home, name='home'),
    path('', RedirectView.as_view(url='/home/')),
    
	path('contato/', views.contact, name='contact'),
    
    #-----------------------------------------------------------------------
    # path('', views.index), #com a função em views
    # Com url normal redireciona para /devsys/
    # Comentado redirect para devsys para usar home
    # path('', RedirectView.as_view(url='/devsys/')),
    path('login/', views.login_user, name='login_user'),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user, name='logout_user'),

]

# Upload - verificar, talvez o código não precise:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)