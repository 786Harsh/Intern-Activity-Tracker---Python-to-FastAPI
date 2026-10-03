import json


def calculate_total_hours(hours):
    return sum(hours)


def calculate_average_hours(hours):
    if len(hours) == 0:
        return 0

    return sum(hours) / len(hours)


def generate_summary(intern):
    total_hours = calculate_total_hours(intern.daily_hours)
    average_hours = calculate_average_hours(intern.daily_hours)

    summary = f"""
INTERN ACTIVITY SUMMARY

Name    : {intern.name}
Role    : {intern.role}

Total Hours   : {total_hours:.2f}
Average Hours : {average_hours:.2f}

Task History

"""

    if len(intern.daily_tasks) == 0:
        summary += "No valid activities were recorded.\n"
    else:
        for i in range(len(intern.daily_tasks)):
            summary += (
                f"Day {i + 1}\n"
                f"  Hours : {intern.daily_hours[i]:.2f}\n"
                f"  Task  : {intern.daily_tasks[i]}\n\n"
            )

    return summary


class Intern:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.daily_hours = []
        self.daily_tasks = []

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "daily_hours": self.daily_hours,
            "daily_tasks": self.daily_tasks
        }


name = input("Enter intern name: ").strip().title()
role = input("Enter intern role: ").strip().title()

intern = Intern(name, role)

print()
print("Intern Created Successfully!")
print("Name:", intern.name)
print("Role:", intern.role)

days = int(input("How many days do you want to record? "))

for day in range(1, days + 1):

    try:
        hours = float(input(f"Enter hours for Day {day}: "))

        if hours < 0:
            print("Hours cannot be negative. Skipping this day.")
            continue

    except ValueError:
        print("Invalid input. Please enter a number. Skipping this day.")
        continue

    task = input(f"Enter task for Day {day}: ").strip()

    intern.daily_hours.append(hours)
    intern.daily_tasks.append(task)


print()
print(generate_summary(intern))


with open("intern.json", "w") as file:
    json.dump(intern.to_dict(), file, indent=4)


with open("intern.json", "r") as file:
    stored_data = json.load(file)


print()
print("JSON Data Verification")
print("-----------------------")
print("Name:", stored_data["name"])
print("Role:", stored_data["role"])
print("Daily Hours:", stored_data["daily_hours"])
print("Daily Tasks:", stored_data["daily_tasks"])