import json
from datetime import datetime, date

#create a custom JSON encoder that knows how to handle datetime.date objects.
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Initialize an empty task list
tasks = []

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date_str = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (low, medium, high): ")

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    print("Task added successfully!")

def update_task():
    display_tasks()
    try:
        task_index = int(input("Enter the task number you want to update: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            print(f"Selected Task: {task['title']} - {task['description']}")

            # Allow updating specific fields
            task['title'] = input("Enter new title (press Enter to keep the existing title): ") or task['title']
            task['description'] = input("Enter new description (press Enter to keep the existing description): ") or task['description']
            new_due_date_str = input("Enter new due date (YYYY-MM-DD, press Enter to keep the existing due date): ")
            task['due_date'] = datetime.strptime(new_due_date_str, "%Y-%m-%d").date() if new_due_date_str else task['due_date']
            task['priority'] = input("Enter new priority (low, medium, high, press Enter to keep the existing priority): ") or task['priority']

            print("Task updated successfully!")
        else:
            print("Invalid task number. No task updated.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

def mark_as_complete():
    display_tasks()
    try:
        task_index = int(input("Enter the task number you want to mark as complete: ")) - 1
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            if not task['completed']:
                task['completed'] = True
                print("Task marked as complete!")
            else:
                print("Task is already marked as complete.")
        else:
            print("Invalid task number. No task marked as complete.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

def remove_task():
    display_tasks()
    try:
        task_index = int(input("Enter the task number you want to remove: ")) - 1
        if 0 <= task_index < len(tasks):
            removed_task = tasks.pop(task_index)
            print(f"Task '{removed_task['title']}' removed successfully!")
        else:
            print("Invalid task number. No task removed.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

def display_tasks():
    if not tasks:
        print("No tasks found.")
        return

    # Sorting options
    print("\nSort Options:")
    print("1. Sort by Due Date")
    print("2. Sort by Priority")
    print("3. Sort by Task Number (default)")

    sort_option = input("Enter your sorting choice (1/2/3): ")

    if sort_option == "1":
        tasks.sort(key=lambda x: x['due_date'])
    elif sort_option == "2":
        tasks.sort(key=lambda x: x['priority'])
    # Default: Sort by task number
    else:
        pass

    print("\nTask List:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. {task['title']} - Due: {task['due_date']} - Priority: {task['priority']} - Completed: {task['completed']}")

def save_tasks_to_file():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, cls=CustomEncoder)

def load_tasks_from_file():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            data = file.read()
            if data:
                tasks = json.loads(data)
            else:
                print("No data found in the file.")
    except FileNotFoundError:
        print("No file found. Starting with an empty task list.")
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def main():
    load_tasks_from_file()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Mark Task as Complete")
        print("4. Remove Task")
        print("5. Display Tasks")
        print("6. Save and Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            update_task()
        elif choice == "3":
            mark_as_complete()
        elif choice == "4":
            remove_task()
        elif choice == "5":
            display_tasks()
        elif choice == "6":
            save_tasks_to_file()
            print("Tasks saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
