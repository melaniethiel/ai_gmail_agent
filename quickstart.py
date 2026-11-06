import os.path
import logging
import argparse
from logging.handlers import TimedRotatingFileHandler

# import all python libraries that are needed for this file
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create a project-local log folder so logging works from any working directory.
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "ai_gmail_agent.log")

# Keep timestamped logs in the terminal and rotate the file at local midnight.
logging.basicConfig(
  level=logging.INFO,
  format="[%(asctime)s] %(levelname)s: %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  handlers=[
      logging.StreamHandler(),
      #this part creates a new log file every day at midnight, adds date to the filename, and keeps 4 days of logs before deleting old ones
      TimedRotatingFileHandler(
          LOG_FILE,
          when="midnight",
          interval=1,
          backupCount=4,
          encoding="utf-8",
      ),
  ],
)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def parse_positive_integer (value):
  """Parse a positive integer for command-line queries."""
  try:
    number = int(value)
  except ValueError as error:
    raise argparse.ArgumentTypeError("must be a whole number") from error

  if number < 1:
    raise argparse.ArgumentTypeError("must be greater than zero")
  return number


def parse_cli_arguments (arguments=None):
  """Parse search and result-count options from the command line."""
  parser = argparse.ArgumentParser(
      description="Search and triage recent Gmail inbox messages."
  )
  parser.add_argument(
      "--query",
      default="",
      help="Gmail search query, such as 'from:person@example.com is:unread'",
  )
  parser.add_argument(
      "--max-results",
      type=parse_positive_integer,
      default=5,
      help="maximum number of inbox messages to display (default: 5)",
  )
  return parser.parse_args(arguments)


# function to fetch 5 recent inbox messages with their display metadata
def get_recent_messages(service, max_results=5, query=""):
  """Fetch recent inbox messages with their display metadata."""
  logging.info(
      "Requesting up to %d recent inbox messages; search filter applied: %s",
      max_results,
      bool(query),
  )
  list_arguments = {
      "userId": "me",
      "labelIds": ["INBOX"],
      "maxResults": max_results,
  }
  if query:
    list_arguments["q"] = query
  results = service.users().messages().list(**list_arguments).execute()
  logging.info("Gmail API access confirmed by successful inbox search")

  # get the list of message references from the API response
  message_refs = results.get("messages", [])
  logging.info("Found %d recent inbox message references", len(message_refs))
  # initialize an empty list to hold the full message metadata
  messages = []

# loops through each message reference and fetches the full message metadata for display
  for message_ref in message_refs:
    # fetch the headers and snippet of the message using the Gmail API
    message = service.users().messages().get(
        userId="me",
        id=message_ref["id"],
        format="metadata",
        metadataHeaders=["From", "Date", "Subject"],
    ).execute()
    # append the full message metadata to the messages list
    messages.append(message)

  logging.info("Retrieved metadata for %d inbox messages", len(messages))
  # return the list of messages with their display metadata
  return messages


def get_triage_flags(message):
  """Return useful triage signals from Gmail's existing message labels."""
  # fetch the labels of the message using the Gmail API
  message_labels = set(message.get("labelIds", []))
  triage_flags = []

  #check for and add each flag to the list of triage flags if it is present in the message labels
  if "IMPORTANT" in message_labels:
    triage_flags.append("Important")
  if "STARRED" in message_labels:
    triage_flags.append("Starred")
  if "UNREAD" in message_labels:
    triage_flags.append("Unread")

  # return the list of triage flags, or a default message if none are found
  return triage_flags or ["No special flags"]


def get_category(message):
  """Return a readable category from Gmail's built-in category labels."""
  # fetch the labels of the message using the Gmail API
  message_labels = set(message.get("labelIds", []))

  # define a mapping of Gmail category label IDs to human-readable category names
  category_labels = {
      "CATEGORY_PERSONAL": "Personal",
      "CATEGORY_SOCIAL": "Social",
      "CATEGORY_PROMOTIONS": "Promotions",
      "CATEGORY_UPDATES": "Updates",
      "CATEGORY_FORUMS": "Forums",
  }

  # loops through labeles for category_* labels and displays first one found, or returns "No category" if none are found
  for label_id, category_name in category_labels.items():
    if label_id in message_labels:
      return category_name

  return "No category"

# function to format a Gmail message's details for display
# Currently shows: headers, preview, category, and select triage flags
def format_message_summary(message):
  """Format a Gmail message's details for display."""
  headers = message.get("payload", {}).get("headers", [])
  header_values = {
      header["name"].lower(): header["value"] for header in headers
  }
  sender = header_values.get("from", "Unknown sender")
  date = header_values.get("date", "Unknown date")
  subject = header_values.get("subject", "(No subject)")
  snippet = message.get("snippet", "").strip() or "(No preview available)"
  triage = ", ".join(get_triage_flags(message))
  category = get_category(message)

  return (
      f"From: {sender}\nDate: {date}\nSubject: {subject}\n"
      f"Category: {category}\nTriage: {triage}\n{snippet}"
  )

# function to authenticate and display recent inbox messages
def main():
  """Authenticate with Gmail and display recent inbox messages."""
  arguments = parse_cli_arguments()
  logging.info("Initialized main function")
  creds = None
  
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    logging.info("Loading saved OAuth credentials")
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
      logging.info("Refreshed expired OAuth credentials")
    else:
      logging.info("Starting Google OAuth authorization")
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
      logging.info("Google OAuth authorization completed")
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    logging.info("Saved OAuth credentials to token.json")

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    logging.info("Initialized Gmail API client")

    messages = get_recent_messages(
      service,
      max_results=arguments.max_results,
      query=arguments.query,
    )
    if not messages:
      logging.info("No inbox messages were returned")
      print("\nNo messages found in your inbox.")
      return

    summaries = [format_message_summary(message) for message in messages]
    logging.info("Created %d message summaries", len(summaries))
    print("\nRecent inbox messages:")
    for index, summary in enumerate(summaries, start=1):
      print(f"\n{index}. {summary}")
    logging.info("Displayed %d message summaries", len(summaries))

  except HttpError:
    logging.exception("Gmail API request failed")

# when this file is run as a script, call the main function
if __name__ == "__main__":
  main()
