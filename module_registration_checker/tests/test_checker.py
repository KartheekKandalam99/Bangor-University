import csv
import os
import subprocess

os.chdir("tests/sample")
subprocess.run(["python", "../../part_b/checker.py"], check=True)

report = []
with open("exceptions.csv") as f:
    for row in csv.DictReader(f):
        report.append(row["issue_type"] + " " + row["student_id"] + " " + row["module_code"])


def test_student_on_120_has_no_issues():
    for line in report:
        assert " T1 " not in line


def test_full_time_under_120():
    assert "FT_CREDITS_NOT_120 T2 " in report


def test_no_registrations():
    assert "NO_ACTIVE_REGISTRATIONS T3 " in report


def test_withdrawn_still_registered():
    assert "WITHDRAWN_WITH_REGISTRATIONS T4 " in report


def test_part_time_not_60():
    assert "PT_CREDITS_NOT_60 T5 " in report


def test_duplicate_and_typo_reported_but_credits_correct():
    assert "DUPLICATE_REGISTRATION T6 TST-1005" in report
    assert "INVALID_MODULE_CODE T6 TST-1002" in report
    assert "FT_CREDITS_NOT_120 T6 " not in report


def test_unknown_module():
    assert "UNKNOWN_MODULE_CODE T7 XXX-9999" in report


def test_module_not_running():
    assert "DISALLOWED_MODULE_CODE T8 OLD-1001" in report


def test_module_over_capacity():
    assert "MODULE_OVER_CAPACITY  TST-1006" in report