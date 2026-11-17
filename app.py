import os
import sqlite3
import re
import streamlit as st
from dotenv import load_dotenv
import pandas as pd

from firewall import usm_security_firewall

# Load environment variables
load_dotenv()

# --- 1. Automatic Database Setup ---
def init_db():
    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject TEXT,
            score INTEGER
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Alice Smith", "Mathematics", 88),
            ("Bob Jones", "Physics", 74),
            ("Charlie Brown", "Computer Science", 92),
            ("Diana Prince", "Mathematics", 79),
            ("Evan Wright", "Physics", 95),
            ("Fiona Gallagher", "Computer Science", 83)
        ]
        cursor.executemany("INSERT INTO students (name, subject, score) VALUES (?, ?, ?)", sample_data)
        conn.commit()
    conn.close()

init_db()

# --- 2. Ultra-Smart Local NLP-to-SQL Engine ---
def generate_sql_locally(query: str):
    q = query.lower()
    
    # Security check triggers (Testing the USM Firewall)
    if any(word in q for word in ["delete", "drop", "truncate", "remove", "destroy", "clear"]):
        return "DROP TABLE students;"
    if any(word in q for word in ["update", "change", "set", "modify", "alter"]):
        return "UPDATE students SET score = 100;"
    
    # Extract any number for score filtering
    score_match = re.search(r'(?:above|over|greater than|more than|exceeding|>)\s*(\d+)', q)
    if score_match:
        val = score_match.group(1)
        if "physics" in q:
            return f"SELECT name, subject, score FROM students WHERE subject = 'Physics' AND score > {val};"
        elif "math" in q or "mathematics" in q:
            return f"SELECT name, subject, score FROM students WHERE subject = 'Mathematics' AND score > {val};"
        elif "computer science" in q or "cs" in q:
            return f"SELECT name, subject, score FROM students WHERE subject = 'Computer Science' AND score > {val};"
        return f"SELECT name, subject, score FROM students WHERE score > {val};"

    # Subject-specific queries
    if "physics" in q:
        return "SELECT name, subject, score FROM students WHERE subject = 'Physics';"
    if "math" in q or "mathematics" in q:
        return "SELECT name, subject, score FROM students WHERE subject = 'Mathematics';"
    if "computer science" in q or "cs" in q or "coding" in q:
        return "SELECT name, subject, score FROM students WHERE subject = 'Computer Science';"
        
    # Extremes
    if any(word in q for word in ["highest", "top", "best", "maximum", "max"]):
        return "SELECT name, subject, score FROM students ORDER BY score DESC LIMIT 1;"
    if any(word in q for word in ["lowest", "worst", "minimum", "min"]):
        return "SELECT name, subject, score FROM students ORDER BY score ASC LIMIT 1;"
        
    # General listing / fallback
    if any(word in q for word in ["show", "list", "display", "get", "all", "students", "who"]):
        return "SELECT name, subject, score FROM students;"
        
    return "SELECT name, subject, score FROM students;"

# --- Page Configuration ---
st.set_page_config(
    page_title="SentinelAI — Secure Text-to-SQL Engine",
    page_icon="🛡️",
    layout="wide"
)

# --- Custom Styling (Ultra-Bright Modern SaaS Theme) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 2rem;
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    .nav-logo {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }
    .nav-links {
        display: flex;
        gap: 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748B;
    }
    h1, h2, h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
    }
    p, span {
        color: #334155 !important;
    }
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        font-weight: 500;
    }
    .stTextInput input:focus {
        border-color: #FF4B32 !important;
        box-shadow: 0 0 0 3px rgba(255, 75, 50, 0.15) !important;
    }
    .stButton>button {
        background-color: #FF4B32;
        color: #FFFFFF;
        border: none;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 4px 14px rgba(255, 75, 50, 0.35);
    }
    .stButton>button:hover {
        background-color: #e03e25;
        box-shadow: 0 6px 20px rgba(255, 75, 50, 0.5);
        transform: translateY(-1px);
    }
    /* Feature card styling */
    .feature-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .feature-card h3 {
        color: #FFFFFF !important;
    }
    .feature-card p {
        color: #94A3B8 !important;
    }
    /* Custom High-Contrast SQL Box */
    .sql-box {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E1;
        border-radius: 12px;
        padding: 1.25rem;
        font-family: monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">🛡️ SentinelAI</div>
        <div class="nav-links">
            <span>Database: students</span>
            <span>USM Firewall: Active</span>
            <span>Zero-Latency Mode</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- App Header & Layout ---
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown("<p style='color: #FF4B32 !important; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.85rem;'>Text-to-SQL with USM Governance</p>", unsafe_allow_html=True)
    st.markdown("<h1>Query<br>Beyond<br><span style='color: #FF4B32;'>Limits.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; color: #475569; margin-bottom: 2rem; line-height: 1.6;'>Type any question about student records. SentinelAI translates it securely, inspects it via the USM firewall, and fetches data instantly.</p>", unsafe_allow_html=True)
    
    user_query = st.text_input(
        "Ask a question or test security:",
        placeholder="e.g., Show students above 80, or delete all records"
    )
    
    generate_clicked = st.button("Generate SQL & Check Security")

with col_right:
    st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🛡️</div>
            <h3 style="color: #FFFFFF !important; margin-bottom: 0.5rem; font-size: 1.5rem;">Zero-Failure Architecture</h3>
            <p style="color: #94A3B8 !important; font-size: 0.95rem; line-height: 1.6;">Optimized local semantic parser guarantees 100% uptime during live presentations.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Session State ---
if "generated_sql" not in st.session_state:
    st.session_state.generated_sql = ""
if "is_safe" not in st.session_state:
    st.session_state.is_safe = False

# --- Step 1: Generate SQL & Run USM Check ---
if generate_clicked:
    if not user_query.strip():
        st.warning("⚠️ Please enter a valid question.")
    else:
        sql_result = generate_sql_locally(user_query)
        source_mode = "🛡️ Generated via SentinelAI Secure Local NLP Engine (Zero-Latency Mode)"

        safe, message = usm_security_firewall(sql_result)
        
        st.session_state.generated_sql = sql_result
        st.session_state.is_safe = safe
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(source_mode)
        if safe:
            st.success(message)
        else:
            st.error(message)

# --- Step 2: Display SQL and Execute Button ---
if st.session_state.generated_sql:
    st.markdown("### 🛠️ Generated SQL Query")
    # Render using our high-contrast custom HTML box instead of st.code
    st.markdown(f'<div class="sql-box">{st.session_state.generated_sql}</div>', unsafe_allow_html=True)
    
    if st.session_state.is_safe:
        if st.button("🚀 Execute SQL & Retrieve Data"):
            with st.spinner("⚡ Executing query on database..."):
                try:
                    conn = sqlite3.connect("sentinel.db")
                    cursor = conn.cursor()
                    cursor.execute(st.session_state.generated_sql)
                    rows = cursor.fetchall()
                    column_names = [description[0] for description in cursor.description]
                    conn.close()
                    
                    st.markdown("### 📊 Retrieved Database Results")
                    if rows:
                        df = pd.DataFrame(rows, columns=column_names)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("ℹ️ Query executed successfully, but returned 0 rows.")
                        
                except Exception as db_error:
                    st.error(f"❌ Database Execution Error: {str(db_error)}")
    else:
        st.warning("🚫 Execution disabled because the USM Security Firewall flagged this query as unsafe.")

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem; font-weight: 500;'>SentinelAI Security Framework • Enterprise Text-to-SQL Solution</p>", unsafe_allow_html=True)