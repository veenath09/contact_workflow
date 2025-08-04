import gspread
from google.oauth2.service_account import Credentials

# Define the scope
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# Load credentials from the downloaded JSON file
creds = Credentials.from_service_account_file("neon-poetry-467907-k3-c6c2f44fb294.json", scopes=scope)

# Authorize and open the sheet
client = gspread.authorize(creds)
spreadsheet_id = "1ST3IWDLgNNJESD5Kb4d6FquveuaOJt3_kkKXP3JgDUg"
sheet = client.open_by_key(spreadsheet_id).sheet1 # or use .worksheet("Sheet2") etc.

# Example: Write a single row


# Example: Write multiple rows
data = [
    ["Alice", "alice@example.com", "Hello!"],
    ["Bob", "bob@example.com", "How are you?"]
]
for row in data:
    sheet.append_row(row)
