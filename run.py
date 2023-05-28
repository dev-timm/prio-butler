import gspread 
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('prio-butler')

USER = SHEET.worksheet('user')
data = USER.get_all_values()

def introduce_to_user():
    """
    Welcome user and ask for name
    """
    print("Welcome user! I am Alfred, your butler who will help you prioritize your tasks for today.\n")

    username = input("Would you be so kind to tell me your name so that I can properly address you? ")
    print(f"Good day {username}")

introduce_to_user()