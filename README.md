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
- working with real external APIs
- handling credentials safely in local development
- iterative product development and portfolio documentation

## Current status

This version establishes the foundation:
- Google OAuth login
- Gmail API connection
- reading the user's Gmail labels
- retrieving up to 5 recent inbox messages with sender, date, subject, and preview
- timestamped console and file logs for authentication, API requests, and message-processing steps
- daily log rotation, retaining up to five daily log files in `logs/`
- secure local credential handling via `token.json`

## Tech stack

- Python
- Google Gmail API
- Google OAuth 2.0

## Development tools

- VS Code
- Git and GitHub
- GitHub Copilot Chat

## Project structure

- quickstart.py — initial Gmail authentication and label retrieval
- requirements.txt — Python dependencies for the project
- README.md — project overview and setup instructions
- VERSION_HISTORY.md — version-by-version project progression
- .gitignore — ignores sensitive credentials and local environment files

## How it works

1. The app checks whether a valid token already exists.
2. If no valid token exists, it starts the Google OAuth flow.
3. After approval, Google returns credentials.
4. The script uses the Gmail API to access the user's account.
5. It lists the available Gmail labels as a proof of successful authentication.
6. It retrieves up to 5 recent inbox messages and displays their headers and preview snippets.
7. It logs progress and API errors with timestamps to the terminal and `logs/ai_gmail_agent.log`, without logging message contents.

## Roadmap

Planned milestones for future versions include:
- filtering emails by sender, date, and label
- extracting metadata such as sender, subject, and thread information
- prioritizing important messages based on urgency or sender
- summarizing unread threads for a daily inbox digest
- identifying subscription or promotional emails for review
- classifying messages into categories such as work, personal, and follow-up

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
6. This will print message details in the terminal
7. Timestamped logs are also saved in the `logs/` folder and rotated daily.


## Important security note

Ignored sensitive files using `.gitignore` file; should never be committed to GitHub:
- `credentials.json`
- `token.json`

## Version history

This repo is intentionally structured as an evolving project rather than a single static script, so the GitHub history and [VERSION_HISTORY.md](VERSION_HISTORY.md) show how the project grows as new skills are learned.

