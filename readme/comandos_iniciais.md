# Comandos Iniciais para as Configurações Básicas
Você deve ter a versão 3.10 ou superior do Python instalada para rodar este projeto

### COMANDO P/ CRIAR VIRTUALENV
```bash
python3 -m venv venv
```
### COMANDO P/ ATIVAR VIRTUALENV
(WINDOWS)
```bash
.venv/Scripts/activate
```
(MAC / LINUX)
```bash
.venv/bin/activate
```
### COMANDO P/ INCLUIR AS DEPENDÊNCIAS JÁ INSTALADAS NO PROJETO
```bash
pip install -r requirements.txt
```
### COMANDO PARA RODAR AS MIGRAÇÕES
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### COMANDO P/ RODAR (TESTAR) A APLICAÇÃO
```bash
python manage.py runserver
```
