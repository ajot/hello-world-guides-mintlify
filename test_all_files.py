import importlib.util
import pytest
from dotenv import load_dotenv
import os
import io
import sys
from unittest.mock import patch

# Load environment variables from .env file
load_dotenv()

# Helper function to execute a code string and capture output
def exec_code_string(code_string):
    local_vars = {}
    globals_dict = {
        "os": os,
        "load_dotenv": load_dotenv,
        "aai": importlib.import_module("assemblyai"),
        "st": importlib.import_module("streamlit"),
        "requests": importlib.import_module("requests"),
        "datetime": importlib.import_module("datetime"),
        "timedelta": importlib.import_module("datetime").timedelta,
        "YouTube": importlib.import_module("pytube").YouTube,
        "ChatOpenAI": importlib.import_module("langchain_openai").ChatOpenAI,
        "ChatPromptTemplate": importlib.import_module("langchain_core.prompts").ChatPromptTemplate,
    }
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code_string, globals_dict, local_vars)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return local_vars, output

# Helper function to extract code from .mdx file
def extract_code_from_mdx(file_path):
    code_lines = []
    in_code_block = False
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith("```python"):
                in_code_block = True
            elif line.strip() == "```":
                in_code_block = False
            elif in_code_block:
                code_lines.append(line)
    return ''.join(code_lines)

# Define the paths to your snippet files
SNIPPET_FILES = {
    "resend_email": "snippets/resend-example-snippet.mdx",
    "transcribe_mp3": "snippets/transcribe-mp3-streamlit-snippet.mdx",
    "fetch_plausible_analytics": "snippets/fetch-plausible-analytics-snippet.mdx",
    "download_youtube_video": "snippets/download-youtube-video-snippet.mdx",
    "langchain_openai": "snippets/langchain-openai-snippet.mdx"
}

# Tests
def test_resend_email():
    """
    Test sending an email using the Resend API.

    Success Criteria:
    - The email is sent successfully.
    - The response contains an 'id' indicating the email was sent.

    Why:
    To ensure that the Resend API integration is working correctly.
    """
    code_string = extract_code_from_mdx(SNIPPET_FILES["resend_email"])
    local_vars, output = exec_code_string(code_string)
    # Print the captured output for debugging
    print(output)
    # Assert that email was sent (check if 'id' is in response)
    assert 'response' in local_vars and 'id' in local_vars['response']

def test_transcribe_mp3():
    """
    Test transcribing an MP3 audio file using the AssemblyAI API.

    Success Criteria:
    - The audio file is transcribed successfully.
    - The transcription contains one or more paragraphs.

    Why:
    To ensure that the AssemblyAI transcription integration is working correctly.
    """
    code_string = extract_code_from_mdx(SNIPPET_FILES["transcribe_mp3"])
    local_vars, output = exec_code_string(code_string)
    # Print the captured output for debugging
    print(output)
    # Call the transcribe function directly for testing
    paragraphs = local_vars['transcribe_audio']("https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3")
    # Assert that transcription was successful
    assert len(paragraphs) > 0

def test_fetch_plausible_analytics():
    """
    Test fetching analytics data from the Plausible API.

    Success Criteria:
    - The analytics data is fetched successfully.
    - The data contains the 'results' key.
    - The 'results' key contains 'visitors' data.

    Why:
    To ensure that the Plausible API integration is working correctly.
    """
    code_string = extract_code_from_mdx(SNIPPET_FILES["fetch_plausible_analytics"])
    local_vars, output = exec_code_string(code_string)
    # Print the captured output for debugging
    print(output)
    # Assert that analytics data was fetched successfully
    assert 'data' in local_vars
    assert 'results' in local_vars['data']
    assert 'visitors' in local_vars['data']['results']

def test_download_youtube_video():
    """
    Test downloading a YouTube video using the Pytube library.

    Success Criteria:
    - The video is downloaded successfully.
    - The output indicates the title of the video and a success message.

    Why:
    To ensure that the Pytube integration for downloading videos is working correctly.
    """
    code_string = extract_code_from_mdx(SNIPPET_FILES["download_youtube_video"])
    local_vars, output = exec_code_string(code_string)
    # Mock input to provide a YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    with patch('builtins.input', return_value=youtube_url):
        # Capture print output during the function call
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            # Call the download function directly for testing
            local_vars['download_youtube_video'](youtube_url)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    # Print the captured output for debugging
    print(output)
    # Assert that video was downloaded (check for expected output in print statements)
    assert "Download completed!" in output

def test_langchain_openai():
    """
    Test interacting with the OpenAI API using LangChain.

    Success Criteria:
    - The OpenAI API call is made successfully.
    - The response contains the expected output from the LangChain model.

    Why:
    To ensure that the LangChain and OpenAI integration is working correctly.
    """
    code_string = extract_code_from_mdx(SNIPPET_FILES["langchain_openai"])
    local_vars, output = exec_code_string(code_string)
    # Print the captured output for debugging
    print(output)
    # Assert that OpenAI API interaction was successful (check for expected response in output)
    assert "Seinfeld" in output

if __name__ == "__main__":
    pytest.main()
