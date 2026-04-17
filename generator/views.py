import zipfile
import io
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    if request.method == "POST":
        tech = request.POST.get("tech")
        topic = request.POST.get("topic")

        # Create ZIP in memory
        buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(buffer, 'w')

        if tech == "django":
            # Add files to ZIP
            zip_file.writestr("project/manage.py", "# Django manage file")
            zip_file.writestr("project/app/views.py", f"""
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to {topic}")
""")

        elif tech == "android":
            zip_file.writestr("project/MainActivity.java", f"""
public class MainActivity {{
    protected void onCreate() {{
        System.out.println("{topic}");
    }}
}}
""")

        zip_file.close()

        # Send ZIP to user
        response = HttpResponse(buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={topic}.zip'

        return response

    return render(request, "index.html")