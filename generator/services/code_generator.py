# generator/services/code_generator.py

def generate_project_code(tech_stack, project_type, topic, difficulty):
    
    prompt = f"""
    Generate a complete {project_type} project using {tech_stack}.
    Topic: {topic}
    Difficulty: {difficulty}

    Include:
    - Full code
    - File structure
    - Explanation
    - Setup instructions
    """

    # For now (mock)
    return {
        "title": topic,
        "code": f"# Sample {tech_stack} project for {topic}",
        "explanation": "This project demonstrates basic functionality.",
        "setup": "Run pip install requirements.txt"
    }