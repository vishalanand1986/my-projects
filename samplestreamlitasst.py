import streamlit as st
import pandas as pd

# -------------------------------
# Session state for storing user-added properties
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
st.sidebar.header("➕ Add New Property")

with st.sidebar.form("add_property"):
    name = st.text_input("Property Name")
    location = st.text_input("Location (City, Country)")
    price = st.number_input("Price per month ($)", min_value=100, max_value=5000, value=500, step=50)
    wifi_speed = st.text_input("Wi-Fi Speed (e.g., 100 Mbps)")
    safety_rating = st.selectbox("Safety Rating", ["Low", "Medium", "High"])
    workspace = st.checkbox("Workspace Available?")
    submit = st.form_submit_button("Add Property")

    if submit:
        new_property = {
            "Name": name,
            "Location": location,
            "Price_per_month": price,
            "Wifi_speed": wifi_speed,
            "Safety_rating": safety_rating,
            "Workspace": workspace
        }
        st.session_state.properties.append(new_property)
        st.success(f"✅ {name} added!")

# -------------------------------
# Section: Filters
# -------------------------------
st.sidebar.header("🔎 Filters")
max_price = st.sidebar.slider("Max monthly price ($)", 200, 3000, 1000)
wifi_required = st.sidebar.text_input("Minimum Wi-Fi (e.g., 100 Mbps)")
safety_required = st.sidebar.selectbox("Minimum Safety Rating", ["Any", "Medium", "High"])
workspace_required = st.sidebar.checkbox("Must have workspace")

# Convert to DataFrame for filtering
df = pd.DataFrame(st.session_state.properties)

# -------------------------------
# Apply filters
# -------------------------------
if not df.empty:
    filtered = df[df["Price_per_month"] <= max_price]

    if wifi_required:
        # crude check: keep properties with equal or higher Mbps number
        required_speed = int(wifi_required.split()[0])
        filtered = filtered[filtered["Wifi_speed"].str.extract(r"(\d+)").astype(float)[0] >= required_speed]

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
            st.write(f"**{row['Name']}** — {row['Location']}")
            st.write(f"💵 Price per month: ${row['Price_per_month']}")
            st.write(f"📶 Wi-Fi: {row['Wifi_speed']}")
            st.write(f"🛡️ Safety: {row['Safety_rating']}")
            st.write("💻 Workspace available" if row["Workspace"] else "❌ No dedicated workspace")

            # Mock booking flow
            if st.button(f"Book {row['Name']}", key=row['Name']):
                st.success(f"✅ Booking request submitted for {row['Name']} (Demo Mode)")
else:
    st.info("No stays available. Add a property or adjust filters.")
