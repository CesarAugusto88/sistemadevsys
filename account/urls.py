from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    #path('registrar/', views.register.as_view(), name='registrar'),
    # Registra USUARIO cliente/funcionario
    path('alterar_senha_cliente/', views.alterar_senha_cli, name='alterar_senha_cli'),
    path('alterar_senha_funcionario/', views.alterar_senha_fun, name='alterar_senha_fun'),
    path('registrar/clie', views.register_clie, name='registrar_cliente'),
    path('registrar/func', views.register_func, name='registrar_funcionario'),
    path('cadastro/cliente', views.register_cliente, name='cad_cliente'),
    path('funcionario', views.register_funcionario, name='cad_funcionario'),
    path('cadastro/submit', views.submit_register_cliente),
    path('submit', views.submit_register_funcionario),
]
