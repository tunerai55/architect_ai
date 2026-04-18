import zipfile
import io
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    if request.method == "POST":
        tech = request.POST.get("tech")
        topic = request.POST.get("topic")
        action = request.POST.get("action")

        # 👉 GENERATE (preview only)
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

        # 👉 DOWNLOAD ZIP
        elif action == "download":
            buffer = io.BytesIO()
            zip_file = zipfile.ZipFile(buffer, 'w')

            if tech == "django":
                zip_file.writestr("project/manage.py", """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

                zip_file.writestr("project/project/__init__.py", "")

                zip_file.writestr("project/project/settings.py", f"""
SECRET_KEY = 'dummykey'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

MIDDLEWARE = []

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }},
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }}
}}
""")

                zip_file.writestr("project/project/urls.py", f"""
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to {topic}")

urlpatterns = [
    path('', home),
]
""")

                zip_file.writestr("project/project/wsgi.py", """
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
application = get_wsgi_application()
""")

                zip_file.writestr("project/requirements.txt", "Django")

                zip_file.writestr("project/README.md", f"""# {topic}

## Run this project:

1. pip install -r requirements.txt
2. python manage.py runserver
3. Open http://127.0.0.1:8000/
""")

            elif tech == "android":
                zip_file.writestr("project/MainActivity.java", f"""
public class MainActivity {{
    protected void onCreate() {{
        System.out.println("{topic}");
    }}
}}
""")

                zip_file.writestr("project/README.md", f"# {topic}\nAndroid Project")

            zip_file.close()

            response = HttpResponse(buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={topic}.zip'
            return response

    return render(request, "index.html")
