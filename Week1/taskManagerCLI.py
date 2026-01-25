import json
import os
from datetime import datetime

FILE_NAME = "AllTasks.json"

def loadTasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def saveTasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def addTask(tasks):
    title = input("Task title: ")
    desc = input("Task description: ")
    dueDate = input("Due date (YYYY-MM-DD): ")
    try:
        datetime.strptime(dueDate, "%Y-%m-%d")
    except ValueError:
        print("This is not a valid date format")
        return

    task = {
        "title": title,
        "description": desc,
        "due_date": dueDate,
        "completed": False
    }
    tasks.append(task)
    saveTasks(tasks)
    print("Task added successfully!")

def viewTasks(tasks):
    if not tasks:
        print("No task has been created")
        return

    print("\nALL TASKS")
    for task in tasks:
        status = "Completed" if task["completed"] else "Not Completed"
        print(f"""
Title: {task['title']}
Description: {task['description']}
Due Date: {task['due_date']}
Status: {status}
""")

def markComplete(tasks):
    taskTitle = input("Which task have you completed: ")

    for task in tasks:
        if task["title"].lower() == taskTitle.lower():
            task["completed"] = True
            saveTasks(tasks)
            print("Task has been completed!")
            return

    print("No task with that name")

def deleteTask(tasks):
    taskTitle = input("Which task do you want to delete: ")

    for task in tasks:
        if task["title"].lower() == taskTitle.lower():
            tasks.remove(task)
            saveTasks(tasks)
            print("Task deleted.")
            return

    print("No task with that name")

def main():
    tasks = loadTasks()
    viewTasks(tasks)

    while True:
        print("""
TASK MANAGER
1. Add task
2. View all tasks
3. Mark task as complete
4. Delete task
5. Stop Process
""")
        num = input("Choose an option to continue: ")

        if num == "1":
            addTask(tasks)
        elif num == "2":
            viewTasks(tasks)
        elif num == "3":
            markComplete(tasks)
        elif num == "4":
            deleteTask(tasks)
        elif num == "5":
            break
        else:
            print("Choose a number from 1 to 5")

if __name__ == "__main__":
    main()