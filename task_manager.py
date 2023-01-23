# this program is for a small business that can help it to manage tasks assigned to each member of the team
# it is using two files for store users and tasks data,
# admin user is the only user that can add new user and view the statistics
# all user can add new task, view all tasks, and view owned tasks


import os
import datetime

# file paths are used several time ine the code by using these constants
# we can easily change the path in future
USER_FILE_PATH = "./Task 26/user.txt"
TASKS_FILE_PATH = "./Task 26/tasks.txt"
TASK_OVERVIEW_FILE_PATH = "./Task 26/task_overview.txt"
USER_OVERVIEW_FILE_PATH = "./Task 26/user_overview.txt"

# constant for date formats
INPUT_DATE_FORMAT = "%d-%m-%Y"
OUTPUT_DATE_FORMAT = "%d %b %Y"

login_data = {}

# ask user to enter their username and password and check
# if combination of these data is valid then display the menu
# otherwise ask user to enter their username and password agin
def login_user():
    with open(USER_FILE_PATH, "r") as users_file:
        for user_password in users_file.readlines():
            username, password = user_password.strip("\n").split(", ")
            login_data[username.lower()] = password

    while True:
        username = input("Please enter your username: ").lower()
        password = input("Please enter your password: ")

        user_password = login_data.get(username)

        if (user_password == None or user_password != password):
            print("The username or password is not valid!\n")
        else:
            break

    return username


# this function checks the given string is empty or white space or not
def is_empty(input_string=""):
    return input_string.strip() == ""


# this function adds a new user, ask username, password and confirmation password
# check the username not duplicate and password and confirmation password are match
# finally, store these data to file
def reg_user():
    while True:
        username = input("Please enter new username: ").lower()
        user_password = login_data.get(username)

        if (is_empty(username)):
            print("The username could not be empty!\n")
        elif (user_password != None):
            print("The username is duplicate!\n")
        else:
            break

    while True:
        password = input("Please enter new password: ")
        check_password = input("Please enter password again: ")

        if (is_empty(password)):
            print("The password could not be empty!\n")
        elif (password != check_password):
            print("The passwords are not match!\n")
        else:
            break

    with open(USER_FILE_PATH, "a") as users_file:
        users_file.writelines(f"{username}, {password}\n")

    # add new user to login_data dictionary to keep it update
    login_data[username.lower()] = password

    print("Adding a new user was successful")


# this function adds a new task, ask title, username, description and due date
# check the username exist, title not empty and due date is valid
# finally, store these data to file
def add_task():
    while True:
        task_title = input("Please enter title of task: ")

        if (is_empty(task_title)):
            print("Task title can\'t be empty!\n")
        else:
            break

    username = ask_username()

    task_description = input("Enter description of the task: ")

    due_date = ask_due_date()

    today = datetime.date.today()

    # convert date variables to sting by specific format
    today_str = today.strftime(OUTPUT_DATE_FORMAT)
    due_date_str = due_date.strftime(OUTPUT_DATE_FORMAT)

    with open(TASKS_FILE_PATH, "a") as tasks_file:
        tasks_file.writelines(
            f"{username}, {task_title}, {task_description}, {today_str}, {due_date_str}, No\n")

    print("Adding a new task was successful")


# this function asks the user to input due date and validate it
def ask_due_date():
    while True:
        due_date = input("Enter due date of the task:[DD-MM-YYYY] ")

        # try to parse input string as a date by specific format,
        # if it not successful exception occur and ask to input date agin
        try:
            due_date = datetime.datetime.strptime(due_date, INPUT_DATE_FORMAT)
        except ValueError:
            print("Date format is invalid!\n")
            continue

        today = datetime.date.today()
        if due_date.date() < today:
            print("Due date should be greater than or equal to today date")
        else:
            break

    return due_date


# this function asks the user to input a username and checks it to exist
def ask_username():
    while True:
        username = input("Enter the username to assign the task: ").lower()
        user_password = login_data.get(username)

        if (user_password == None):
            print("The username is invalid!\n")
        else:
            break

    return username


