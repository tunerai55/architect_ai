import zipfile
import io
import os
import openai

from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv

# Load env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_ai_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Django expert. Return ONLY clean code. No explanation."
            },
            {"role": "user", "content": prompt}
        ]
    )

    code = response['choices'][0]['message']['content']
    return code.replace("```python", "").replace("```", "")


def home(request):
    if request.method == "POST":
        prompt = request.POST.get("topic")
        action = request.POST.get("action")

        # 🔥 PREVIEW
        if action == "generate":
            preview = generate_ai_code("Explain project: " + prompt)
            return render(request, "index.html", {"result": preview})

        # 🔥 DOWNLOAD ZIP
        elif action == "download":
            buffer = io.BytesIO()
            zip_file = zipfile.ZipFile(buffer, 'w')

            # AI GENERATED FILES
            models = generate_ai_code("Create models.py for: " + prompt)
            views = generate_ai_code("Create views.py for: " + prompt)
            urls = generate_ai_code("Create urls.py for: " + prompt)
            html = generate_ai_code("Create HTML template for: " + prompt)

            # SAVE FILES
            zip_file.writestr("project/app/models.py", models)
            zip_file.writestr("project/app/views.py", views)
            zip_file.writestr("project/app/urls.py", urls)
            zip_file.writestr("project/app/templates/home.html", html)

            zip_file.writestr("project/requirements.txt", "Django")

            zip_file.close()

            response = HttpResponse(buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=ai_project.zip'
            return response

    return render(request, "index.html")
