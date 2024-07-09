# Test Suite for Hello World Guides

This test suite is designed to automatically test all code snippets in the `snippets` directory. The suite extracts and executes code from MDX files, checks their functionality, and logs the results. It uses an SQLite database to track the last test run status and timestamps, skipping tests that have been successfully tested within the last 2 days, unless forced to run.

## Directory Structure

```
hello-world-guides-mintlify/
│
├── snippets/
│   ├── assemblyai-lemur-example-snippet.mdx
│   ├── assemblyai-transcription-example-snippet.mdx
│   ├── download-youtube-video-snippet.mdx
│   ├── fetch-plausible-analytics-snippet.mdx
│   ├── langchain-openai-snippet.mdx
│   ├── openai-hello-world-snippet.mdx
│   ├── resend-example-snippet.mdx
│   ├── transcribe-mp3-streamlit-snippet.mdx
│   └── twilio-sms-snippet.mdx
│
├── test-suite/
│   ├── test_all_files.py
│   ├── requirements.txt
│   ├── setup_test_db.py
│   └── test_results.db
│
└── README.md
```

## Prerequisites

- Python 3.7+
- Required Python packages (listed in `requirements.txt`)

## Setup

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/hello-world-guides-mintlify.git
cd hello-world-guides-mintlify/test-suite
```

2. **Install the required packages:**

```sh
pip install -r requirements.txt
```

3. **Set up the SQLite database:**

Run the `setup_test_db.py` script to initialize the database.

```sh
python setup_test_db.py
```

## Running the Tests

Run the `test_all_files.py` script to execute the test suite.

```sh
python test_all_files.py
```

This script will:

- Extract code from each MDX file in the `snippets` directory.
- Execute the code and capture the output.
- Log the results in the SQLite database.
- Skip tests that were successfully tested within the last 2 days, unless the `force_run` flag is set to `True`.

## Understanding the Test Script

The `test_all_files.py` script includes the following key functions:

- **`exec_code_string(code_string)`**: Executes the extracted code string and captures the output.
- **`extract_code_from_mdx(file_path)`**: Extracts Python code from the MDX file.
- **`get_last_test_status(file_name)`**: Retrieves the last test status from the database.
- **`update_test_status(file_name, status)`**: Updates the test status in the database.
- **`should_run_test(file_name)`**: Determines if a test should be run based on the last run time and status.
- **`get_snippet_files()`**: Retrieves the list of MDX snippet files from the `snippets` directory.
- **`log_test_start(test_name)`**: Logs the start of each test.

## Adding New Snippets

To add new snippets to the test suite:

1. Add your MDX file to the `snippets` directory.
2. Ensure the code block in the MDX file is properly formatted and surrounded by triple backticks (```).
3. Run the test suite to validate the new snippet.

## Contributing

If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.