# this function shows all tasks, read all tasks from file and display them in user friendly manner
def view_all():
    with open(TASKS_FILE_PATH, "r") as task_file:
        tasks = task_file.readlines()

    show_tasks(tasks)


# this function shows the user's tasks, read tasks assigned to the current user from file and display them in user friendly manner
# and allow to the user to select a task for edit or mark it as complete
def view_mine():
    while True:
        with open(TASKS_FILE_PATH, "r") as task_file:
            tasks = task_file.readlines()

        index_map = {}
        filtered_tasks = []
        new_index = 0
        for index, task in enumerate(tasks):
            username = task.strip("\n").split(", ")[0]

            if (username.lower() == current_user):
                filtered_tasks.append(task)
                index_map[new_index] = index
                new_index += 1

        show_tasks(filtered_tasks)

        task_index, selected_task = select_task(filtered_tasks)

        if (task_index == -1):
            break

        actual_index = index_map[task_index]

        option = select_edit_option()

        if (option == 1):
            mark_as_complete(tasks, actual_index, selected_task)
            input("Press Enter to back ...")

        elif (option == 2):
            edit_filed = select_edit_filed()
            if (edit_filed == 1):
                edit_username(tasks, selected_task, actual_index)
                input("Press Enter to back ...")

            elif (edit_filed == 2):
                edit_due_date(tasks, selected_task, actual_index)
                input("Press Enter to back ...")

        else:
            break


# this function asks a new due date to update in a task, 
# checks the new date is valid and different with current due date
# finally, update corresponding task in the task file
def edit_due_date(tasks, selected_task, actual_index):
    while True:
        due_date_str = selected_task.strip("\n").split(", ")[-2]
        due_date = datetime.datetime.strptime(due_date_str, OUTPUT_DATE_FORMAT)
        new_due_date = ask_due_date()

        if (due_date == new_due_date):
            print("You should select different due date")
            continue
        else:
            break

    new_due_date_str = new_due_date.strftime(OUTPUT_DATE_FORMAT)
    username, task_title, task_description, today_str, due_date_str, is_completed = selected_task.strip("\n").split(", ")
    tasks[actual_index] = (f"{username}, {task_title}, {task_description}, {today_str}, {new_due_date_str}, {is_completed}\n")
    save_tasks(tasks)

    print("Due date is changed successfully")


# this function asks a username to assigns the task to it, 
# checks the username is valid and different with current username
# finally, update corresponding task in the task file
def edit_username(tasks, selected_task, actual_index):
    while True:
        username = selected_task.strip("\n").split(", ")[0]
        new_username = ask_username()
        if (new_username == username):
            print("You should select different username")
            continue
        else:
            break

    username, task_title, task_description, today_str, due_date_str, is_completed = selected_task.strip("\n").split(", ")
    tasks[actual_index] = (f"{new_username}, {task_title}, {task_description}, {today_str}, {due_date_str}, {is_completed}\n")
    save_tasks(tasks)

    print(f"Task assigned to {new_username} successfully")


# this function marks a task as completed, 
# and update corresponding task in the task file
def mark_as_complete(tasks, actual_index, selected_task):
    username, task_title, task_description, today_str, due_date_str, is_completed = selected_task.strip("\n").split(", ")
    is_completed = "Yes"
    tasks[actual_index] = (f"{username}, {task_title}, {task_description}, {today_str}, {due_date_str}, {is_completed}\n")

    save_tasks(tasks)
    print("Task is marked as completed successfully")


# this function shows a menu to asks the user what they want to do with selected task
# checks the selected option is valid and returns it
def select_edit_option():
    while True:
        option_str = input('''Select one of the following Options below:
1 - Mark the task as complete
2 - Edit the task
0 - Back
: ''').lower()

        if (not option_str.isdigit() or int(option_str) > 2 or int(option_str) < 0):
            print("You have made a wrong choice, Please Try again")
            continue

        option = int(option_str)
        break

    return option

