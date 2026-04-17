# generator/models.py

from django.db import models

class ProjectRequest(models.Model):
    TECHNOLOGY_CHOICES = [
        ('django', 'Django'),
        ('android', 'Android'),
        ('flask', 'Flask'),
    ]

    PROJECT_TYPE = [
        ('web', 'Web App'),
        ('android', 'Android App'),
    ]

    tech_stack = models.CharField(max_length=50, choices=TECHNOLOGY_CHOICES)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE)
    topic = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)