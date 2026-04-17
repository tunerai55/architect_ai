from django.shortcuts import render
from .services.code_generator import generate_project

def home(request):
    if request.method == "POST":
        tech = request.POST.get("tech")
        project_type = request.POST.get("type")
        topic = request.POST.get("topic")
        difficulty = request.POST.get("difficulty")

        result = generate_project(tech, project_type, topic, difficulty)

        return render(request, "index.html", {"result": result})

    return render(request, "index.html")