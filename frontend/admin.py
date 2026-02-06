import streamlit as st
from datetime import datetime
import sys
import os
import pandas as pd

# ----------------------------
# Config
# ----------------------------
ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")  # fallback for demo

# ----------------------------
# Import backend
# ----------------------------
BACKEND_PATH = os.path.abspath("../backend")
sys.path.insert(0, BACKEND_PATH)

from storage import get_all_leads, delete_lead, export_leads_as_dict

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Clinic Admin Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------
# Auth state
# ----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------
# LOGIN SCREEN
# ----------------------------
if not st.session_state.authenticated:
    st.title("🔐 Admin Login")

    pin = st.text_input(
        "Enter Admin PIN",
        type="password"
    )

    if st.button("Login"):
        if pin == ADMIN_PIN:
            st.session_state.authenticated = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid PIN")

    st.stop()  # ⛔ Block rest of app

# ----------------------------
# DASHBOARD (Authenticated)
# ----------------------------
st.title("🏥 Clinic Admin Dashboard")

# Logout
if st.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

st.divider()

# ----------------------------
# Export Leads
# ----------------------------
st.subheader("📤 Export Leads")

export_data = export_leads_as_dict()
if export_data:
    df = pd.DataFrame(export_data)
    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name="clinic_leads.csv",
        mime="text/csv"
    )
else:
    st.info("No leads available.")

st.divider()

# ----------------------------
# Refresh
# ----------------------------
if st.button("🔄 Refresh Leads"):
    st.rerun()

# ----------------------------
# Show Leads
# ----------------------------
st.subheader("📋 All Leads")

leads = get_all_leads()

if not leads:
    st.info("No leads yet.")
else:
    for lead in leads:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(
                    f"""
                    **Service:** {lead.service}  
                    **Date:** {lead.date}  
                    **Phone:** {lead.phone}  
                    **Received:** {lead.created_at.strftime("%Y-%m-%d %H:%M")}
                    """
                )

            with col2:
                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{lead.id}"
                ):
                    delete_lead(lead.id)
                    st.success("Lead deleted")
                    st.rerun()

# ----------------------------
# Stats
# ----------------------------
st.divider()
st.subheader("📊 Quick Stats")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Leads", len(leads))

with col2:
    today_count = sum(
        1 for lead in leads
        if lead.created_at.date() == datetime.today().date()
    )
    st.metric("Leads Today", today_count)
