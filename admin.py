import streamlit as st
from db import get_db


def admin_dashboard():
    st.title("Admin Dashboard")

    db = get_db()
    cur = db.cursor()

    st.subheader("Pending Leave Requests")

    cur.execute("""
        SELECT 
            lr.id,
            u.name,
            lt.name AS leave_type,
            lr.start_date,
            lr.end_date,
            lr.days
        FROM leave_requests lr
        JOIN users u ON u.id = lr.user_id
        JOIN leave_types lt ON lt.id = lr.leave_type_id
        WHERE lr.status = 'pending'
        ORDER BY lr.start_date DESC
    """)

    rows = cur.fetchall()

    if not rows:
        st.info("No pending leave requests")
        return

    for r in rows:
        with st.container(border=True):
            st.write(f"👤 **Employee:** {r['name']}")
            st.write(f"📄 **Leave Type:** {r['leave_type']}")
            st.write(f"📅 **From:** {r['start_date']} → {r['end_date']}")
            st.write(f"🧮 **Days:** {r['days']}")

            col1, col2 = st.columns(2)

            if col1.button("Approve", key=f"approve_{r['id']}"):
                cur.execute(
                    "UPDATE leave_requests SET status='approved' WHERE id=?",
                    (r["id"],)
                )
                db.commit()
                st.success("Approved")
                st.rerun()

            if col2.button("Reject", key=f"reject_{r['id']}"):
                cur.execute(
                    "UPDATE leave_requests SET status='rejected' WHERE id=?",
                    (r["id"],)
                )
                db.commit()
                st.warning("Rejected")
                st.rerun()
