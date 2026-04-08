# Hack A Password

A browser-based password security game built with Flask and vanilla JavaScript. Players submit a password, watch it get "cracked" by a simulated brute-force engine, and receive a detailed performance summary. Results are ranked on a live leaderboard so players can compete for the strongest password.

---

## How It Works

1. Enter a username and password on the home screen and click **Analyze Password**
2. The loading screen simulates a cracking attempt while your password is analyzed server-side
3. After the timer expires, click **Continue** to view your **Performance Summary** — including character breakdown, strength rating, and any detected weaknesses
4. Click **View Leaderboard** to see how your password ranked against other players in the current session

---

## Features

- **Password entropy analysis** — calculates bits of entropy based on character pool size and length
- **Breach database check** — flags substrings found in the RockYou dataset (14M+ leaked passwords)
- **Dictionary check** — flags common English words found within the password
- **Strength rating** — classifies passwords as Weak, Medium, or Strong
- **Estimated crack time** — simulates crack time using 10, 100, 1,000, and 1,000,000 virtual GPUs
- **Live leaderboard** — top 5 players ranked by crack time resistance, reset each session for privacy
- **Session privacy** — the leaderboard JSON is wiped every time the server restarts; no data persists between sessions

---

## Project Structure

```
hack-a-password/
│
├── main.py                  # Flask app and all routes
│
├── function/
│   ├── __init__.py
│   ├── entropy_calculator.py      # Entropy and crack time estimation
│   ├── fileCheckerFunctions.py    # Breach and dictionary matching
│   └── functions.py               # Input validation and password parsing
│
├── frontend/
│   ├── index.html
│   ├── loadingScreen.html
│   ├── performanceSummary.html
│   └── leaderboard.html
│
├── static/
│   └── images/
│       └── matrix.gif
│
└── data/
    ├── rockyou.txt          # Breach password dataset (not included, see below)
    ├── words.txt            # English dictionary dataset (not included, see below)
    └── crack_times.json     # Auto-generated at runtime; wiped on each restart
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip

### Install dependencies

```bash
pip install flask
```

### Datasets

This project requires two external datasets placed in the `data/` folder:

- **rockyou.txt** — the RockYou breach dataset. Widely available for security research purposes. Contains 14,341,564 unique passwords, used in 32,603,388 accounts.
Download at https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt
- **words.txt** — any standard English word list. Download one from https://www.kaggle.com/datasets/lennartluik/all-english-words-csv

Place both files in the `data/` directory before running.

### Run the app

```bash/terminal
python main.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

```
Terminate program using Ctrl + C 
```

> **Do not** open the HTML files directly in your browser or use the VS Code Live Server extension — the app requires Flask to handle routing and password analysis.

---

## Password Rules

- Must be between 1 and 16 characters
- No spaces allowed

---

## Strength Thresholds

| Strength | Entropy Range     |
|----------|-------------------|
| Weak     | Below 40 bits     |
| Medium   | 40 – 59 bits      |
| Strong   | 60 bits and above |

---

## Notes

- The leaderboard ranks by estimated crack time (higher = stronger), showing the top 5 players
- All leaderboard data is stored in memory only for the duration of the server session
- The loading screen timer is set to 15 seconds by default for testing — change `WAIT_MS` in `loadingScreen.html` to `300000` for the intended 5-minute experience
