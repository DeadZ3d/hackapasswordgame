# Nwabueze-Umeh Izuchukwu's functions that checks files
import os
import re

ALPHANUMERIC_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")
PASSWORD_PARTS_PATTERN = re.compile(r"[A-Za-z]+|\d+")


def get_password_parts(password):
    return PASSWORD_PARTS_PATTERN.findall(password)


def existingPasswordChecker(password, matchedList):
    file_path = "data/rockyou.txt"
    if not os.path.exists(file_path):
        return matchedList

    password_parts = get_password_parts(password)

    with open(file_path, "r", encoding="latin-1", errors="ignore") as file_handle:
        for line in file_handle:
            clean_line = line.strip()

            if not clean_line:
                continue

            if not ALPHANUMERIC_PATTERN.match(clean_line):
                continue

            if clean_line in password_parts and clean_line not in matchedList:
                matchedList.append(clean_line)

    return matchedList


def englishWordsChecker(password, matchedList):
    file_path = "data/words.txt"
    if not os.path.exists(file_path):
        return matchedList

    password_parts = get_password_parts(password.lower())

    with open(file_path, "r", encoding="latin-1", errors="ignore") as file_handle:
        for line in file_handle:
            clean_line = line.strip()

            if not clean_line:
                continue

            if not ALPHANUMERIC_PATTERN.match(clean_line):
                continue

            if clean_line.lower() in password_parts and clean_line not in matchedList:
                matchedList.append(clean_line)

    return matchedList
