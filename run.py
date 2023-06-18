import gspread
from google.oauth2.service_account import Credentials
import colorama
from time import sleep
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('prio-butler')


def update_user_worksheet(task):
    """
    update worksheet with input from user.
    """
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(task)


def check_for_duplicates(user_input, list_of_records):
    """
    Check if the user input us already captured in the spreadsheet,
    """
    is_duplicate = False

    for record in list_of_records:
        if record == user_input:
            is_duplicate = True

    return is_duplicate


def introduce_to_user():
    """
    Welcome user.
    """
    print(f"Welcome user! I am Alfred, your butler who will help you prioritize your tasks for today.\n"); sleep(1.5)
    print(f"If you give me the tasks that you need to do for today, I will create your personalized priority lists of tasks. Once you are done with a task, you can simply delete it from the list and focus on the other ones.\n"); sleep(2)
    print(f"Alright, let's get started.\n"); sleep(2)


def get_username():
    """
    Ask for username.
    Validate if entered name is more than one character long.
    """
    username = input(f"Please be so kind to tell me your name so that I can properly address you.\n{Fore.GREEN}").strip()
    while True:
        if len(username) > 0:
            user_list = SHEET.worksheet("user").col_values(1)
            list_of_usernames = list(dict.fromkeys(user_list))
            username_exists = check_for_duplicates(username, list_of_usernames)

            if username_exists is True:
                while True:
                    print()
                    print(f"Welcome back {username}!")
                    print()
                    show_option_menu(username)
                    break
            break
        else:
            print()
            username = input(f"Please enter a valid username.\n{Fore.GREEN}").strip()
            print()
    print()

    return username


def create_task(name):
    """
    Creates a new task.
    Asks the user for a title, the importance and urgency of the task.
    """
    task_name = input(f"Which task would you like to add to your list of tasks?\n{Fore.GREEN}").strip()
    print()
    while True:
        if len(task_name) > 0:

            user_data = SHEET.worksheet("user").get_all_records()
            task_list = []

            for data in user_data:
                data_name = (data['Name'])

                if data_name == name:
                    task_list.append(data['Task Name'])

            task_exists = check_for_duplicates(task_name, task_list)
            if task_exists is True:
                while True:
                    print()
                    print(f"Looks like this task already exists on your list. If you like, you can review your current tasks by typing [show] in the menu below.")
                    print()
                    show_option_menu(name)
                    break

            break
        else:
            task_name = input(f"Please enter a valid task title.\n{Fore.GREEN}").strip()
            print()

    task_importance = input(f"Splendid!\nCould you tell me if this is an important task?\n[yes]\n[no]\n{Fore.GREEN}").lower()
    print()
    while True:
        if task_importance == 'yes' or task_importance == 'no':
            break
        else:
            task_importance = input(f"Please enter either 'yes' or 'no'.\n{Fore.GREEN}").lower()
            print()

    task_urgency = input(f"And is this task urgent?\n[yes]\n[no]\n{Fore.GREEN}").lower()
    print()
    while True:
        if task_urgency == 'yes' or task_urgency == 'no':
            break
        else:
            task_urgency = input(f"Please enter either 'yes' or 'no'.\n{Fore.GREEN}").lower()
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

    print(f"You currently have {number_of_tasks} task(s) in your list!")


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

    if len(high_prio) < 2:
        high_prio_statement = f"You have {len(high_prio)} high priority for today which you should work on as soon as you can:"
    else:
        high_prio_statement = f"You have {len(high_prio)} high priorities for today which you should work on as soon as you can:"
    if len(high_importance) < 2:
        high_importance_statement = f"You have {len(high_importance)} important task which would be great if you could at least start working on today:"
    else:
        high_importance_statement = f"You have {len(high_importance)} important tasks which would be great if you could at least start working on today:"
    if len(high_urgency) < 2:
        high_urgency_statement = f"You have {len(high_urgency)} urgent task that I would suggest that you think about if someone else can do it for you since it’s not as important:"
    else:
        high_urgency_statement = f"You have {len(high_urgency)} urgent tasks that I would suggest that you think about if someone else can do them for you since they are not as important:"
    if len(high_prio) < 2:
        no_prio_statement = f"You have {len(no_prio)} task which I suggest that you ignore for now until it becomes more urgent or important:"
    else:
        no_prio_statement = f"You have {len(no_prio)} tasks which I suggest that you ignore for now until they become more urgent or important:"

    def show_prio_items(print_statement, list):
        """
        Displays each item of the list as an ordered list.
        """
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


def delete_task(name):
    """
    Enables user to delete a task.
    """
    user_data = SHEET.worksheet("user").get_all_records()
    user_list = []

    for data in user_data:
        data_name = (data['Name'])

        if data_name == name:
            user_list.append(data)

            for item in user_list:
                item_index = user_list.index(item) + 1

            if data['Important?'] == 'yes' and data['Urgent?'] == 'yes':
                print(f"[{item_index}] {data['Task Name']} (important and urgent)")
            elif data['Important?'] == 'no' and data['Urgent?'] == 'yes':
                print(f"[{item_index}] {data['Task Name']} (urgent)")
            elif data['Important?'] == 'yes' and data['Urgent?'] == 'no':
                print(f"[{item_index}] {data['Task Name']} (important)")
            elif data['Important?'] == 'no' and data['Urgent?'] == 'no':
                print(f"[{item_index}] {data['Task Name']} (no prio)")

    if len(user_list) == 0:
        show_option_menu(name)
    else:
        print()
        task_to_delete = input(f"Please type the number of the task that you would like to delete:\n{Fore.GREEN}")
        print()

    while True:
        try:
            if int(task_to_delete) > 0 and int(task_to_delete) <= len(user_list):
                user_worksheet = SHEET.worksheet("user")
                sheet_name_col = user_worksheet.col_values(1)
                sheet_task_col = user_worksheet.col_values(2)

                task_index = user_list[int(task_to_delete) - 1]
                all_sheet_tasks = []

                for index, item in enumerate(sheet_name_col):
                    all_sheet_tasks.append({'name': sheet_name_col[index], 'task': sheet_task_col[index]})

                for index, item in enumerate(all_sheet_tasks):
                    if item['name'] == name and item['task'] == task_index['Task Name']:
                        row_to_delete = index + 1

                user_worksheet.delete_rows(row_to_delete)

                break
            else:
                task_to_delete = input(f"Please enter a valid number between 1 and {len(user_list)}.\n{Fore.GREEN}")
                print()
        except ValueError:
            task_to_delete = input(f"Please enter a valid number between 1 and {len(user_list)}.\n{Fore.GREEN}")
            print()


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
            user_selection = input(f"Please enter a valid option.\n{Fore.GREEN}")
            print()

    while True:
        if user_selection.lower() == "new":
            create_task(name)
            break
        elif user_selection.lower() == "show":
            show_list_of_priorities(name)
            break
        elif user_selection.lower() == "delete":
            delete_task(name)
            break
        elif user_selection.lower() == "quit":
            print(f"I wish you a wonderful rest of your day {name}!")
            quit()
        else:
            user_selection = input(f"Please enter a valid option.\n{Fore.GREEN}")
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
