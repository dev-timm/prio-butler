import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset = True)

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

def update_user_worksheet(arg):
    """
    update worksheet with input from user
    """
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(arg)

def introduce_to_user():
    """
    Welcome user.
    """
    print(f"Welcome user! I am Alfred, your butler who will help you prioritize your tasks for today.\n")

introduce_to_user()

def get_username():
    """
    Ask for username.
    Validate if entered name is more than one character long.
    """
    username = input(f"Would you be so kind to tell me your name so that I can\nproperly address you?\n{Fore.GREEN}")
    while True:
        if len(username) > 0:
            break
        else:
            username = input(f"Please enter a valid name\n{Fore.GREEN}")
            print()
    print()
    return username

username = get_username()

def create_task():
    task_name = input(f"Which task would you like to add to your list of tasks?\n{Fore.GREEN}")
    print()
    while True:
        if len(task_name) > 0:
            break
        else:
            task_name = input(f"Please enter a valid name\n{Fore.GREEN}")
            print()
    
    task_importance = input(f"Splendid!\nCould you tell me if this is an important task?\n1. [yes]\n2. [no]\n{Fore.GREEN}")
    print()
    while True:
        if task_importance.lower() == 'yes' or task_importance == 'no':
            break
        else:
            task_importance = input(f"Please enter either 'yes' or 'no'\n{Fore.GREEN}")
            print()
    
    task_urgency = input(f"And is this task urgent?\n1. [yes]\n2. [no]\n{Fore.GREEN}")
    print()
    while True:
        if task_urgency.lower() == 'yes' or task_urgency == 'no':
            break
        else:
            task_urgency = input(f"Please enter either 'yes' or 'no'\n{Fore.GREEN}")
            print()

    task_data = [username, task_name, task_importance, task_urgency]
    update_user_worksheet(task_data)

create_task()

def show_number_of_tasks():
    print(f"Excellent {username}! \n")
    print(f"You currently have {number_of_tasks} tasks in your list")

show_number_of_tasks()

def show_list_of_priorities():
    """
    Shows a list of all task data the user has added
    """
    tasks = SHEET.worksheet("user").get_all_values()
    pprint(tasks)

def show_option_menu():
    print("Please choose what you would like me to do for you next:")
    print()
    user_selection = input(f"Create a new task - [new]\nShow the list of your priorities - [show]\nDelete a task - [delete]\nQuit program - [quit]\n{Fore.GREEN}")

    while True:
        if len(user_selection) > 0:
            break
        else:
            user_selection = input(f"Please enter a valid option\n{Fore.GREEN}")
            print()

    while True:
        if user_selection.lower() == "new":
            create_task()
            break
        elif user_selection.lower() == "show":
            print("show all tasks")
            show_list_of_priorities()
            break
        elif user_selection.lower() == "delete":
            print("delete a task")
            break
        elif user_selection.lower() == "quit":
            print("goodbye")
            quit()
        else:
            user_selection = input(f"Please enter a valid option\n{Fore.GREEN}")

    show_option_menu()

show_option_menu()