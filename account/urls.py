from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    #path('registrar/', views.register.as_view(), name='registrar'),
    path('registrar/', views.register, name='registrar'),
    path('cadastro/cliente/submit', views.submit_register_cliente),
    path('cadastro/funcionario/submit', views.submit_register_funcionario),
]
