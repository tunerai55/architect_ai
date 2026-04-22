import zipfile
import io
from django.http import HttpResponse
from django.shortcuts import render

def generate_django_project(zip_file, topic, project_type):

    # Base structure
    zip_file.writestr("project/manage.py", """#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
""")

    zip_file.writestr("project/project/__init__.py", "")

    zip_file.writestr("project/project/settings.py", """
SECRET_KEY = 'dummykey'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'app',
]

ROOT_URLCONF = 'project.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
""")

    zip_file.writestr("project/project/urls.py", """
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
]
""")

    zip_file.writestr("project/app/__init__.py", "")

    # 🔥 PROJECT TYPE LOGIC
    if project_type == "auth":
        generate_auth(zip_file, topic)

    elif project_type == "blog":
        generate_blog(zip_file, topic)

    elif project_type == "ecommerce":
        generate_ecommerce(zip_file, topic)

    # Common files
    zip_file.writestr("project/requirements.txt", "Django")

    zip_file.writestr("project/README.md", f"""
# {topic}

Run:
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
""")

def generate_auth(zip_file, topic):

    zip_file.writestr("project/app/urls.py", """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('register/', views.register),
]
""")

    zip_file.writestr("project/app/views.py", """
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('/login/')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')
""")

    zip_file.writestr("project/app/templates/home.html", "<h1>Home</h1>")
    zip_file.writestr("project/app/templates/login.html", "<form method='POST'>{% csrf_token %}<input name='username'><input name='password'><button>Login</button></form>")
    zip_file.writestr("project/app/templates/register.html", "<form method='POST'>{% csrf_token %}<input name='username'><input name='password'><button>Register</button></form>")

def generate_blog(zip_file, topic):

    zip_file.writestr("project/app/models.py", """
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
""")

    zip_file.writestr("project/app/views.py", """
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})
""")

    zip_file.writestr("project/app/urls.py", """
from django.urls import path
from .views import home

urlpatterns = [path('', home)]
""")

    zip_file.writestr("project/app/templates/home.html", """
<h1>Blog</h1>
{% for post in posts %}
<h2>{{ post.title }}</h2>
<p>{{ post.content }}</p>
{% endfor %}
""")

def generate_ecommerce(zip_file, topic):

    zip_file.writestr("project/app/models.py", """
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
""")

    zip_file.writestr("project/app/views.py", """
from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
""")

    zip_file.writestr("project/app/urls.py", """
from django.urls import path
from .views import home

urlpatterns = [path('', home)]
""")

    zip_file.writestr("project/app/templates/home.html", """
<h1>Products</h1>
{% for p in products %}
<h2>{{ p.name }}</h2>
<p>{{ p.price }}</p>
{% endfor %}
""")

def generate_android_project(zip_file, topic):

    zip_file.writestr("project/MainActivity.java", f"""
public class MainActivity {{
    public static void main(String[] args) {{
        System.out.println("{topic}");
    }}
}}
""")

    zip_file.writestr("project/README.md", f"# {topic}\\nAndroid Project")

def home(request):
    if request.method == "POST":
        tech = request.POST.get("tech")
        topic = request.POST.get("topic")
        action = request.POST.get("action")

        # 👉 PREVIEW
        if action == "generate":
            result = f"""
Project: {topic}

Technology: {tech}

Steps:
1. Setup project
2. Create basic structure
3. Add functionality

Sample Output:
Welcome to {topic}
"""
            return render(request, "index.html", {"result": result})

        # 👉 DOWNLOAD
    elif action == "download":
        buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(buffer, 'w')

    if tech == "django":
        project_type = request.POST.get("type")
        generate_django_project(zip_file, topic, project_type)

    elif tech == "android":
        generate_android_project(zip_file, topic)

    zip_file.close()

    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={topic}.zip'
    return response

    return render(request, "index.html")
