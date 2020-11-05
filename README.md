# Projeto Sistema DevSys
### Autor: Cesar Costa
### Data (versão: 0.4.0): 2020-08-11
##### Aplicação com Ordem de Serviços e Manipulação de Arquivos com Upload para Download.
## Servidor Home Host App Python 3.7 - Django 2.0
##### Servidor teste na plataforma Heroku
##
### Instalação para executar em sua maquina (python 3.7.x):
---
#### com o git instalado execute:
    git clone https://github.com/CesarAugusto88/sistemadevsys.git
#### com a virtualenv instalada (python3 -m venv .venv) e ativada (source .venv/Scripts/activate) execute o comando a seguir para instalar os pacotes do projeto:
    pip install -r requirements-dev.txt
#### Criar arquivo .env com os dados preenchidos:
    SECRET_KEY=
    DEBUG=
    SECRET_EMAIL=
#### Execute os comandos:
    python manage.py makemigrations core
    python manage.py migrate
    python manage.py collectstatic
#### Comando para executar o servidor em sua maquina:
    python manage.py runserver
#### Execute o comando para criar um super usuario:
    python manage.py createsuperuser
---

![GitHub](https://img.shields.io/github/license/CesarAugusto88/sistemadevsys)

##

![GitHub followers](https://img.shields.io/github/followers/CesarAugusto88?%20Follow&style=social)

##

![Twitter Follow](https://img.shields.io/twitter/follow/cesaraugustodem?style=social)

##

![GitHub.io](https://img.shields.io/badge/Github.io-CesarAugusto88.github.io-red)

## Project Leaders

 - [Cesar Costa](https://github.com/cesaraugusto88)
 - Maurílio
 - Fernando
 - Flávia
 - Rogério
