import streamlit as st
from auth import login, hash_password
from admin import admin_dashboard
from employee import employee_dashboard
from db import get_db


# -------------------- DB INIT --------------------
db = get_db()
cur = db.cursor()

cur.execute("SELECT 1 FROM users WHERE role='admin'")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (
        "Admin",
        "admin@actecal.com",
        hash_password("admin123"),
        "admin"
    ))
    db.commit()


# -------------------- SESSION INIT --------------------
if "user" not in st.session_state:
    st.session_state.user = None


# -------------------- LOGIN --------------------
if st.session_state.user is None:
    st.title("Login")

    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(email, pwd)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid email or password")


# -------------------- DASHBOARD --------------------
else:
    user = st.session_state.user

    if user["role"] == "admin":
        admin_dashboard()
    else:
        employee_dashboard(user)

    st.divider()

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
