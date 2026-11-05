"""
This code below generates single list combining 2 requests.

#1 - A list of every active student with their total credits from active registration on the census date, including students with no registrations.
#2 - A list of students whose total on the census date is different from their total on 31st of October 2026, showing both figures

My plan: Loop through "Active" status students, checks each of their registrations is active(registered on or before and not dropped on or before) on census date, and then looks up the module's credits and add them
to total credits. Repeat the same steps but this time compare the dates with 31st Oct and total them and print the differences. Since it requires same loginc, combining them in single code and looping the code twice on census date and later date.


"""

import csv
from datetime import datetime

census_date = datetime(2026, 10, 1)
october_31 = datetime(2026, 10, 31)

with open("module_registration_checker/data/students.csv") as f:
    students = list(csv.DictReader(f))

with open("module_registration_checker/data/registrations.csv") as f:
    registrations = list(csv.DictReader(f))

with open("module_registration_checker/data/modules.csv") as f:
    modules = list(csv.DictReader(f))

print("student_id, census_total, different?, total_on_oct_31")
for student in students:
    if student["status"] != "Active":
        continue
    totals = []
    for on_date in [census_date, october_31]:
        total_credits = 0
        counted_modules = []
        for reg in registrations:
            if reg["student_id"] != student["student_id"]:
                continue
            if datetime.strptime(reg["registered_on"], "%d/%m/%Y") > on_date:
                continue
            if reg["dropped_on"] != "" and datetime.strptime(reg["dropped_on"], "%d/%m/%Y") <= on_date:
                continue
            module_code = reg["module_code"].strip().upper()
            if module_code in counted_modules:
                continue
            counted_modules.append(module_code)
            for module in modules:
                if module["module_code"] == module_code:
                    total_credits = total_credits + int(module["credits"])
        totals.append(total_credits)
    census_total, october_total = totals
    if census_total != october_total:
        print(student["student_id"], census_total, "Y", october_total)
    else:
        print(student["student_id"], census_total, "N", "")
