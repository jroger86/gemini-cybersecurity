"""
Assignment 1: Gemini API — Cybersecurity experiments
Model: gemini-2.0-flash-lite  (free-tier quota available)
Run: python gemini_cybersecurity.py
Requires: GEMINI_API_KEY set in your environment (never in this file)
"""

import os
import sys
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    sys.exit("Error: GEMINI_API_KEY is not set. Export it before running:\n"
             "  export GEMINI_API_KEY=your_key_here")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash-lite"

SYSTEM_PROMPT = (
    "You are a senior application-security engineer. "
    "Be concise, precise, and reference relevant CVEs or CWEs where appropriate. "
    "Do not hallucinate vulnerability IDs — if you are unsure, say so."
)

EXPERIMENTS = [
    {
        "label": "Experiment 1 — SQL injection in Python",
        "expectation": (
            "Gemini should identify the unsanitised string interpolation as "
            "a classic SQL injection sink and suggest parameterised queries."
        ),
        "prompt": (
            "Review the following Python function for security vulnerabilities "
            "and explain how an attacker could exploit them:\n\n"
            "```python\n"
            "import sqlite3\n\n"
            "def get_user(username):\n"
            "    conn = sqlite3.connect('users.db')\n"
            "    cursor = conn.cursor()\n"
            "    query = f\"SELECT * FROM users WHERE username = '{username}'\"\n"
            "    cursor.execute(query)\n"
            "    return cursor.fetchone()\n"
            "```"
        ),
    },
    {
        "label": "Experiment 2 — Insecure password hashing",
        "expectation": (
            "Gemini should flag MD5 as cryptographically broken for passwords "
            "and recommend bcrypt, scrypt, or Argon2."
        ),
        "prompt": (
            "A developer stores user passwords like this:\n\n"
            "```python\n"
            "import hashlib\n\n"
            "def store_password(password):\n"
            "    return hashlib.md5(password.encode()).hexdigest()\n"
            "```\n\n"
            "What are the security problems with this approach and what "
            "should be used instead? Reference relevant CWEs."
        ),
    },
    {
        "label": "Experiment 3 — Reflected XSS in a Flask route",
        "expectation": (
            "Gemini should spot that user input is rendered unescaped and "
            "explain a reflected XSS payload."
        ),
        "prompt": (
            "Identify any vulnerabilities in this Flask route and show a "
            "proof-of-concept exploit URL:\n\n"
            "```python\n"
            "from flask import Flask, request\n\n"
            "app = Flask(__name__)\n\n"
            "@app.route('/search')\n"
            "def search():\n"
            "    query = request.args.get('q', '')\n"
            "    return f'<h1>Results for: {query}</h1>'\n"
            "```"
        ),
    },
]


def run_experiment(exp: dict) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n" + exp["prompt"]}]}
        ],
    )
    return response.text


def separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main() -> None:
    print(f"Model: {MODEL}")
    for exp in EXPERIMENTS:
        separator(exp["label"])
        print(f"\nExpectation: {exp['expectation']}\n")
        print("--- Prompt ---")
        print(exp["prompt"])
        print("\n--- Gemini Response ---")
        answer = run_experiment(exp)
        print(answer)


if __name__ == "__main__":
    main()