# this function shows a menu to asks the user which filed they want to edit in selected task
# checks the selected option is valid and returns it
def select_edit_filed():
    while True:
        edit_filed_str = input('''Select one of the following Options below:
1 - Edit who assigned to
2 - Edit due date
0 - Back
: ''').lower()

        if (not edit_filed_str.isdigit() or int(edit_filed_str) > 2 or int(edit_filed_str) < 0):
            print("You have made a wrong choice, Please Try again")
            continue

        edit_filed = int(edit_filed_str)
        break

    return edit_filed


# this function asks the user to select a task
# checks the selected task is valid and editable 
# finally, returns task_index and selected_task
def select_task(filtered_tasks):
    while True:
        task_index_str = input(
            "Select either a specific task number or input \'-1\' to return to the main menu: ")

        try:
            task_index = int(task_index_str)
        except ValueError:
            print("Your choice is wrong!")
            continue

        if (task_index > len(filtered_tasks) or task_index == 0 or task_index < -1):
            print("Your choice should be -1 or greater than 0!")
            continue

        if (task_index == -1):
            return -1, None

        selected_task = filtered_tasks[task_index-1]
        is_completed = selected_task.strip("\n").split(", ")[-1].lower()

        if (is_completed == "yes"):
            print("This task is completed. you can\'t edit it")
            continue
        else:
            break

    return task_index - 1, selected_task


# this function overwrites the given task list in the task file
def save_tasks(tasks=[]):
    with open(TASKS_FILE_PATH, "w") as tasks_file:
        for task in tasks:
            tasks_file.write(f"{task}")


# this function shows the given task list in the output
def show_tasks(tasks=[]):
    # check is there any task in the file
    if (len(tasks) == 0):
        print("No task found!")

    for index, task in enumerate(tasks, 1):
        username, task_title, task_description, today_str, due_date_str, is_completed = task.strip("\n").split(", ")
        print(f"_____________________________________ Task {index} _______________________________________\n")
        print(f"Task:\t\t\t{task_title}")
        print(f"Assigned to:\t\t{username}")
        print(f"Date assigned:\t\t{today_str}")
        print(f"Due date:\t\t{due_date_str}")
        print(f"Task completed:\t\t{is_completed}")
        print(f"Task description:\n    {task_description}")

    print("___________________________________________________________________________________\n")


# this function generates task overview report and user overview report
def generate_reports():
    tasks, total_task_count = generate_task_overview()
    generate_user_overview(tasks, total_task_count)
    print("Reports are generated successfully")


# this function generates user overview report and store the result in a file
def generate_user_overview(tasks, total_task_count):
    user_count = len(login_data)
    today = datetime.date.today()

    with open(USER_OVERVIEW_FILE_PATH, "w") as user_overview_file:
        user_overview_file.write("___________________________________________________________________________________\n")
        user_overview_file.write(f"User count:   {user_count}\n")
        user_overview_file.write(f"Total tasks:  {total_task_count}\n")

        for username in login_data.keys():
            user_task_count = 0
            user_uncompleted_count = 0
            user_overdue_count = 0

            for task in tasks:
                data = task.strip("\n").split(", ")
                task_username = data[0]
                is_completed = data[-1]
                due_date_str = data[-2]

                if (task_username.lower() == username.lower()):
                    user_task_count += 1
                else:
                    continue

                if (is_completed.lower() == "no"):
                    user_uncompleted_count += 1
                    due_date = datetime.datetime.strptime(due_date_str, OUTPUT_DATE_FORMAT)

                    if (due_date.date() < today):
                        user_overdue_count += 1

            user_completed_count = user_task_count - user_uncompleted_count

            if (user_task_count > 0):
                user_task_percent = round(user_task_count / total_task_count * 100, 2)
                user_completed_percent = round(user_completed_count / user_task_count * 100, 2)
                user_incomplete_percent = round(user_uncompleted_count / user_task_count * 100, 2)
                user_overdue_percent = round(user_overdue_count / user_task_count * 100, 2)
            else:
                user_task_percent = 0
                user_completed_percent = 0
                user_incomplete_percent = 0
                user_overdue_percent = 0

            user_overview_file.write("\n\n--------------------------------------------------------\n")
            user_overview_file.write(f"{username} :\n")
            user_overview_file.write(f"\tTotal user tasks:        {user_task_count}\n")
            user_overview_file.write(f"\tUser task percent:       {user_task_percent}%\n")
            user_overview_file.write(f"\tUser completed percent:  {user_completed_percent}%\n")
            user_overview_file.write(f"\tUser incomplete percent: {user_incomplete_percent}%\n")
            user_overview_file.write(f"\tUser overdue percent:    {user_overdue_percent}%\n")

        user_overview_file.write("___________________________________________________________________________________\n")


