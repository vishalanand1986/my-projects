import streamlit as st
import pandas as pd
from datetime import date

# -------------------------------
# Session state for storing properties
# -------------------------------
if "properties" not in st.session_state:
    st.session_state.properties = []

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Nomad Stay Finder", page_icon="🌍")
st.title("🌍 Nomad Stay Finder")
st.caption("Find affordable, reliable long-stay accommodations for remote workers")

# -------------------------------
# Section: Add new property
# -------------------------------
st.sidebar.header("➕ Add New Stay")

with st.sidebar.form("add_property"):
    location = st.text_input("Location (City, Country)")
    price = st.number_input("Price per month ($)", min_value=100, max_value=5000, value=500, step=50)
    wifi_speed = st.text_input("Wi-Fi Speed (e.g., 100 Mbps)")
    safety_rating = st.selectbox("Safety Rating", ["Low", "Medium", "High"])
    workspace = st.checkbox("Workspace Available?")
    submit = st.form_submit_button("Add Stay")

    if submit:
        stay_id = len(st.session_state.properties) + 1
        auto_name = f"Stay #{stay_id} in {location}"
        new_property = {
            "Name": auto_name,
            "Location": location,
            "Price_per_month": price,
            "Wifi_speed": wifi_speed,
            "Safety_rating": safety_rating,
            "Workspace": workspace
        }
        st.session_state.properties.append(new_property)
        st.success(f"✅ Added: {auto_name}")

# -------------------------------
# Section: Filters
# -------------------------------
st.sidebar.header("🔎 Filters")
max_price = st.sidebar.slider("Max monthly price ($)", 200, 3000, 1000)
wifi_required = st.sidebar.text_input("Minimum Wi-Fi (e.g., 100 Mbps)")
safety_required = st.sidebar.selectbox("Minimum Safety Rating", ["Any", "Medium", "High"])
workspace_required = st.sidebar.checkbox("Must have workspace")

# Date selection for intended booking
st.sidebar.header("📅 Select Stay Dates")
date_range = st.sidebar.date_input(
    "Choose check-in and check-out",
    value=(date.today(), date.today()),
)

# Convert to DataFrame for filtering
df = pd.DataFrame(st.session_state.properties)

# -------------------------------
# Apply filters
# -------------------------------
if not df.empty:
    filtered = df[df["Price_per_month"] <= max_price]

    if wifi_required:
        try:
            required_speed = int(wifi_required.split()[0])
            filtered = filtered[filtered["Wifi_speed"].str.extract(r"(\d+)").astype(float)[0] >= required_speed]
        except:
            st.warning("⚠️ Please enter Wi-Fi as a number followed by Mbps (e.g., 100 Mbps).")

    if safety_required != "Any":
        filtered = filtered[filtered["Safety_rating"] == safety_required]

    if workspace_required:
        filtered = filtered[filtered["Workspace"] == True]
else:
    filtered = pd.DataFrame()

# -------------------------------
# Section: Display results
# -------------------------------
st.subheader("🏠 Available Stays")

if not filtered.empty:
    for _, row in filtered.iterrows():
        with st.container(border=True):
            st.write(f"**{row['Name']}**")
            st.write(f"📍 Location: {row['Location']}")
            st.write(f"💵 Price per month: ${row['Price_per_month']}")
            st.write(f"📶 Wi-Fi: {row['Wifi_speed']}")
            st.write(f"🛡️ Safety: {row['Safety_rating']}")
            st.write("💻 Workspace available" if row["Workspace"] else "❌ No dedicated workspace")

            # Mock booking flow
            if st.button(f"Book {row['Name']}", key=row['Name']):
                if isinstance(date_range, tuple) and len(date_range) == 2:
                    check_in, check_out = date_range
                    st.success(
                        f"✅ Booking request submitted for {row['Name']}!\n\n"
                        f"📍 {row['Location']}\n"
                        f"📅 From {check_in} to {check_out}\n"
                        f"💵 Monthly Rate: ${row['Price_per_month']}"
                    )
                else:
                    st.warning("⚠️ Please select both check-in and check-out dates before booking.")
else:
    st.info("No stays available. Add a property or adjust filters.")
