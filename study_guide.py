"""Study guide functions"""
import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from ai_helper import generate_study_guide

study_guide_bp = Blueprint('study_guide', __name__)

@study_guide_bp.route('/generate-study-guide', methods=['POST'])
def handle_generate_study_guide():
    """Generate study guide endpoint"""
    data = request.json
    try:
        use_mock = os.environ.get('USE_MOCK_API', 'False').lower() == 'true'
        if use_mock:
            study_guide = mock_deekseek_api(data)
            success = True
            error = None
        else:
            study_guide, error = generate_study_guide(data)
            success = error is None

        if not success or not study_guide:
            return jsonify({"success": False, "error": error or "Failed to generate study guide"}), 500

        # Directly return the study guide content as text
        return jsonify({"success": True, "content": study_guide})

    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500

def mock_deekseek_api(data):
    """Mock function to generate a study guide based on user input."""
    class_name = data.get('class', 'General')
    unit = data.get('unit', 'Unknown')
    year = data.get('year', 'College')
    details = data.get('details', '')

    study_guide = f"""
        ===== STUDY GUIDE FOR {class_name.upper()} - {unit.upper()} =====
        Year Level: {year}
        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        ===== INTRODUCTION =====
        This study guide covers key concepts from {class_name}, focusing on the {unit} unit.
        {details if details else "No additional details provided."}

        ===== KEY CONCEPTS =====
        1. Main Concept One
        - Detail point
        - Detail point
        - Example application

        2. Main Concept Two
        - Detail point
        - Relationship to other concepts
        - Common misconceptions

        3. Main Concept Three
        - Detail point
        - Historical context
        - Modern applications

        ===== PRACTICE PROBLEMS =====
        1. Problem description
        Solution: Brief explanation

        2. Problem description
        Solution: Brief explanation

        ===== ADDITIONAL RESOURCES =====
        - Recommended textbook chapters
        - Online resources
        - Practice exercises

        ===== CONCLUSION =====
        This study guide was automatically generated to help with your studies.
        Feel free to supplement with your own notes and ask questions if anything is unclear.
    """

    return study_guide
