🛒 Projeto LOJA

Django + Django REST Framework + React + JavaScript

Projeto de loja virtual utilizando Django no backend e React (JS) no frontend, com comunicação via API REST.

📦 Tecnologias
Python
Django
Django REST Framework
django-cors-headers
Frontend
Node.js
npm
React
JavaScript
Mantine

⚙️ Instalação e Configuração
🔹 Backend (Django)

Instale as dependências necessárias:

pip install django
pip install djangorestframework
pip install django-cors-headers

<<<<<<< HEAD:api/api/README.md
set PATH=C:\node;%PATH%
node -v
npm run 

pip install djangorestframework djangorestframework-simplejwt
=======

Configure o Django para permitir acesso do frontend (CORS):

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True


Execute o servidor:

python manage.py migrate
python manage.py runserver
>>>>>>> bd5df0635a2a2a3f98b7dee2e15c62868fe0e71c:README.md
