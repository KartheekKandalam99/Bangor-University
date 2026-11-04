"""
CHECKS:
1. NO_ACTIVE_REGISTRATIONS -> Active student with no active registrations.
2. WITHDRAWN_WITH_REGISTRATIONS -> Student is withdrawn but having active registrations.
3. FT_CREDITS_NOT_120 -> Full time students not having expected number of credits - 120
4. PT_CREDITS_NOT_60 -> Part time students not having expected number of credits - 60
5. INVALID_MODULE_CODE -> Registered with an invalid(i.e not following the format)
6. UNKNOWN_MODULE_CODE -> Registered with an unknown(totally invalid module)
7. DISALLOWED_MODULE_CODE -> Registered with a module code which is not running in this academic year
8. DATE_FORMAT_INCORRECT - Dates are not in YYYY-MM-DD format
9. MODULE_OVER_CAPACITY - Module has students with over capacity
10. DUPLICATE_REGISTRATION - Registered on same module more than once
"""

