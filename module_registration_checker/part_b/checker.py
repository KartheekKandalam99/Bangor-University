import csv
import re
from datetime import datetime

census_date = datetime(2026, 10, 1)

with open("data/students.csv") as f:
    students = list(csv.DictReader(f))

with open("data/registrations.csv") as f:
    registrations = list(csv.DictReader(f))

with open("data/modules.csv") as f:
    modules = list(csv.DictReader(f))

issues = []
modules_taken = []

for student in students:
    total_credits = 0
    counted_modules = []

    for reg in registrations:
        if reg["student_id"] != student["student_id"]:
            continue

        if datetime.strptime(reg["registered_on"], "%d/%m/%Y") > census_date:
            continue
        if reg["dropped_on"] != "" and datetime.strptime(reg["dropped_on"], "%d/%m/%Y") <= census_date:
            continue

        module_code = reg["module_code"].strip().upper()

        if not re.match(r"^[A-Z]{3}-\d{4}$", reg["module_code"]):
            issues.append({"issue_type": "INVALID_MODULE_CODE",
                           "student_id": student["student_id"], "module_code": module_code,
                           "description": f"Module code recorded as '{reg['module_code']}'. Correct it to {module_code}."})

        if module_code in counted_modules:
            issues.append({"issue_type": "DUPLICATE_REGISTRATION",
                           "student_id": student["student_id"], "module_code": module_code,
                           "description": f"Registered on {module_code} more than once. Remove the extra record."})
            continue
        counted_modules.append(module_code)

        found_module = None
        for module in modules:
            if module["module_code"] == module_code:
                found_module = module

        if found_module is None:
            issues.append({"issue_type": "UNKNOWN_MODULE_CODE",
                           "student_id": student["student_id"], "module_code": module_code,
                           "description": f"{module_code} is not in the module list. Re-register on the correct module."})
            continue

        if found_module["running"] != "Y":
            issues.append({"issue_type": "DISALLOWED_MODULE_CODE",
                           "student_id": student["student_id"], "module_code": module_code,
                           "description": f"{module_code} is not running this year. Move to a running module."})

        total_credits = total_credits + int(found_module["credits"])
        modules_taken.append(module_code)

    if student["status"] == "Withdrawn":
        if len(counted_modules) > 0:
            issues.append({"issue_type": "WITHDRAWN_WITH_REGISTRATIONS",
                           "student_id": student["student_id"], "module_code": "",
                           "description": f"Withdrawn but still on {len(counted_modules)} modules. Drop the registrations."})
        continue

    if len(counted_modules) == 0:
        issues.append({"issue_type": "NO_ACTIVE_REGISTRATIONS",
                       "student_id": student["student_id"], "module_code": "",
                       "description": "Active student with no modules. Register the student or check their status."})

    elif student["study_mode"] == "FT" and total_credits != 120:
        issues.append({"issue_type": "FT_CREDITS_NOT_120",
                       "student_id": student["student_id"], "module_code": "",
                       "description": f"Full-time student has {total_credits} credits, 120 expected."})

    elif student["study_mode"] == "PT" and total_credits != 60:
        issues.append({"issue_type": "PT_CREDITS_NOT_60",
                       "student_id": student["student_id"], "module_code": "",
                       "description": f"Part-time student has {total_credits} credits, 60 expected."})

for module in modules:
    number_of_students = modules_taken.count(module["module_code"])
    if number_of_students > int(module["capacity"]):
        issues.append({"issue_type": "MODULE_OVER_CAPACITY",
                       "student_id": "", "module_code": module["module_code"],
                       "description": f"{number_of_students} students but capacity is {module['capacity']}. Raise capacity or move students."})


with open("exceptions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["issue_type", "student_id", "module_code", "description"])
    writer.writeheader()
    writer.writerows(issues)

for issue in issues:
    print(issue["issue_type"], issue["student_id"], issue["module_code"])