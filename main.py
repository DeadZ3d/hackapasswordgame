from flask import Flask, render_template, request, jsonify
import json
import os

from function.entropy_calculator import entropy
from function.fileCheckerFunctions import englishWordsChecker, existingPasswordChecker
from function.functions import (
    get_digits_info,
    get_password_size,
    get_symbols_info,
    inputValidation,
    tokenize_string,
)

app = Flask(__name__, template_folder="frontend")

CRACK_TIMES_FILE = "data/crack_times.json"

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Wipe the leaderboard on every startup for privacy
with open(CRACK_TIMES_FILE, "w") as f:
    json.dump([], f)


def save_result_to_json(name, metrics, crack_time_seconds):
    with open(CRACK_TIMES_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append({
        "name": name,
        "metrics": metrics,
        "crack_time_seconds": crack_time_seconds
    })

    with open(CRACK_TIMES_FILE, "w") as f:
        json.dump(data, f, indent=4)


def calculate_strength_level(entropy_value):
    """Maps entropy bits to a human-readable strength label."""
    if entropy_value < 40:
        return "Weak"
    elif entropy_value < 60:
        return "Medium"
    else:
        return "Strong"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loading")
def loading():
    return render_template("loadingScreen.html")


@app.route("/submit_password", methods=["POST"])
def submit_password():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if inputValidation(password):
        return jsonify({"error": "Password must be 1–16 characters with no spaces."}), 400

    # Analyze password
    tokens = tokenize_string(password)
    password_size = get_password_size(password)
    digits, digit_positions = get_digits_info(password)
    symbols, symbol_positions = get_symbols_info(password)
    leaked_matches = existingPasswordChecker(password, [])
    english_matches = englishWordsChecker(password, [])

    crack_times = entropy(password, leaked_matches, english_matches)

    # Use 100-GPU crack time as the leaderboard score
    crack_time_100 = crack_times.get(100, 0)

    # Calculate real entropy for strength label
    import math
    from function.entropy_calculator import estimate_poolsize
    pool = estimate_poolsize(password)
    raw_entropy = password_size * math.log(pool, 2) if pool > 0 else 0
    strength = calculate_strength_level(raw_entropy)

    metrics = {
        "length": password_size,
        "uppercase": sum(1 for c in password if c.isupper()),
        "lowercase": sum(1 for c in password if c.islower()),
        "digits": len(digits),
        "symbols": len(symbols),
        "strength": strength,
        "tokens": tokens,
        "leaked_matches": leaked_matches,
        "english_matches": english_matches,
        "crack_time_seconds": crack_time_100,
    }

    save_result_to_json(username, metrics, crack_time_100)

    # Compute rank after saving
    with open(CRACK_TIMES_FILE, "r") as f:
        all_data = json.load(f)

    sorted_data = sorted(all_data, key=lambda x: x["crack_time_seconds"], reverse=True)
    rank = next((i + 1 for i, entry in enumerate(sorted_data) if entry["name"] == username), 1)
    total = len(sorted_data)

    metrics["rank"] = rank
    metrics["totalPlayers"] = total

    return jsonify({"metrics": metrics, "crack_time_seconds": crack_time_100})


@app.route("/performance_summary")
def performance_summary():
    return render_template("performanceSummary.html")


@app.route("/leaderboard_data")
def leaderboard_data():
    """Return top-5 leaderboard sorted by crack_time_seconds descending."""
    with open(CRACK_TIMES_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    sorted_data = sorted(data, key=lambda x: x["crack_time_seconds"], reverse=True)
    return jsonify(sorted_data[:5])  # Top 5 only


@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")


if __name__ == "__main__":
    app.run(debug=True)