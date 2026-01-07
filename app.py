import streamlit as st
from auth import login
from admin import admin_dashboard
from employee import employee_dashboard

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("Login")
    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(email, pwd)
        if user:
            st.session_state.user = user
            st.experimental_rerun()
        else:
            st.error("Invalid login")
else:
    user = st.session_state.user
    if user["role"] == "admin":
        admin_dashboard()
    else:
        employee_dashboard(user)

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
