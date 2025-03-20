"""Helper module for AI-powered study guide generation."""
import os
from flask import Blueprint
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

ai_helper_blueprint = Blueprint("ai_helper", __name__)



def get_openai_client():
    """Retrieves OpenAI client using the API key from Flask config."""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API Key")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def generate_response(system_prompt, user_prompt):
    """Helper function to generate AI responses using DeepSeek Chat API."""
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content, None
    except Exception as error:  # noqa: W0718 (Still catching general exceptions)
        current_app.logger.error("Unexpected AI Model Error: %s", str(error))
        return None, "An unexpected error occurred."

def generate_study_guide(data):
    """Generate a study guide using the DeepSeek API."""
    class_name = data.get('class', 'General')
    unit = data.get('unit', 'Unknown')
    year = data.get('year', 'College')
    details = data.get('details', '')

    # Check if API key is available
    if not DEEPSEEK_API_KEY:
        return None, "API key not configured. Please set the DEEPSEEK_API_KEY environment variable."

    system_prompt = (
        "You are a professional study guide creator. You create detailed, well-structured study guides for students. "
        "Thoughtfully consider a student's education level, course, and unit/topic to generate an in-depth, relevant study guide. "
        "Ensure that the study guide is appropriate for their education level. "
        "Format the study guide with the following sections, each preceded by '===== SECTION NAME =====' (including the equals signs and spaces):\n"
        "1. INTRODUCTION\n"
        "2. KEY CONCEPTS\n"
        "3. DEFINITIONS\n"
        "4. PRACTICE PROBLEMS\n"
        "5. ADDITIONAL RESOURCES\n"
        "6. CONCLUSION\n\n"
        "Use plain text formatting with clear section headers and bullet points."
        "Use bullet points with '- ' for main points and '   - ' for sub-points (with three spaces before the dash)."
        "Number lists as '1. ', '2. ', etc."
    )

    user_prompt = (
        f"I am a student at the {year} level studying {class_name}. "
        f"I need a study guide for the {unit} unit or topic. "
        f"Additional details: {details}\n\n"
        f"Please generate a comprehensive study guide to help me prepare for my exam or assignment."
    )

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
            stream=False
        )

        content = response.choices[0].message.content

        if not content.strip().startswith("====="):
            formatted_content = f"""
            ===== STUDY GUIDE FOR {class_name.upper()} - {unit.upper()} =====

            {content}
            """
        else:
            formatted_content = content

        return formatted_content, None

    except Exception as error:
        error_msg = f"Error generating study guide: {str(error)}"
        print(error_msg)  # For debugging
        return None, error_msg
