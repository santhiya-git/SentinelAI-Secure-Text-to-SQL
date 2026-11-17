# 🛡️ SentinelAI — Secure Text-to-SQL Engine

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
[![USM Security](https://img.shields.io/badge/USM-Security%20Firewall-green.svg)](https://github.com/santhiya-git/SentinelAI-Secure-Text-to-SQL)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SentinelAI** is an enterprise-grade, zero-failure Generative AI Text-to-SQL engine featuring an automated **USM (Unified Security Management)** security firewall, a resilient hybrid API/local fallback architecture, and a modern high-contrast SaaS user interface. 

Designed specifically for job interviews and technical showcases, it bridges natural language querying with robust backend security and guaranteed 100% presentation uptime.

---

## 🚀 Key Features

* **Natural Language to SQL Translation:** Instantly converts human questions into precise SQLite queries.
* **USM Security Governance (`firewall.py`):** An independent modular security layer that inspects generated SQL statements in real-time, blocking unauthorized or destructive commands (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`).
* **Zero-Failure Hybrid Architecture:** Features an advanced local regex-based semantic parser (`generate_sql_locally`) that automatically takes over during high-demand API traffic congestion or offline states, guaranteeing 100% uptime during live demos.
* **High-Contrast SaaS UI:** Built with Streamlit using a professional bright palette (`#F8FAFC` background, `#0F172A` deep text, and `#FF4B32` coral accents) for a polished, modern developer platform experience.
* **Live Database Execution:** Securely executes validated read-only queries against a local SQLite database (`sentinel.db`) and renders results instantly via interactive DataFrames.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend UI:** Streamlit
* **Database:** SQLite & Pandas
* **Security & Parsing:** Modular Python scripts & Regular Expressions (`re`)

---

## 📂 Project Structure

```text
SentinelAI/
│
├── app.py              # Main Streamlit application, UI, local NLP parser, and database executor
├── firewall.py         # USM security governance and threat interception module
├── requirements.txt    # Python package dependencies
├── .gitignore          # Excludes temporary caches, local DB, and environment secrets
└── sentinel.db         # Local SQLite sample database (auto-generated)
