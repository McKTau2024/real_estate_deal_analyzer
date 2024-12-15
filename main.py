import streamlit as st
from utils import generate_pdf_report

st.title("Real Estate Deal Analyzer")

# Step 1: Property Details
property_sqft = st.number_input("Property Square Footage", min_value=0)

# User directly inputs estimated price per sqft
estimated_price_per_sqft = st.number_input("Estimated Price per Sq Ft", min_value=0.0)
arv = estimated_price_per_sqft * property_sqft

st.write(f"Estimated ARV: ${arv:.2f}")

# Repair Costs
repair_cost = st.number_input("Repair Cost ($)", min_value=0)

# Acquisition Cost
acquisition_cost = st.number_input("Acquisition Cost ($)", min_value=0)

profit = arv - (acquisition_cost + repair_cost)
st.write(f"Estimated Profit: ${profit:.2f}")

# Generate PDF (if still desired)
if st.button("Generate PDF Report"):
    generate_pdf_report("Real_Estate_Report.pdf", [], arv, repair_cost, acquisition_cost, profit)
    st.success("PDF Report Generated!")
