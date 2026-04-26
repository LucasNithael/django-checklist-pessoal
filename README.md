# Django Checklist (Simples)

Projeto Django monolítico com SQLite e autenticação.

## Rodar localmente (sem Docker)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:
- http://127.0.0.1:8000

## Rodar com Docker

```bash
docker build -t django-checklist .
docker run -p 8000:8000 django-checklist
```

Depois rode as migrations dentro do container (recomendado usar docker-compose, mas aqui é simples):

```bash
docker ps
docker exec -it <container_id> python manage.py migrate
docker exec -it <container_id> python manage.py createsuperuser
```

## Funcionalidades

- Login/Logout
- Áreas (categorias) de checklist
- Itens de checklist por área
- Marcar item como concluído
- Cada usuário vê apenas suas próprias áreas/itens
