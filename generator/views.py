from django.shortcuts import render

def home(request):
    if request.method == "POST":
        return render(request, "result.html", {
            "result": {
                "title": "Sample Project",
                "code": "print('Hello World')",
                "explanation": "Basic example",
                "setup": "Run python file"
            }
        })
    return render(request, "index.html")