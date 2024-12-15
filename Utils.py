import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

API_KEY = "your_api_key_here"  # Replace with your actual API key

def fetch_comps(address):
    # Placeholder implementation.
    # Replace with a real API call, or use static data for testing.
    # Example: Using static data
    # return [
    #    {"address": "123 Elm St", "price": 200000, "square_footage": 1000, "price_per_sqft": 200, "status": "sold", "days_on_market": 50},
    #    {"address": "456 Oak St", "price": 250000, "square_footage": 1200, "price_per_sqft": 208, "status": "expired", "days_on_market": 120}
    # ]

    # For a real API call using Mashvisor (requires valid address & API_KEY):
    url = f"https://api.mashvisor.com/v1.1/client/property/{address}/comps"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        comps = response.json().get("content", {}).get("comps", [])
        processed_comps = []
        for comp in comps:
            sqft = comp.get("size", 0)
            price = comp.get("price", 0)
            price_per_sqft = round(price / sqft, 2) if sqft > 0 else 0
            processed_comps.append({
                "address": comp.get("address", "Unknown"),
                "price": price,
                "square_footage": sqft,
                "price_per_sqft": price_per_sqft,
                "status": comp.get("status", "unknown"),
                "days_on_market": comp.get("days_on_market", 0)
            })
        return processed_comps
    else:
        print(f"Error fetching comps: {response.status_code}")
        return []

def calculate_arv(comps, property_sqft):
    if not comps or property_sqft <= 0:
        return 0, 0
    avg_price_per_sqft = sum(c["price_per_sqft"] for c in comps if c["price_per_sqft"] > 0) / len([c for c in comps if c["price_per_sqft"] > 0])
    arv = avg_price_per_sqft * property_sqft
    return avg_price_per_sqft, arv

def estimate_profit(arv, acquisition_cost, repair_cost):
    return round(arv - (acquisition_cost + repair_cost), 2)

def generate_pdf_report(filename, comps, arv, repair_cost, acquisition_cost, profit):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(50, 750, "Real Estate Deal Report")
    c.drawString(50, 730, f"ARV: ${arv}")
    c.drawString(50, 710, f"Repair Cost: ${repair_cost}")
    c.drawString(50, 690, f"Acquisition Cost: ${acquisition_cost}")
    c.drawString(50, 670, f"Profit: ${profit}")
    y = 640
    c.drawString(50, y, "Comparable Properties:")
    y -= 20
    for comp in comps:
        c.drawString(50, y, f"{comp['address']}: ${comp['price']} - {comp['square_footage']} sq ft - {comp['status']} - {comp['days_on_market']} days")
        y -= 20
    c.save()
