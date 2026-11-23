# AI Gmail Agent

A Python project to explore the Gmail API, OAuth authentication, and practical email automation.

This project started as a basic Gmail quickstart and is intended to evolve over time as I learn more about API integration, automation, and intelligent inbox workflows.

## Project goal

Build a personal Gmail assistant that can:
- authenticate securely with Google
- read inbox data
- filter and organize messages
- extract useful information from email content
- support future AI-assisted summarization and triage

## Skills demonstrated

This project highlights core skills in:
- Python scripting and automation
- Google OAuth 2.0 and secure authentication flows
- Gmail API integration
- command-line interface design and input validation with `argparse`
- searching and retrieving data from an external API
- parsing and formatting structured Gmail API responses
- rule-based message categorization and triage using Gmail labels
- offline unit testing with Python's `unittest` framework
- timestamped application logging and daily log rotation
- handling credentials safely in local development
- Git workflow with feature branches, commits, and pull requests
- iterative product development and portfolio documentation

## Current status

The current version includes:
- Google OAuth login
- Gmail API connection
- retrieving up to 5 recent inbox messages with sender, date, subject, and preview
- searching inbox messages with Gmail query syntax
- optionally retrieving full email bodies and generating summaries with a local Ollama model
- displaying Gmail's important, starred, and unread labels as triage signals
- displaying Gmail's built-in message categories, such as Personal and Promotions
- timestamped console and file logs for authentication, API requests, and message-processing steps
- daily log rotation, retaining up to five daily log files in `logs/`
- secure OAuth token storage in the Git-ignored `token.json`

## Tech stack

- Python
- Google Gmail API
- Google OAuth 2.0
- Ollama local HTTP API (optional, for AI summaries)

## Development tools

- VS Code
- Git and GitHub
- GitHub Copilot Chat

## Project structure

- quickstart.py — initial Gmail authentication and message detail retrieval
- requirements.txt — Python dependencies for the project
- tests/test_quickstart.py — offline tests for command-line options, full-body extraction, Ollama requests, triage flags, categories, and message formatting
- README.md — project overview and setup instructions
- VERSION_HISTORY.md — version-by-version project progression
- .gitignore — ignores sensitive credentials and local environment files

## How it works

1. The app checks whether a valid token already exists.
2. If no valid token exists, it starts the Google OAuth flow.
3. After approval, Google returns credentials.
4. The script requests recent inbox messages using the Gmail API with read-only access to Gmail data.
5. After Gmail successfully responds, the app logs a confirmation that API access is working.
6. It retrieves up to 5 recent inbox messages and displays key details.
7. It logs progress and API errors with timestamps to the terminal and `logs/ai_gmail_agent.log`, without logging message contents.
8. When `--summarize` is selected, it retrieves each full message, extracts readable text (not attachments), and sends that body to the selected Ollama model through the local Ollama service. Without that option, it continues using Gmail's snippet.

## Roadmap

### Next version: agentic actions

The next milestone is to use email summaries to suggest useful actions, such as creating a follow-up task or preparing a reply draft. Actions that change Gmail or other data should require the user's explicit review and approval before execution.

Other planned milestones include:
- extracting thread metadata for more useful triage
- prioritizing important messages based on urgency or sender
- identifying subscription or promotional emails for review
- adding custom categories such as Work and Follow-up alongside Gmail's built-in categories
- building an inbox analytics dashboard showing counts by label and category, triage totals, and daily or weekly email-volume trends

## Local setup

This project can run without a virtual environment, but using one is recommended for cleaner dependency management.

1. Optionally create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```
> A virtual environment is not strictly required for a small learning project, but it helps keep dependencies isolated and avoids conflicts with other Python work on your machine.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download your Google OAuth `credentials.json` file from Google Cloud Console.

4. Place it in the project root.

5. Run the script:

```bash
python quickstart.py
```
Results:
This will print message details in the terminal.

Timestamped logs are also saved in the `logs/` folder and rotated daily.

To search within the inbox, pass Gmail search syntax with `--query`. For example, `python quickstart.py --query "from:person@example.com after:2026/01/01 is:unread" --max-results 10` searches by sender, date, and unread status. Gmail search terms can be combined; see Google's Gmail search operators for more options.

### Optional: local AI email summaries with Ollama

The summary feature uses Ollama's local HTTP API and Python's standard library; it does not add a Python package or send email content to a hosted AI service. Full message bodies are fetched from Gmail only when `--summarize` is used.

1. Install Ollama for Windows from [ollama.com/download](https://ollama.com/download) if it is not already installed.
2. In PowerShell, run `ollama list` and choose one of your installed models. If needed, download one with `ollama pull MODEL_NAME`.
3. Make sure Ollama is running locally. The Windows app normally starts the service; if it is not running, start it with `ollama serve`.
4. Run a small test using the model name shown by `ollama list`:

```bash
python quickstart.py --summarize --model "YOUR_MODEL_NAME" --query "is:unread" --max-results 1
```

Replace `YOUR_MODEL_NAME` with the exact installed model name. You can also omit `--query` or change the Gmail search criteria. Summarization is opt-in; regular runs still fetch only message metadata and display Gmail snippets. If Ollama is unavailable or the model name is invalid, the command reports the error.

Run the offline tests with `python -m unittest discover -s tests`. Add test names to the output using `python -m unittest discover -s tests -v`.

## Important security and privacy notes

The `.gitignore` excludes local OAuth credentials and logs from new Git changes:
- `credentials.json` — Google OAuth client configuration
- `token.json` — saved OAuth access/refresh credentials
- `logs/` — local application logs

The app stores OAuth credentials as JSON files in the project folder; `.gitignore` does not encrypt them. Protect access to your Windows account and do not share these files.

With `--summarize`, the full readable email body is sent to Ollama at `localhost` on your computer. This project does not intentionally send the body to a hosted AI service or write it to its logs. Keep Ollama bound to the local machine; exposing its service to a network could expose email content. Summaries are generated output and may be inaccurate.

Before publishing, review `git status` and confirm `credentials.json`, `token.json`, and `logs/` are not tracked (`git ls-files credentials.json token.json logs/`). `.gitignore` prevents untracked local files from being added accidentally, but it does not remove a file that was already committed or erase it from Git history. Do not publish email bodies, summaries, OAuth tokens, or credentials.

## Version history

This repo is intentionally structured as an evolving project rather than a single static script, so the GitHub history and [VERSION_HISTORY.md](VERSION_HISTORY.md) show how the project grows as new skills are learned.
