import importlib.util
import pytest
from dotenv import load_dotenv
import os
import io
import sys
import sqlite3
from unittest.mock import patch
from datetime import datetime, timedelta
import glob

# Load environment variables from .env file
load_dotenv()

# Define the path to the database
DB_PATH = 'test_results.db'
print(f"Database path: {DB_PATH}")  # Debug print statement

# Initialize the database
def init_db():
    """
    Initialize the SQLite database to store test results.
    Creates a table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS test_results
                 (file_name TEXT PRIMARY KEY,
                  last_run TIMESTAMP,
                  status TEXT,
                  force_run BOOLEAN)''')
    conn.commit()
    conn.close()

init_db()

# Helper function to execute a code string and capture output
def exec_code_string(code_string):
    """
    Execute a given code string and capture its output.
    Returns local variables and the captured output.
    """
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
    """
    Extract and return Python code blocks from an MDX file.
    """
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

# Helper functions for database operations
def get_last_test_status(file_name):
    """
    Retrieve the last test status for a given file from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_run, status, force_run FROM test_results WHERE file_name = ?", (file_name,))
    row = c.fetchone()
    conn.close()
    return row

def update_test_status(file_name, status):
    """
    Update the test status for a given file in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now()
    c.execute('''INSERT OR REPLACE INTO test_results (file_name, last_run, status, force_run)
                 VALUES (?, ?, ?, ?)''', (file_name, now, status, False))
    conn.commit()
    conn.close()

# Check if the test should be run based on the last run time and status
def should_run_test(file_name):
    """
    Determine if a test should be run based on its last run time and status.
    """
    status = get_last_test_status(file_name)
    if status:
        last_run, test_status, force_run = status
        if force_run:
            return True
        if test_status == "success":
            if datetime.now() - datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S.%f') < timedelta(days=2):
                return False
    return True

# Define the path to the snippets directory
SNIPPETS_DIR = os.path.join(os.path.dirname(__file__), "..", "snippets")

# Helper function to get the list of snippet files
def get_snippet_files():
    """
    Retrieve a list of all MDX snippet files in the snippets directory.
    """
    files = glob.glob(os.path.join(SNIPPETS_DIR, "*.mdx"))
    print(f"Discovered snippet files: {files}")  # Debug print statement
    return files

# Logging function to print the test being conducted
def log_test_start(test_name):
    """
    Log the start of a test.
    """
    print(f"\nRunning test: {test_name}\n" + "="*40)

# Parameterized test function
@pytest.mark.parametrize("snippet_file", get_snippet_files())
def test_snippet(snippet_file):
    """
    Run a test for a given snippet file.
    Extracts and executes the code, then updates the test status in the database.
    """
    log_test_start(snippet_file)
    file_name = os.path.basename(snippet_file)
    if not should_run_test(file_name):
        pytest.skip(f"Skipping {file_name} as it was successfully tested recently.")
    
    code_string = extract_code_from_mdx(snippet_file)
    try:
        local_vars, output = exec_code_string(code_string)
        print(output)  # Debug print statement
        update_test_status(file_name, "success")
    except Exception as e:
        update_test_status(file_name, "failure")
        raise e

if __name__ == "__main__":
    pytest.main()
