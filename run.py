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

    user_data = SHEET.worksheet("user").get_all_records()
    number_of_tasks = 0

    for data in user_data:
        data_name = (data['Name'])
        
        if data_name == name:
            number_of_tasks += 1

    print(f"Excellent {name}!")
    print(f"You currently have {number_of_tasks} tasks in your list!")


def show_list_of_priorities(name):
    """
    Shows a list of all task data the user has added.
    """
    user_data = SHEET.worksheet("user").get_all_records()

    high_prio = []
    high_importance = []
    high_urgency = []
    no_prio = []
    number_of_tasks = high_prio + high_importance + high_urgency + no_prio


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
        
    high_prio_statement = f"You have {len(high_prio)} high priority for today which you should work on as soon as you can:"
    high_importance_statement = f"You have {len(high_importance)} important task which would be great if you could at least start working on today:"
    high_urgency_statement = f"You have {len(high_urgency)} urgent task that I would suggest that you think about if someone else can do it for you since:"
    no_prio_statement = f"You have {len(no_prio)} task which I suggest that you ignore for now until it becomes more urgent or important:"
    
    def show_prio_items(print_statement, list):
        print(print_statement)
        for item in list:
            item_index = list.index(item) + 1
            print(f"{item_index}. {item}")
        print()
    
    if len(high_prio) > 0:
        show_prio_items(high_prio_statement, high_prio)
    else:
        print("Marvelous, I have not identified any high priorities for today which you should work on as soon as you can!")
        print()
    if len(high_importance) > 0:
        show_prio_items(high_importance_statement, high_importance)
    if len(high_urgency) > 0:
        show_prio_items(high_urgency_statement, high_urgency)
    if len(no_prio) > 0:
        show_prio_items(no_prio_statement, no_prio)
    
    print(number_of_tasks)


def show_option_menu(name):
    """
    Show all options the user can choose from.
    Options are: Creating a new task, show all priorities, delete a task and quit the program.
    """
    show_number_of_tasks(name)
    print()
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
    show_option_menu(username)

main()