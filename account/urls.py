from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    #path('registrar/', views.register.as_view(), name='registrar'),
    # Registra USUARIO cliente/funcionario
    path('registrar/cliente', views.register_cliente, name='registrar_cliente'),
    path('cadastro/cadastrar-cliente/', views.cadastrar_cliente, name="cadastrar_cliente"),
    path('registrar/funcionario', views.register_funcionario, name='registrar_funcionario'),
    path('cadastro/cadastrar-funcionario/', views.cadastrar_funcionario, name="cadastrar_funcionario"),
    path('alterar_senha_cliente/', views.alterar_senha_cliente, name='alterar_senha_cliente'),
    path('alterar_senha_funcionario/', views.alterar_senha_funcionario, name='alterar_senha_funcionario'),

    path('reset_password/', auth_views.PasswordResetView.as_view(),
                            name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
                            name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
                            name="password_reset_confirm"),
    path('reset_password_complete/',
                    auth_views.PasswordResetCompleteView.as_view(),
                    name="password_reset_complete"),

]
