import streamlit as st
import json
from datetime import datetime

LEADS_FILE = "realtors.json"

def load_realtors():
    try:
        with open(LEADS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_realtors(realtors):
    with open(LEADS_FILE, "w") as file:
        json.dump(realtors, file, indent=4)

def add_realtor(name, phone, follow_up_date):
    realtors = load_realtors()
    realtors.append({
        "name": name,
        "phone": phone,
        "follow_up_date": follow_up_date,
        "status": "Pending",
        "properties": []
    })
    save_realtors(realtors)

def view_realtors():
    realtors = load_realtors()
    if not realtors:
        st.write("No realtors found.")
        return
    st.write("Current Realtor Contacts:")
    for i, r in enumerate(realtors, start=1):
        st.write(f"{i}. {r['name']} | {r['phone']} | Follow-up: {r['follow_up_date']} | Status: {r['status']}")
        if r.get("properties"):
            st.write("   Properties:")
            for p_i, p in enumerate(r["properties"], start=1):
                notes_str = f" - Notes: {p['notes']}" if p.get('notes') else ""
                st.write(f"     {p_i}. {p['address']}{notes_str}")
        else:
            st.write("   No properties associated yet.")

def follow_up_alerts():
    realtors = load_realtors()
    today = datetime.now().strftime("%Y-%m-%d")
    alerts = [r for r in realtors if r["follow_up_date"] <= today and r["status"] == "Pending"]

    if alerts:
        st.write("Realtors to Follow Up Today or Overdue:")
        for r in alerts:
            st.write(f"{r['name']} | {r['phone']} | Follow-up Date: {r['follow_up_date']}")
    else:
        st.write("No follow-ups needed today.")

def update_realtor_status(index, status):
    realtors = load_realtors()
    if 0 <= index < len(realtors):
        realtors[index]["status"] = status
        save_realtors(realtors)
        st.success("Realtor status updated successfully!")
    else:
        st.error("Invalid realtor index.")

def add_property_to_realtor(index, address, notes=None):
    realtors = load_realtors()
    if 0 <= index < len(realtors):
        property_entry = {"address": address}
        if notes:
            property_entry["notes"] = notes
        realtors[index]["properties"].append(property_entry)
        save_realtors(realtors)
        st.success("Property added successfully!")
    else:
        st.error("Invalid realtor index.")

# Streamlit Interface
st.title("Realtor Contact & Property Tracker")

# Add a New Realtor
st.header("Add a New Realtor Contact")
name = st.text_input("Realtor Name")
phone = st.text_input("Phone Number")
follow_up_date = st.date_input("Follow-up Date")
if st.button("Add Realtor"):
    if name and phone and follow_up_date:
        add_realtor(name, phone, follow_up_date.strftime("%Y-%m-%d"))
        st.success("Realtor added successfully!")
    else:
        st.error("Please fill out all fields.")

st.header("View Existing Realtors")
view_realtors()

st.header("Follow-Up Alerts")
follow_up_alerts()

# Update Realtor Status
st.header("Update Realtor Status")
index_to_update = st.number_input("Enter Realtor Number to Update Status", min_value=1, step=1)
new_status = st.text_input("Enter New Status (e.g., Completed, Pending)")
if st.button("Update Status"):
    update_realtor_status(index_to_update - 1, new_status)

# Add Property to an Existing Realtor
st.header("Add Property to a Realtor")
property_realtor_index = st.number_input("Enter Realtor Number to Add Property", min_value=1, step=1)
property_address = st.text_input("Property Address")
property_notes = st.text_input("Property Notes (optional)")
if st.button("Add Property"):
    if property_address:
        add_property_to_realtor(property_realtor_index - 1, property_address, property_notes)
    else:
        st.error("Please enter a property address.")
