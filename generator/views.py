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
                zip_file.writestr("project/manage.py", "# Django manage file")

                zip_file.writestr("project/app/views.py", f"""
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to {topic}")
""")

                zip_file.writestr("project/README.md", f"# {topic}\nDjango Project")

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