import json
import os

from function.entropy_calculator import entropy
from function.fileCheckerFunctions import (
    englishWordsChecker,
    existingPasswordChecker,
)
from function.functions import (
    get_digits_info,
    get_password_size,
    get_symbols_info,
    inputValidation,
    tokenize_string,
)


def format_time(seconds):
    total_seconds = int(seconds)

    days = total_seconds // 86400
    remaining_seconds = total_seconds % 86400

    hours = remaining_seconds // 3600
    remaining_seconds = remaining_seconds % 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return f"{days}:{hours:02}:{minutes:02}:{seconds:02}"


def get_time_to_crack(seconds):
    if seconds >= 31536000:
        return f"{seconds / 31536000:.2f} years"
    elif seconds >= 86400:
        return f"{seconds / 86400:.2f} days"
    elif seconds >= 3600:
        return f"{seconds / 3600:.2f} hours"
    elif seconds >= 60:
        return f"{seconds / 60:.2f} minutes"
    else:
        return f"{seconds:.2f} seconds"


def save_result_to_json(name, crack_time_seconds):
    file_path = "data/crack_times.json"
    new_record = {
        "name": name,
        "crack_time_seconds": crack_time_seconds
    }

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file_handle:
            try:
                data = json.load(file_handle)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_record)

    with open(file_path, "w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, indent=4)


def main():
    print("Disclaimer: No password or username is stored.")
    user_name = input("Enter your name: ")
    password = input("Enter a password: ")

    # Keep asking until the password follows the rules in functions.py
    while inputValidation(password):
        password = input(
            "Invalid password. It must be 1-16 characters with no spaces. Try another one: "
        )

    tokens = tokenize_string(password)
    password_size = get_password_size(password)
    digits, digit_positions = get_digits_info(password)
    symbols, symbol_positions = get_symbols_info(password)

    leaked_matches = existingPasswordChecker(password, [])
    english_matches = englishWordsChecker(password, [])
    crack_times = entropy(password, leaked_matches, english_matches)
    save_result_to_json(user_name, crack_times[100])

    print()
    print(f"Password length: {password_size}")
    print(f"Tokens: {tokens}")

    if english_matches:
        print(f"English words found: {english_matches}")
    else:
        print("English words found: none")

    if leaked_matches:
        print(f"Leaked password fragments found: {leaked_matches}")
    else:
        print("Leaked password fragments found: none")

    print("\nEstimated crack time by attacker type:")
    print(f"10 GPUs (run of the mill hacker): {get_time_to_crack(crack_times[10])}")
    print(f"100 GPUs (dedicated attacker): {get_time_to_crack(crack_times[100])}")
    print(f"1000 GPUs (criminal organization): {get_time_to_crack(crack_times[1000])}")
    print(f"1000000 GPUs (nation state): {get_time_to_crack(crack_times[1000000])}")


if __name__ == "__main__":
    main()
