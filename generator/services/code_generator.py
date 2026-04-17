def generate_project(tech, project_type, topic, difficulty):
    if tech == "django":
        return f"""
Project: {topic}

Steps:
1. Create Django project
2. Create app
3. Define models
4. Add views

Sample Code:

# views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to {topic}")
"""
    
    elif tech == "android":
        return f"""
Project: {topic}

Steps:
1. Create Android project
2. Design UI in XML
3. Add Java/Kotlin logic

Sample Code:

// MainActivity.java
public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}
"""