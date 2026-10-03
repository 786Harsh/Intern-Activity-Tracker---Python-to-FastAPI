import json
import os


class Intern:
    def __init__(self, intern_id, name, role, status="Active"):
        self.intern_id = intern_id
        self.name = name
        self.role = role
        self.status = status
        self.daily_hours = []
        self.daily_tasks = []

    def to_dict(self):
        return {
            "intern_id": self.intern_id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "daily_hours": self.daily_hours,
            "daily_tasks": self.daily_tasks
        }


FILE_NAME = "interns.json"


def load_interns():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_interns(interns):
    with open(FILE_NAME, "w") as file:
        json.dump(interns, file, indent=4)


def generate_intern_id(interns):
    if not interns:
        return "INT001"

    numbers = []

    for intern in interns:
        intern_id = intern["intern_id"]
        number = int(intern_id.replace("INT", ""))
        numbers.append(number)

    next_number = max(numbers) + 1

    return f"INT{next_number:03d}"


def find_intern(interns, intern_id):
    for intern in interns:
        if intern["intern_id"].upper() == intern_id.upper():
            return intern

    return None


def add_intern(interns):
    name = input("Enter intern name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter intern name: ").strip()

    role = input("Enter intern role: ").strip()

    while not role:
        print("Role cannot be empty.")
        role = input("Enter intern role: ").strip()

    intern_id = generate_intern_id(interns)

    intern = Intern(intern_id, name, role)

    interns.append(intern.to_dict())

    save_interns(interns)

    print("\nIntern added successfully.")
    print("Intern ID:", intern_id)


def add_daily_activity(interns):
    intern_id = input("Enter intern ID: ").strip()

    intern = find_intern(interns, intern_id)

    if intern is None:
        print("Intern not found.")
        return

    if intern["status"] != "Active":
        print("Activity cannot be added.")
        print("Current status:", intern["status"])
        return

    while True:
        try:
            hours = float(input("Enter hours worked: "))

            if hours < 0:
                print("Hours cannot be negative.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    task = input("Enter task completed: ").strip()

    while not task:
        print("Task cannot be empty.")
        task = input("Enter task completed: ").strip()

    intern["daily_hours"].append(hours)
    intern["daily_tasks"].append(task)

    save_interns(interns)

    print("Daily activity added successfully.")


def update_status(interns):
    intern_id = input("Enter intern ID: ").strip()

    intern = find_intern(interns, intern_id)

    if intern is None:
        print("Intern not found.")
        return

    print("Current status:", intern["status"])
    print("1. Active")
    print("2. Inactive")
    print("3. Completed")

    choice = input("Enter new status: ").strip()

    if choice == "1":
        new_status = "Active"
    elif choice == "2":
        new_status = "Inactive"
    elif choice == "3":
        new_status = "Completed"
    else:
        print("Invalid choice.")
        return

    intern["status"] = new_status

    save_interns(interns)

    print("Status updated successfully.")
    print("New status:", new_status)


def view_intern_summary(interns):
    intern_id = input("Enter intern ID: ").strip()

    intern = find_intern(interns, intern_id)

    if intern is None:
        print("Intern not found.")
        return

    hours = intern["daily_hours"]
    tasks = intern["daily_tasks"]

    total_hours = sum(hours)

    if hours:
        average_hours = total_hours / len(hours)
    else:
        average_hours = 0

    print("\n===== INTERN SUMMARY =====")
    print("Intern ID:", intern["intern_id"])
    print("Name:", intern["name"])
    print("Role:", intern["role"])
    print("Status:", intern["status"])
    print("Total Hours:", total_hours)
    print("Average Hours:", round(average_hours, 2))

    print("\nTask History:")

    if tasks:
        for i in range(len(tasks)):
            print(f"{i + 1}. {tasks[i]} - {hours[i]} hours")
    else:
        print("No activities recorded.")

    if tasks:
        print("\nMost Recent Activity:")
        print(tasks[-1])
        print("Hours:", hours[-1])


def overall_statistics(interns):
    if not interns:
        print("No interns available.")
        return

    total_interns = len(interns)

    active_interns = 0
    all_hours = []
    top_performer = None
    highest_hours = -1

    for intern in interns:
        if intern["status"] == "Active":
            active_interns += 1

        total_hours = sum(intern["daily_hours"])
        all_hours.extend(intern["daily_hours"])

        if total_hours > highest_hours:
            highest_hours = total_hours
            top_performer = intern

    if all_hours:
        average_hours = sum(all_hours) / len(all_hours)
    else:
        average_hours = 0

    print("\n===== OVERALL STATISTICS =====")
    print("Total Interns:", total_interns)
    print("Active Interns:", active_interns)
    print("Average Hours:", round(average_hours, 2))

    print("\nTop Performer:")
    print("Intern ID:", top_performer["intern_id"])
    print("Name:", top_performer["name"])
    print("Total Hours:", highest_hours)


def main():
    interns = load_interns()

    while True:
        print("\nINTERN ACTIVITY TRACKER")
        print("1. Add Intern")
        print("2. Add Daily Activity")
        print("3. Update Intern Status")
        print("4. View Intern Summary")
        print("5. Overall Statistics")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_intern(interns)

        elif choice == "2":
            add_daily_activity(interns)

        elif choice == "3":
            update_status(interns)

        elif choice == "4":
            view_intern_summary(interns)

        elif choice == "5":
            overall_statistics(interns)

        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


main()

