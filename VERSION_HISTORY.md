# Version History
This file documents the progression of the project so the GitHub repository shows a clear learning timeline.

## Portfolio note
The goal is not just to build one script, but to show steady growth in practical software engineering over time.

## v0.1 - Initial Gmail API setup, secure project configuration, and documentation

### Added
- Python project created for Gmail API experimentation
- Google OAuth setup using `google-auth-oauthlib`
- Gmail API client connection
- script to authenticate and access Gmail labels
- `.gitignore` rules to protect `credentials.json` and `token.json`
- `README.md` overview and project rationale
- `VERSION_HISTORY.md` tracking file for portfolio progress

### Purpose
- establish a working Gmail API foundation
- confirm OAuth and API access work correctly
- protect secrets before publishing the project
- present the project as a clean portfolio artifact

### Notes
- this is the baseline version of the project
- it demonstrates secure integration with a real external API
- the project is now structured for safe public sharing and clearer documentation


## v0.2 - Read recent messages and display previews

### Added
- retrieve up to 5 recent messages from the inbox
- request sender, date, and subject metadata from Gmail
- display each message with its headers and preview snippet
- add timestamped logs for authentication, API requests, and message processing
- save logs to a daily rotating file and retain up to five daily log files
- retain the existing Gmail label listing

### Purpose
- expand the Gmail API integration from labels to recent inbox messages
- present useful message information in a readable format
- make it easier to locate failures with logging

## Planned future versions

### v0.3 - Filter emails by sender or date
- add email search and filtering logic
- improve message triage capabilities

### v0.4 - Message categorization
- sort messages into priority buckets
- detect important senders or keywords

### v0.5 - AI-assisted summarization
- use an LLM or AI service to summarize email content
- make the tool more useful for daily inbox management

### v1.0 - MVP Gmail assistant
- full workflow for reading, filtering, classifying, and summarizing messages
- cleaner code structure and reusable modules


