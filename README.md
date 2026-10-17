# Gemini Cybersecurity Experiments

Assignment 1 — first Gemini API call, applied to cybersecurity code review.

## What this does

Sends three security-focused code snippets to the Gemini API and records what
the model identifies, misses, or gets wrong. Each experiment includes:

- **Expectation** — what a human expert would flag
- **Prompt** — the code and question sent to the model
- **Response** — Gemini's raw output
- **Assessment** — what it got right, wrong, or fabricated

---

## Setup

### 1. Clone and enter the repo

```bash
git clone https://github.com/<your-handle>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key (never commit this)

Get a free key from https://aistudio.google.com/apikey then:

```bash
export GEMINI_API_KEY=your_key_here
```

Add that line to your shell's rc file (`~/.zshrc`, `~/.bashrc`) to persist it.

### 5. Run

```bash
python gemini_cybersecurity.py
```

---

## Model

`gemini-2.0-flash-lite` — chosen for free-tier availability.

---

## Experiments

### Experiment 1 — SQL Injection in Python

**Prompt:** Asks Gemini to review a Flask route that builds a SQL query with
f-string interpolation.

**Expectation:** Should identify the unsanitised string as a SQL injection
sink (CWE-89) and recommend parameterised queries.

**Response:**
> *(paste Gemini's output here after running)*

**Assessment:**
> *(What did it get right? What did it miss? Did it hallucinate any CVE/CWE
> numbers? Did you verify any claim with your own knowledge?)*

---

### Experiment 2 — Insecure Password Hashing

**Prompt:** Asks Gemini to critique a function that stores passwords as raw
MD5 hashes.

**Expectation:** Should flag MD5 as cryptographically broken for passwords
(CWE-916) and recommend Argon2, bcrypt, or scrypt.

**Response:**
> *(paste Gemini's output here after running)*

**Assessment:**
> *(fill in)*

---

### Experiment 3 — Reflected XSS in Flask

**Prompt:** Asks Gemini to find vulnerabilities in a route that echoes a
query parameter directly into HTML without escaping.

**Expectation:** Should identify reflected XSS (CWE-79) and show a payload
URL like `?q=<script>alert(1)</script>`.

**Response:**
> *(paste Gemini's output here after running)*

**Assessment:**
> *(fill in)*

---

## Reflection

> *(Write 3–5 sentences: What surprised you? Where was Gemini confident but
> wrong? What would you not trust it to do alone?)*

---

## Files

| File | Purpose |
|------|---------|
| `gemini_cybersecurity.py` | Main script — runs all three experiments |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Keeps `.env` and keys out of Git |
| `README.md` | This file |
