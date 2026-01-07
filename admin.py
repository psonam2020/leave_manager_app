import streamlit as st
import pandas as pd
from db import get_db
from auth import hash_password

def admin_dashboard():
    st.title("Admin Panel")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Leave Types", "Employees", "Leave Requests", "Reports"]
    )

    db = get_db()

    # LEAVE TYPES
    with tab1:
        name = st.text_input("Leave Name")
        total = st.number_input("Yearly Count", 0)
        if st.button("Save Leave"):
            db.execute(
                "INSERT OR IGNORE INTO leave_types (name,total_per_year) VALUES (?,?)",
                (name, total)
            )
            db.commit()
            st.success("Saved")

    # EMPLOYEE CREATE
    with tab2:
        name = st.text_input("Employee Name")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")

        if st.button("Create Employee"):
            cur = db.cursor()
            cur.execute(
                "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
                (name, email, hash_password(pwd), "employee")
            )
            uid = cur.lastrowid

            cur.execute("SELECT * FROM leave_types")
            for lt in cur.fetchall():
                cur.execute(
                    "INSERT INTO leave_balances (user_id,leave_type_id,balance) VALUES (?,?,?)",
                    (uid, lt["id"], lt["total_per_year"])
                )
            db.commit()
            st.success("Employee created")

    # LEAVE REQUESTS
    with tab3:
        rows = db.execute("""
            SELECT lr.id,u.name,lt.name as leave,start_date,end_date,days
            FROM leave_requests lr
            JOIN users u ON u.id=lr.user_id
            JOIN leave_types lt ON lt.id=lr.leave_type_id
            WHERE lr.status='pending'
        """).fetchall()

        for r in rows:
            st.write(r["name"], r["leave"], r["start_date"], r["end_date"])
            if st.button("Approve", key=f"a{r['id']}"):
                db.execute(
                    "UPDATE leave_requests SET status='approved', actioned_at=CURRENT_TIMESTAMP WHERE id=?",
                    (r["id"],)
                )
                db.commit()
                st.success("Approved")

    # REPORTS
    with tab4:
        data = pd.read_sql("SELECT * FROM leave_requests", db)
        st.dataframe(data)
