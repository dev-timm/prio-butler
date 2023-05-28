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
    Welcome user.
    """
    print("Welcome user! I am Alfred, your butler who will help you prioritize your tasks for today.\n")

introduce_to_user()

def get_username():
    """
    Ask for username.
    Validate if entered name is more than one character long.
    """
    username = input("Would you be so kind to tell me your name so that I can\nproperly address you? ")
    while True:
        if len(username) > 0:
            break
        else:
            username = input("Please enter a valid name ")
    return username

username = get_username()

print(username)