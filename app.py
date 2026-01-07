import streamlit as st
from auth import login
from admin import admin_dashboard
from employee import employee_dashboard



from db import get_db
from auth import hash_password

db = get_db()
cur = db.cursor()

cur.execute("SELECT * FROM users WHERE role='admin'")
if not cur.fetchone():
    cur.execute("""
        INSERT INTO users (name,email,password,role)
        VALUES (?,?,?,?)
    """, (
        "Admin",
        "admin@actecal.com",
        hash_password("admin123"),
        "admin"
    ))
    db.commit()

if st.session_state.user is None:
    st.title("Login")

    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(email, pwd)
        if user:
            st.session_state.user = user
            st.rerun()   # NEW API (experimental_rerun deprecated)
        else:
            st.error("Invalid email or password")

else:
    user = st.session_state.user
    if user["role"] == "admin":
        admin_dashboard()
    else:
        employee_dashboard(user)

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
