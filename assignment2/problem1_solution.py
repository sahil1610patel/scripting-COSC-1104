# Author: Sahil Patel
# Date: 2024/11/15
# Description: A Task Reminder and Checklist Application that helps users manage tasks with due dates and tracks overdue items for better organization.
import os
import time
from datetime import datetime, timedelta

TASK_FILENAME = "tasks.txt"

def retrieve_tasks():
    if not os.path.exists(TASK_FILENAME):
        return []
    with open(TASK_FILENAME, "r") as file:
        return [eval(line.strip()) for line in file.readlines()]

def store_tasks(task_list):
    with open(TASK_FILENAME, "w") as file:
        for task in task_list:
            file.write(str(task) + "\n")

def insert_task(task_name, task_due_date, task_category):
    task_list = retrieve_tasks()
    new_task = {
        "name": task_name,
        "due_date": task_due_date,
        "completed": False,
        "category": task_category,
    }
    task_list.append(new_task)
    store_tasks(task_list)
    print(f"Task '{task_name}' added successfully!")

def finalize_task(task_name):
    task_list = retrieve_tasks()
    for task in task_list:
        if task["name"] == task_name and not task["completed"]:
            task["completed"] = True
            store_tasks(task_list)
            print(f"Task '{task_name}' marked as completed!")
            return
    print(f"Task '{task_name}' not found or already completed.")

def list_tasks():
    task_list = retrieve_tasks()
    if not task_list:
        print("No tasks found.")
        return
    print("\nYour Tasks:")
    for task in task_list:
        status = "Completed" if task["completed"] else "Pending"
        print(f"- {task['name']} (Due: {task['due_date']}, Category: {task['category']}, Status: {status})")

def display_overdue_tasks():
    task_list = retrieve_tasks()
    current_time = datetime.now()
    overdue_list = [task for task in task_list if datetime.strptime(task["due_date"], "%Y-%m-%d") < current_time and not task["completed"]]
    if not overdue_list:
        print("No overdue tasks.")
        return
    print("\nOverdue Tasks:")
    for task in overdue_list:
        print(f"- {task['name']} (Due: {task['due_date']})")

def main():
    while True:
        print("\nTask Reminder and Checklist")
        print("1. Add Task")
        print("2. Complete Task")
        print("3. View All Tasks")
        print("4. View Overdue Tasks")
        print("5. Exit")
        user_choice = input("Choose an option: ")
        
        if user_choice == "1":
            task_name = input("Enter task name: ")
            task_due_date = input("Enter due date (YYYY-MM-DD): ")
            task_category = input("Enter category (e.g., Work, Personal): ")
            insert_task(task_name, task_due_date, task_category)
        elif user_choice == "2":
            task_name = input("Enter task name to complete: ")
            finalize_task(task_name)
        elif user_choice == "3":
            list_tasks()
        elif user_choice == "4":
            display_overdue_tasks()
        elif user_choice == "5":
            print("Exiting Task Reminder. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()