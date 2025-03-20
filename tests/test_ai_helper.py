import pytest
from unittest.mock import patch, MagicMock
from ai_helper import generate_study_guide, get_openai_client
import ai_helper



@patch('ai_helper.get_openai_client')
def test_generate_study_guide_success(mock_get_openai_client):
    # 1) Create a mock completion response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mock AI content"

    # 2) Mock client so that .chat.completions.create(...) returns that response
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_openai_client.return_value = mock_client

    # 3) Now call generate_study_guide - it won't hit the real API
    content, error = generate_study_guide({
        "class": "Mathematics",
        "unit": "Calculus",
        "year": "University",
        "details": "Derivatives and integrals"
    })

    # 4) Assert what you want
    assert error is None
    assert content is not None
    assert "Mock AI content" in content

@patch('ai_helper.get_openai_client')
def test_generate_study_guide_without_section_headers(mock_get_client):
    """Test study guide generation where API doesn't return proper section headers."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test study guide without proper section headers."
    
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    test_data = {
        'class': 'Literature',
        'unit': 'Shakespeare',
        'year': 'High School',
        'details': 'Romeo and Juliet'
    }
    
    content, error = generate_study_guide(test_data)
    
    assert error is None
    assert "===== STUDY GUIDE FOR LITERATURE - SHAKESPEARE =====" in content
    assert "This is a test study guide without proper section headers." in content

@patch('ai_helper.get_openai_client')
def test_generate_study_guide_failure(mock_get_client):
    """Test study guide generation with API failure."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API connection error")
    mock_get_client.return_value = mock_client
    
    test_data = {
        'class': 'Computer Science',
        'unit': 'Algorithms',
        'year': 'Graduate',
        'details': 'Sorting algorithms'
    }
    
    content, error = generate_study_guide(test_data)
    
    assert content is None
    assert error is not None
    assert "Error generating study guide" in error
    assert "API connection error" in error

@patch('ai_helper.os.environ.get', return_value=None)
def test_get_openai_client_missing_key(mock_env_get):
    """Test get_openai_client when API key is missing."""
    with pytest.raises(ValueError, match="Missing OpenAI API Key"):
        get_openai_client()

@patch('ai_helper.get_openai_client')
def test_generate_study_guide_missing_data(mock_get_client):
    """Test generate_study_guide when required fields are missing."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test study guide without headers."
    
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    test_data = {}  # Missing class, unit, year, and details
    
    content, error = generate_study_guide(test_data)
    
    assert error is None
    assert "===== STUDY GUIDE FOR GENERAL - UNKNOWN =====" in content
    assert "This is a test study guide without headers." in content


@patch('ai_helper.get_openai_client')
def test_generate_study_guide_empty_response(mock_get_client):
    """Test generate_study_guide when API returns an empty response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = ""

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    test_data = {
        'class': 'History',
        'unit': 'World War II',
        'year': 'High School',
        'details': 'Causes and effects of World War II'
    }

    content, error = generate_study_guide(test_data)

    assert error is None
    assert "===== STUDY GUIDE FOR HISTORY - WORLD WAR II =====" in content  # Check if it still formats output properly

