"""
Assignment 1: Gemini API — Browser-based red team / web pen testing
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
    "You are a senior web application penetration tester. "
    "Think like an attacker. Identify vulnerabilities, explain how to exploit them "
    "from a browser, and suggest the MITRE ATT&CK or OWASP category where relevant. "
    "Do not fabricate CVE or CWE numbers — if unsure, say so."
)

EXPERIMENTS = [
    {
        "label": "Experiment 1 — DOM-based XSS via location.hash",
        "expectation": (
            "Gemini should identify that writing location.hash into innerHTML "
            "without sanitization is a DOM XSS sink (CWE-79). It should show "
            "a working payload URL like: page.html#<img src=x onerror=alert(1)>"
        ),
        "prompt": (
            "A developer wrote this JavaScript to show a welcome message:\n\n"
            "```html\n"
            "<!DOCTYPE html>\n"
            "<html>\n"
            "<body>\n"
            "  <div id='msg'></div>\n"
            "  <script>\n"
            "    // Read the page anchor and display it\n"
            "    document.getElementById('msg').innerHTML = decodeURIComponent(location.hash.slice(1));\n"
            "  </script>\n"
            "</body>\n"
            "</html>\n"
            "```\n\n"
            "As a pen tester, identify the vulnerability, craft a proof-of-concept "
            "exploit URL, and explain how an attacker would deliver it to a victim."
        ),
    },
    {
        "label": "Experiment 2 — CSRF on a state-changing endpoint",
        "expectation": (
            "Gemini should identify missing CSRF token as OWASP A01/CWE-352. "
            "It should write a malicious HTML page that auto-submits a form "
            "to the victim's bank/app from a different origin."
        ),
        "prompt": (
            "A Flask app lets logged-in users change their email address:\n\n"
            "```python\n"
            "from flask import Flask, request, session\n\n"
            "app = Flask(__name__)\n\n"
            "@app.route('/settings/email', methods=['POST'])\n"
            "def change_email():\n"
            "    if 'user_id' not in session:\n"
            "        return 'Unauthorized', 401\n"
            "    new_email = request.form['email']\n"
            "    update_email(session['user_id'], new_email)\n"
            "    return 'Email updated'\n"
            "```\n\n"
            "As a pen tester, explain the vulnerability and write a malicious HTML "
            "page hosted on attacker.com that silently changes the victim's email "
            "when they visit it while logged in."
        ),
    },
    {
        "label": "Experiment 3 — Open redirect to phishing",
        "expectation": (
            "Gemini should identify the unvalidated redirect (CWE-601) and show "
            "how an attacker chains it with a phishing page. A URL like "
            "/login?next=https://evil.com looks trusted because it starts with "
            "the real domain."
        ),
        "prompt": (
            "A login page redirects users to a 'next' URL after authentication:\n\n"
            "```python\n"
            "from flask import Flask, request, redirect, session\n\n"
            "app = Flask(__name__)\n\n"
            "@app.route('/login', methods=['POST'])\n"
            "def login():\n"
            "    username = request.form['username']\n"
            "    password = request.form['password']\n"
            "    if authenticate(username, password):\n"
            "        session['user'] = username\n"
            "        next_url = request.args.get('next', '/dashboard')\n"
            "        return redirect(next_url)\n"
            "    return 'Invalid credentials', 401\n"
            "```\n\n"
            "As a pen tester, explain how to exploit this for phishing, write "
            "the malicious link you would send the victim, and describe what "
            "the victim sees that makes it convincing."
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
