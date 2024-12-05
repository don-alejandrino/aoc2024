import re
import time

import numpy as np

EXAMPLE1 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def parse_input(text: str) -> list[np.array]:
    reports = []
    for line in text.strip().split("\n"):
        row = np.array(list(map(lambda x: int(x.strip()), re.split(r"\s", line.strip()))))
        reports.append(row)

    return reports


def is_report_safe(report: np.array) -> bool:
    diffs = np.diff(report)
    if ((diffs > 0).all() | (diffs < 0).all()) & (np.abs(diffs) <= 3).all():
        return True
    else:
        return False


def find_safe_reports(reports: list[np.array]) -> int:
    num_safe_reports = 0
    for report in reports:
        if is_report_safe(report):
            num_safe_reports += 1

    return num_safe_reports


def find_safe_reports_including_problem_dampener_brute_force(reports: list[np.array]) -> int:
    num_safe_reports = 0
    for report in reports:
        for idx in range(len(report)):
            corrected_report = np.delete(report, idx)
            if is_report_safe(corrected_report):
                num_safe_reports += 1
                break

    return num_safe_reports


def find_safe_reports_including_problem_dampener(reports: list[np.array]) -> int:
    num_safe_reports = 0
    for report in reports:
        diffs = np.diff(report)
        diff_signs = np.sign(diffs)
        diff_signs_direction = -1 if diff_signs.mean() <= 0 else 1
        diff_signs = diff_signs - diff_signs_direction
        monotony_outliers = (diff_signs != 0)
        threshold_outliers = (np.abs(diffs) > 3)
        outliers = monotony_outliers | threshold_outliers
        if outliers.sum() == 0:
            num_safe_reports += 1
        elif outliers.sum() <= 2:
            outliers = np.insert(outliers, 0, False)
            outlier_idcs = np.where(outliers)[0]
            for outlier_idx in outlier_idcs:
                corrected_report_a = np.delete(report, outlier_idx)
                corrected_report_b = np.delete(report, outlier_idx - 1)
                if is_report_safe(corrected_report_a) or is_report_safe(corrected_report_b):
                    num_safe_reports += 1
                    break

    return num_safe_reports


if __name__ == "__main__":
    with open("../inputs/02.txt", "r") as fh:
        in_text = fh.read()

    report_matrix = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_safe_reports(report_matrix)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2 (brute force approach)
    start = time.perf_counter()
    res_brute_force = find_safe_reports_including_problem_dampener_brute_force(report_matrix)
    end = time.perf_counter()
    print(f"Part 2 Brute Force Result: {res_brute_force}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2 (refined approach)
    start = time.perf_counter()
    res = find_safe_reports_including_problem_dampener(report_matrix)
    end = time.perf_counter()
    print(f"Part 2 Refined Approach Result: {res}. Took {(end - start) * 1000:.2f} ms.")
