import os.path
import logging
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


# function to fetch 5 recent inbox messages with their display metadata
def get_recent_messages(service, max_results=5):
  """Fetch recent inbox messages with their display metadata."""
  logging.info("Requesting up to %d recent inbox messages", max_results)
  results = service.users().messages().list(
      userId="me", labelIds=["INBOX"], maxResults=max_results
  ).execute()

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

# function to format a Gmail message's headers and preview for display
def format_message_summary(message):
  """Format a Gmail message's headers and preview for display."""
  headers = message.get("payload", {}).get("headers", [])
  header_values = {
      header["name"].lower(): header["value"] for header in headers
  }
  sender = header_values.get("from", "Unknown sender")
  date = header_values.get("date", "Unknown date")
  subject = header_values.get("subject", "(No subject)")
  snippet = message.get("snippet", "").strip() or "(No preview available)"

  return f"From: {sender}\nDate: {date}\nSubject: {subject}\n{snippet}"


# function to list the user's Gmail labels
def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
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
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    logging.info("Gmail API request succeeded; retrieved %d labels", len(labels))

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

    messages = get_recent_messages(service)
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
