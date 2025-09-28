import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE_NAME = "family_expenses.xlsx"

# Initialize or load data
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME, sheet_name="Expense Log")
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Sub-category", "Amount", "Paid By", "Notes"])
        df.to_excel(FILE_NAME, sheet_name="Expense Log", index=False)
        return df

def save_data(df):
    with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Expense Log", index=False)

st.title("💰 Family Monthly Expense Tracker")

# Load existing expenses
df = load_data()

# Expense input form
with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Groceries", "Other"])
    sub_category = st.text_input("Sub-category")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    paid_by = st.selectbox("Paid By", ["Dad", "Mom", "Son", "Daughter"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_row = pd.DataFrame([[date, category, sub_category, amount, paid_by, notes]],
                           columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    st.success("✅ Expense added!")

st.subheader("📜 All Expenses")
st.dataframe(df)

# Generate monthly report
if st.button("📊 Generate Monthly Report"):
    month = datetime.today().month
    year = datetime.today().year
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_df = df[(df["Date"].dt.month == month) & (df["Date"].dt.year == year)]
    
    if monthly_df.empty:
        st.warning("No expenses logged this month!")
    else:
        summary = monthly_df.groupby("Category")["Amount"].sum().reset_index()
        st.write("### Monthly Summary")
        st.dataframe(summary)

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(summary["Amount"], labels=summary["Category"], autopct='%1.1f%%')
        ax.set_title(f"Expense Breakdown - {month}/{year}")
        st.pyplot(fig)

        # Save report
        report_file = f"Expense_Report_{year}_{month}.xlsx"
        with pd.ExcelWriter(report_file, engine="openpyxl") as writer:
            monthly_df.to_excel(writer, sheet_name="This Month Expenses", index=False)
            summary.to_excel(writer, sheet_name="Summary", index=False)
        st.success(f"📂 Report saved as {report_file}")
        with open(report_file, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name=report_file)