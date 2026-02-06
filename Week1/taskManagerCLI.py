import json
import os
from datetime import datetime

# Check if tasks.json exists or if its not empty if existing
if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 0: 
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
        # if it exists and not empty load the objects there to json
else:
    tasks = []
    # put an empty list there if empty or non existent

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def view_tasks():
    read_tasks = open("tasks.json", "r")
    print(read_tasks.read())

def add_tasks():
    while True:
        #strip removes trailing white spaces before and after
        name = input("Task Name: ").strip()
        if name:
            break
        print("Enter a Task name:")

    while True:
        description = input("Task Description: ").strip()
        if description:
            break
        print("Enter a Description:")
    
    while True:
        date = input("Task Due Date(DD/MM/YY): ").strip()
        try:
            due_date = datetime.strptime(date, "%d-%m-%y")
            break
        except(ValueError):
            print("Invalid Date Format, use dd-mm-yy")

    task_id = len(tasks) + 1
 
    task = {
        "id": task_id,
        "name": name,
        "description": description,
        "due date": date,
        "status": "pending"
    }
    tasks.append(task)
    save_tasks(tasks)

def mark_as_complete(id):
    id = int(input("Enter Task Id: "))
    for task in tasks:
        if (task["id"]) == id:
            if task["status"] == "completed":
                return("Task has been completed already")
            else:           
                task["status"] = "completed"
                save_tasks(tasks)
                return("Task successfully marked as completed")
    return("Invalid Task Id")

def view_all_pending():
    for task in tasks:
        if task["status"] != "completed":
            task_json = json.dumps(task, indent=4)
            print(task_json)

def view_all_completed():
    for task in tasks:
        if task["status"] == "completed":
            task_json = json.dumps(task, indent=4)
            print(task_json)

def delete_task(id):
    id = int(input("Enter Task Id: "))
    for task in tasks:
        if (task["id"]) == id:
            tasks.remove(task)
            save_tasks(tasks)
            return("Task has been sucessfully deleted")
    
    return("Invalid Task Id")

def task_manager_cli():
    while True:
        print("""
TASK MANAGER ACTIONS
1. Add New Task
2. View All Tasks
3. Mark Task as Complete
4. Delete Task
5. View All Pending Tasks
6. View All Completed Tasks
7. Stop Process
""")
        task_action = int(input("Enter a Number: "))
        if task_action == 1:
            add_tasks()
        elif task_action == 2:
            view_tasks()
        elif task_action == 3:
            print(mark_as_complete(id))
        elif task_action == 4:
            print(delete_task(id))
        elif task_action == 5:
            print(view_all_pending())
        elif task_action == 6:
            print(view_all_completed())
        elif task_action == 7:
            break
        else:
            print("Select a number from 1 to 5")

print(task_manager_cli())