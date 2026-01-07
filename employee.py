import streamlit as st
from db import get_db
from datetime import date

def employee_dashboard(user):
    st.title("Employee Dashboard")
    db = get_db()

    st.subheader("Leave Balance")
    rows = db.execute("""
        SELECT lt.name,b.balance
        FROM leave_balances b
        JOIN leave_types lt ON lt.id=b.leave_type_id
        WHERE b.user_id=?
    """, (user["id"],)).fetchall()

    for r in rows:
        st.write(r["name"], r["balance"])

    st.subheader("Apply Leave")
    types = db.execute("SELECT * FROM leave_types").fetchall()
    lt = st.selectbox("Leave Type", [t["name"] for t in types])
    start = st.date_input("Start")
    end = st.date_input("End")
    reason = st.text_area("Reason")

    days = (end - start).days + 1

    if st.button("Apply"):
        tid = [t["id"] for t in types if t["name"] == lt][0]
        db.execute("""
            INSERT INTO leave_requests
            (user_id,leave_type_id,start_date,end_date,days,reason,status)
            VALUES (?,?,?,?,?,?, 'pending')
        """, (user["id"], tid, start, end, days, reason))
        db.commit()
        st.success("Applied")

    st.subheader("History")
    hist = db.execute("""
        SELECT lr.*, lt.name
        FROM leave_requests lr
        JOIN leave_types lt ON lt.id=lr.leave_type_id
        WHERE user_id=?
    """, (user["id"],)).fetchall()

    for h in hist:
        st.write(h["name"], h["start_date"], h["status"])
