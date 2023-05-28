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

number_of_tasks = 0

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

def show_number_of_tasks():
    print(f"Excellent {username}! \n")
    print(f"You currently have {number_of_tasks} tasks in your list")

show_number_of_tasks()

def create_task():
    task_name = input("Which task would you like to add to your list of tasks?\n")
    while True:
        if len(task_name) > 0:
            break
        else:
            task_name = input("Please enter a valid name\n")
    
    task_importance = input("Splendid!\nCould you tell me if this is an important task?\n1. [yes]\n2. [no]\n")
    while True:
        if task_importance.lower() == 'yes' or task_importance == 'no':
            break
        else:
            task_importance = input("Please enter either 'yes' or 'no'\n")
    
    task_urgency = input("And is this task urgent?\n1. [yes]\n2. [no]\n")
    while True:
        if task_urgency.lower() == 'yes' or task_urgency == 'no':
            break
        else:
            task_urgency = input("Please enter either 'yes' or 'no'\n")

    return username, task_name, task_importance, task_urgency

new_task = create_task()

def update_user_worksheet(arg):
    """
    update worksheet with input from user
    """
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(arg)

task_data = [(task) for task in new_task]
update_user_worksheet(task_data)