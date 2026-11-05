# Module Registration Checker

## Requirements
- Python 3.11 or later
- pytest (pip install pytest)

## How to run
Run all commands from inside the module_registration_checker folder.

**Part A (census totals):**
    python module_registration_checker/part_a/census_totals.py

**Part B (checker):**
    python module_registration_checker/part_b/checker.py

This writes the exceptions report to exceptions.csv.

**Tests:**
    pytest

## Assumptions
1. Dates in the file are DD/MM/YYYY, not YYYY-MM-DD as stated, so they are read as UK dates. This is reported once as DATE_FORMAT_INCORRECT.
2. Module codes are trimmed and upper-cased before matching, so 'cmp-1003 ' is counted as CMP-1003 but still reported as INVALID_MODULE_CODE.
3. A duplicate registration is counted once in credit totals.
4. A module not in modules.csv adds 0 credits.
5. Credits from a module that isn't running are still counted, as the registration exists on the record; it is reported separately.
6. Part-time students are expected to hold 60 credits. This isn't stated in the brief and needs confirming with Registry.
7. Withdrawn students are excluded from credit checks, but flagged if they still have registrations.
8. Over capacity is a module-level issue, so it has no student_id.
9. Part A Task 2 only compares active students.


### CHECKS:
**NO_ACTIVE_REGISTRATIONS** -> Active student with no active registrations.
**WITHDRAWN_WITH_REGISTRATIONS** -> Student is withdrawn but having active registrations.
**FT_CREDITS_NOT_120*** -> Full time students not having expected number of credits - 120
**PT_CREDITS_NOT_60** -> Part time students not having expected number of credits - 60
**INVALID_MODULE_CODE** -> Registered with an invalid(i.e not following the format)
**UNKNOWN_MODULE_CODE** -> Registered with an unknown(totally invalid module)
**DISALLOWED_MODULE_CODE** -> Registered with a module code which is not running in this academic year
**MODULE_OVER_CAPACITY** - Module has students with over capacity
**DUPLICATE_REGISTRATION** - Registered on same module more than once