# this function generates task overview report and store the result in a file
def generate_task_overview():
    uncompleted_count = 0
    overdue_count = 0
    today = datetime.date.today()

    with open(TASKS_FILE_PATH, "r") as task_file:
        tasks = task_file.readlines()

    total_task_count = len(tasks)

    for task in tasks:
        data = task.strip("\n").split(", ")
        is_completed = data[-1]
        due_date_str = data[-2]

        if (is_completed.lower() == "no"):
            uncompleted_count += 1
            due_date = datetime.datetime.strptime(due_date_str, OUTPUT_DATE_FORMAT)

            if (due_date.date() < today):
                overdue_count += 1

    completed_count = total_task_count - uncompleted_count

    if (total_task_count > 0):
        incomplete_percent = round(uncompleted_count / total_task_count * 100, 2)
        overdue_percent = round(overdue_count / total_task_count * 100, 2)
    else:
        incomplete_percent = 0
        overdue_percent = 0

    with open(TASK_OVERVIEW_FILE_PATH, "w") as task_overview_file:
        task_overview_file.write("___________________________________________________________________________________\n")
        task_overview_file.write(f"Total tasks:             {total_task_count}\n")
        task_overview_file.write(f"Completed tasks:          {completed_count}\n")
        task_overview_file.write(f"Incomplete tasks:         {uncompleted_count}\n")
        task_overview_file.write(f"Overdue tasks:            {overdue_count}\n")
        task_overview_file.write(f"Incomplete tasks percent: {incomplete_percent}%\n")
        task_overview_file.write(f"Overdue tasks percent:    {overdue_percent}%\n")
        task_overview_file.write("___________________________________________________________________________________\n")

    return tasks, total_task_count


# this function shows user overview and task overview reports, 
# if report files are not generated, generate them at first
def display_reports():
    if (not os.path.exists(TASK_OVERVIEW_FILE_PATH)):
        generate_reports()

    print("Task Overview Report: ")
    with open(TASK_OVERVIEW_FILE_PATH, "r") as task_overview_file:
        for line in task_overview_file:
            print(line.strip("\n"))

    print("\n")

    print("User Overview Report: ")
    with open(USER_OVERVIEW_FILE_PATH, "r") as user_overview_file:
        for line in user_overview_file:
            print(line.strip("\n"))


# -----------------------------------


# store current user name and whether is user admin or not,
#  to use in other part of code
current_user = login_user()
is_admin = (current_user == "admin")

# main process of the program,
# presenting the menu to the user till user select exit option
while True:

    # clear screen before show the menu
    os.system("cls")

    # the menu is different based on user is admin or not
    if (is_admin):
        menu = input('''Select one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e  - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following Options below:
a  - Adding a task
va - View all tasks
vm - View my tasks
e  - Exit
: ''').lower()

    print()
    
    # handel registering a user option, only admin user access to this option
    if menu == 'r' and is_admin:
        reg_user()
        input("Press Enter to back to Main Menu...")

    # handel adding a task option
    elif menu == 'a':
        add_task()
        input("Press Enter to back to Main Menu...")

    # handel view all tasks option
    elif menu == 'va':
        view_all()
        input("Press Enter to back to Main Menu...")

    # handel view my tasks option
    elif menu == 'vm':
        view_mine()

    # handel generate reports option
    elif menu == 'gr' and is_admin:
        generate_reports()
        input("Press Enter to back to Main Menu...")

    # handel display statistics option, only admin user access to this option
    elif menu == 'ds' and is_admin:
        display_reports()
        input("Press Enter to back to Main Menu...")

    # exit the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # otherwise show an error message
    else:
        print("You have made a wrong choice, Please Try again")
        input("Press Enter to back to Main Menu...")
