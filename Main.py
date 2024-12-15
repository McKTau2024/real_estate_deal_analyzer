import streamlit as st
import pandas as pd
from utils import fetch_comps, calculate_arv, estimate_profit, generate_pdf_report

comps = []

st.title("Real Estate Deal Analyzer")

# Step 1: Property Details
st.header("Step 1: Enter Property Details")
property_address = st.text_input("Property Address")
property_sqft = st.number_input("Square Footage (Sq Ft)", min_value=0)

if st.button("Fetch Comparable Properties"):
    comps = fetch_comps(property_address)
    if comps:
        st.success("Comps fetched successfully!")
    else:
        st.warning("No comps found or failed to fetch comps.")

if comps:
    st.header("Comparable Properties")
    df = pd.DataFrame(comps)
    st.table(df)

    # Show expired listings
    expired_listings = [c for c in comps if c.get("status", "").lower() == "expired"]
    if expired_listings:
        st.subheader("Expired Listings")
        edf = pd.DataFrame(expired_listings)
        st.table(edf)

    # Show listings over 100 days on market
    long_listings = [c for c in comps if c.get("days_on_market", 0) > 100]
    if long_listings:
        st.subheader("Listings Over 100 Days on Market")
        ldf = pd.DataFrame(long_listings)
        st.table(ldf)

    # Calculate ARV
    avg_price_per_sqft, arv = calculate_arv(comps, property_sqft)
    st.write(f"**Average Price per Sq Ft:** ${avg_price_per_sqft:.2f}")
    st.write(f"**Estimated ARV:** ${arv:.2f}")

    # Step 2: Repair Cost Estimation
    st.header("Step 2: Estimate Repair Costs")
    repair_cost_per_sqft = st.number_input("Repair Cost per Sq Ft ($)", min_value=0, value=30)
    repair_cost = repair_cost_per_sqft * property_sqft
    st.write(f"**Estimated Total Repair Cost:** ${repair_cost:.2f}")

    # Step 3: Profit Estimation
    st.header("Step 3: Estimate Profit")
    acquisition_cost = st.number_input("Acquisition Cost ($)", min_value=0)
    profit = estimate_profit(arv, acquisition_cost, repair_cost)
    st.write(f"**Estimated Profit:** ${profit:.2f}")

    # Report generation
    if st.button("Generate PDF Report"):
        generate_pdf_report("Real_Estate_Report.pdf", comps, arv, repair_cost, acquisition_cost, profit)
        st.success("PDF Report Generated!")
