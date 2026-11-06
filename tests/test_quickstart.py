import unittest

from quickstart import (
  format_message_summary,
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