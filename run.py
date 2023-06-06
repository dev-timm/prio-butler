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
    update worksheet with input from user.
    """
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(arg)


def introduce_to_user():
    """
    Welcome user.
    """
    print(f"Welcome user! I am Alfred, your butler who will help you prioritize your tasks for today.\n")


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


def create_task(name):
    """
    Creates a new task.
    Asks the user for a title, the importance and urgency of the task.
    """
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

    task_data = [name, task_name, task_importance, task_urgency]
    update_user_worksheet(task_data)


def show_number_of_tasks(name):
    """
    Prints the total number of tasks the user has created.
    """
    print(f"Excellent {name}! \n")
    print(f"You currently have {number_of_tasks} tasks in your list")


def show_list_of_priorities(name):
    """
    Shows a list of all task data the user has added.
    """
    user_data = SHEET.worksheet("user").get_all_records()

    high_prio = []
    high_importance = []
    high_urgency = []
    no_prio = []

    for data in user_data:
        data_name = (data['Name'])
        
        if data_name == name:
            if data['Important?'] == 'yes' and data['Urgent?'] == 'yes':
                high_prio.append(data['Task Name'])
            elif data['Important?'] == 'no' and data['Urgent?'] == 'yes':
                high_importance.append(data['Task Name'])
            elif data['Important?'] == 'yes' and data['Urgent?'] == 'no':
                high_urgency.append(data['Task Name'])
            elif data['Important?'] == 'no' and data['Urgent?'] == 'no':
                no_prio.append(data['Task Name'])
        
    print(f"You have {number_of_tasks} high priority for today which you should work on as soon as you can:")
    print(high_prio)
    print()
    print(f"You have {number_of_tasks} important task which would be great if you could at least start working on today:")
    print(high_importance)
    print()
    print(f"You have {number_of_tasks} urgent task that I would suggest that you think about if someone else can do it for you since:")
    print(high_urgency)
    print()
    print(f"You have {number_of_tasks} task which I suggest that you ignore for now until it becomes more urgent or important:")
    print(no_prio)
    print()
        

def show_option_menu(name):
    """
    Show all options the user can choose from.
    Options are: Creating a new task, show all priorities, delete a task and quit the program.
    """
    print("Please choose what you would like me to do for you next:")
    print()
    user_selection = input(f"Create a new task - [new]\nShow the list of your priorities - [show]\nDelete a task - [delete]\nQuit program - [quit]\n{Fore.GREEN}")
    print()

    while True:
        if len(user_selection) > 0:
            break
        else:
            user_selection = input(f"Please enter a valid option\n{Fore.GREEN}")
            print()

    while True:
        if user_selection.lower() == "new":
            create_task(name)
            break
        elif user_selection.lower() == "show":
            show_list_of_priorities(name)
            break
        elif user_selection.lower() == "delete":
            print("delete a task")
            break
        elif user_selection.lower() == "quit":
            print(f"I wish you a wonderful rest of your day {name}!")
            quit()
        else:
            user_selection = input(f"Please enter a valid option\n{Fore.GREEN}")
            print()

    show_option_menu(name)


def main():
    """
    Contains all functions to run the program.
    """
    introduce_to_user()
    username = get_username()
    create_task(username)
    show_number_of_tasks(username)
    show_option_menu(username)

main()