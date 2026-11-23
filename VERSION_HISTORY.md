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

## v0.2 - Read recent messages, display preview, and added logging

### Added
- fetch recent inbox messages
- format message summaries for display
- add logging for troubleshooting

### Purpose
- expand the Gmail API integration from labels to recent inbox message previews
- make progress and API failures easier to troubleshoot

### Notes
- previews use Gmail's snippet; they are not AI-generated summaries
- logs rotate daily and retain up to four archived files in addition to the current log
- logs avoid recording email addresses and message contents

## v0.3 - Search and triage inbox messages

### Added
- accept Gmail search queries from the command line
- allow the result limit to be configured
- display important, starred, and unread Gmail labels as triage signals
- display Gmail's built-in message categories in each summary
- add offline tests for search-option parsing, triage flags, category mapping, and message-summary formatting

### Removed
- script to list Gmail labels

### Purpose
- make it easier to find relevant inbox messages without changing Gmail data
- surface useful triage information using labels already assigned by Gmail
- group messages by categories Gmail has assigned, without custom AI rules

### Notes
- searches remain limited to the inbox and use Gmail's query syntax
- triage is rule-based and transparent; no LLM is used
- built-in categories include Personal, Social, Promotions, Updates, and Forums; custom Work and Follow-up categories remain future work
- this feature reads messages only and does not change labels or email state

## v0.4 - AI-assisted summarization

### Added
- opt-in `--summarize` and `--model` command-line options for generating summaries with a selected local Ollama model
- fetch full Gmail messages only when summarization is requested; default runs continue using Gmail snippets and metadata
- extract readable plain-text or HTML email bodies while skipping named attachments
- prompt the model to explain the email's purpose, important details, explicitly stated deadlines, requested actions, and a recommended next step
- report Ollama connection and response errors
- add offline tests for full-body retrieval, body extraction, CLI validation, and Ollama request construction
- document local Ollama setup and privacy considerations

### Purpose
- provide a local, opt-in way to understand the purpose and action items in an email without changing Gmail data

### Notes
- email bodies are sent to the local Ollama service only when `--summarize` is selected; they are not written to application logs
- model output can be inaccurate; the prompt asks the model not to follow instructions in email content, but this is not a security guarantee
- Gmail access remains read-only; the application does not modify messages or labels

## Planned future versions

### v0.5 - User-approved agentic actions
- use email summaries to suggest next steps, such as a follow-up task or reply draft
- show the proposed action and relevant email context before taking action
- require explicit user approval before any action that changes Gmail or external data

### v1.0 - MVP Gmail assistant
- full workflow for reading, filtering, classifying, and summarizing messages
- cleaner code structure and reusable modules
- look into better unittest outputs to better understand test results
- look into checking if ollama running and auto-start and auto-close as part of process

