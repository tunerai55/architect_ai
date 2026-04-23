import zipfile
import io
import os

from django.http import HttpResponse
from django.shortcuts import render

from openai import OpenAI

# 🔐 Load API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ==============================
# 🤖 AI CODE GENERATOR
# ==============================
def generate_ai_code(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Django expert. Return ONLY clean code. No explanation, no markdown."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        code = response.choices[0].message.content

        # Clean markdown if any
        return code.replace("```python", "").replace("```", "")

    except Exception as e:
        return f"# Error generating code\n# {str(e)}"


# ==============================
# 📦 BASE DJANGO STRUCTURE
# ==============================
def create_base_project(zip_file, topic):
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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'project.urls'

STATIC_URL = '/static/'

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

    zip_file.writestr("project/requirements.txt", "Django")

    zip_file.writestr("project/README.md", f"""
# {topic}

Run:
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
""")


# ==============================
# 🌐 MAIN VIEW
# ==============================
def home(request):
    if request.method == "POST":
        prompt = request.POST.get("topic")
        action = request.POST.get("action")

        # 🔍 PREVIEW
        if action == "generate":
            preview = generate_ai_code(
                "Explain the architecture and features of this Django project:\n" + prompt
            )
            return render(request, "index.html", {"result": preview})

        # 📥 DOWNLOAD ZIP
        elif action == "download":
            buffer = io.BytesIO()
            zip_file = zipfile.ZipFile(buffer, 'w')

            # 📦 Base project
            create_base_project(zip_file, prompt)

            # 🤖 AI GENERATED FILES
            models = generate_ai_code("Create models.py for: " + prompt)
            views = generate_ai_code("Create views.py for: " + prompt)
            urls = generate_ai_code("Create urls.py for: " + prompt)
            html = generate_ai_code("Create a clean Django HTML template for: " + prompt)

            # 📁 Write files
            zip_file.writestr("project/app/models.py", models)
            zip_file.writestr("project/app/views.py", views)
            zip_file.writestr("project/app/urls.py", urls)
            zip_file.writestr("project/app/templates/home.html", html)

            zip_file.close()

            response = HttpResponse(buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=ai_project.zip'
            return response

    return render(request, "index.html")
