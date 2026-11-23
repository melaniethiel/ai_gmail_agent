import base64
import io
import json
import unittest
from contextlib import redirect_stderr
from unittest.mock import MagicMock, patch

from quickstart import (
  extract_email_body,
  format_message_summary,
  generate_email_summary,
  get_recent_messages,
  get_category,
  get_triage_flags,
  parse_cli_arguments,
)

# unittest class to test the search and triage functionality
# unittest.TestCase is a built-in Python class that provides a framework for writing and running unit tests
class SearchAndTriageTests(unittest.TestCase):
  # test that the command-line arguments are parsed correctly
  def test_parse_search_query_and_result_limit(self):
    # define a sample set of command-line arguments for testing
    arguments = parse_cli_arguments([
        "--query",
        "from:person@example.com is:unread",
        "--max-results",
        "12",
    ])

    # assert that the parsed arguments match the expected values and send error message if they do not
    self.assertEqual(arguments.query, "from:person@example.com is:unread")
    self.assertEqual(arguments.max_results, 12)

  def test_summarization_requires_an_ollama_model(self):
    with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
      parse_cli_arguments(["--summarize"])

  def test_full_body_option_requests_full_gmail_message(self):
    service = MagicMock()
    service.users().messages().list().execute.return_value = {
        "messages": [{"id": "message-id"}]
    }
    service.users().messages().get().execute.return_value = {
        "snippet": "Preview only",
        "payload": {"mimeType": "text/plain", "body": {"data": "ZnVsbCBib2R5"}},
    }

    messages = get_recent_messages(service, include_body=True)

    self.assertEqual(extract_email_body(messages[0]), "full body")
    service.users().messages().get.assert_any_call(
        userId="me", id="message-id", format="full"
    )

  def test_default_fetch_keeps_using_gmail_metadata(self):
    service = MagicMock()
    service.users().messages().list().execute.return_value = {
        "messages": [{"id": "message-id"}]
    }

    get_recent_messages(service)

    service.users().messages().get.assert_any_call(
        userId="me",
        id="message-id",
        format="metadata",
        metadataHeaders=["From", "Date", "Subject"],
    )

  def test_extract_body_prefers_plain_text_and_skips_attachments(self):
    encode = lambda value: base64.urlsafe_b64encode(
        value.encode("utf-8")
    ).decode("ascii").rstrip("=")
    message = {
        "payload": {
            "mimeType": "multipart/alternative",
            "parts": [
                {"mimeType": "text/html", "body": {"data": encode("<p>HTML</p>")}},
                {"mimeType": "text/plain", "body": {"data": encode("Full plain body")}},
                {
                    "mimeType": "text/plain",
                    "filename": "attachment.txt",
                    "body": {"data": encode("Do not summarize this attachment")},
                },
            ],
        }
    }

    self.assertEqual(extract_email_body(message), "Full plain body")

  def test_extract_body_uses_html_when_no_plain_text_exists(self):
    message = {
        "payload": {
            "mimeType": "text/html",
            "body": {
                "data": base64.urlsafe_b64encode(
                    "<p>Hello &amp; welcome</p>".encode("utf-8")
                ).decode("ascii").rstrip("=")
            },
        }
    }

    self.assertEqual(extract_email_body(message), "Hello & welcome")

  @patch("quickstart.urlopen")
  def test_ollama_receives_full_body_and_selected_model(self, urlopen):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = json.dumps(
        {"response": "A concise summary"}
    ).encode("utf-8")
    urlopen.return_value = response

    summary = generate_email_summary(
        "Full email content, not the Gmail snippet.", "my-local-model"
    )

    request = urlopen.call_args.args[0]
    request_data = json.loads(request.data.decode("utf-8"))
    self.assertEqual(summary, "A concise summary")
    self.assertEqual(request_data["model"], "my-local-model")
    self.assertIn("Full email content, not the Gmail snippet.", request_data["prompt"])
    self.assertFalse(request_data["stream"])

  # test that the triage flags reflect the Gmail labels correctly
  def test_triage_flags_reflect_gmail_labels(self):
    # define a sample message with specific labels for testing
    message = {"labelIds": ["IMPORTANT", "STARRED", "UNREAD"]}

    # assert that the triage flags match the expected values and send error message if they do not
    self.assertEqual(
        get_triage_flags(message), ["Important", "Starred", "Unread"]
    )

    # test that the category is derived from the Gmail category label correctly
  def test_category_comes_from_gmail_category_label(self):
    message = {"labelIds": ["CATEGORY_PROMOTIONS"]}

    self.assertEqual(get_category(message), "Promotions")

    # test that a message without a category label returns the default category
  def test_message_without_category_label_gets_default_category(self):
    message = {"labelIds": ["IMPORTANT", "UNREAD"]}

    self.assertEqual(get_category(message), "No category")

  # test that the message summary includes the triage flags
  def test_message_summary_includes_triage_flags(self):
    # define a sample message with specific labels and headers for testing
    message = {
        "labelIds": ["CATEGORY_PERSONAL", "IMPORTANT", "UNREAD"],
        "payload": {
            "headers": [
                {"name": "From", "value": "Sender <sender@example.com>"},
                {"name": "Subject", "value": "Project update"},
            ]
        },
        "snippet": "Here is the update.",
    }

    # format the message defined above and confirm includes expected results
    summary = format_message_summary(message)

    # assert they match the expected values and send error message if they do not
    self.assertIn("Subject: Project update", summary)
    self.assertIn("Category: Personal", summary)
    self.assertIn("Triage: Important, Unread", summary)
    self.assertIn("Here is the update.", summary)

  # test that a message without triage labels returns the default flag
  def test_message_without_triage_labels_gets_default_flag(self):
    self.assertEqual(get_triage_flags({}), ["No special flags"])

# run the unit tests if this script is executed directly
if __name__ == "__main__":
  # run the class of unit tests defined above
  unittest.main()