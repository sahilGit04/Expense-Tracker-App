import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="Expense Tracker Pro", layout="wide")

DATA_PATH = "expenses.csv"

# -----------------------------
# Initialize File
# -----------------------------
if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Payment"])
    df.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

# -----------------------------
# Title
# -----------------------------
st.title("💰 Expense Tracker Pro Dashboard")

# -----------------------------
# Sidebar - Add Expense
# -----------------------------
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Rent", "Shopping", "Entertainment", "Bills"]
)
amount = st.sidebar.number_input("Amount", min_value=0)
payment = st.sidebar.selectbox("Payment", ["Cash", "Card", "UPI"])

if st.sidebar.button("Add Expense"):
    new_data = pd.DataFrame([[date, category, amount, payment]],
                            columns=["Date", "Category", "Amount", "Payment"])
    new_data.to_csv(DATA_PATH, mode='a', header=False, index=False)
    st.sidebar.success("Added!")
    st.rerun()

# Reload
df = pd.read_csv(DATA_PATH)

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

    categories = st.sidebar.multiselect(
        "Category Filter",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    df = df[
        (df["Category"].isin(categories)) &
        (df["Date"] >= pd.to_datetime(date_range[0])) &
        (df["Date"] <= pd.to_datetime(date_range[1]))
    ]

# -----------------------------
# Metrics
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total = df["Amount"].sum()
avg = df["Amount"].mean() if not df.empty else 0
count = len(df)

col1.metric("Total Spending", f"₹{total}")
col2.metric("Average Expense", f"₹{round(avg,2)}")
col3.metric("Transactions", count)

# -----------------------------
# Budget Alert
# -----------------------------
BUDGET = 50000

if total > BUDGET:
    st.error("⚠ Budget Exceeded")
else:
    st.success("Budget Under Control")

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📋 Expense Data")
st.dataframe(df, use_container_width=True)

# -----------------------------
# Charts Section
# -----------------------------
if not df.empty:

    col1, col2 = st.columns(2)

    # Category Bar Chart
    with col1:
        st.subheader("Category Spending")
        cat = df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        cat.plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount")
        st.pyplot(fig)

    # Pie Chart
    with col2:
        st.subheader("Spending Distribution")
        fig2, ax2 = plt.subplots()
        cat.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        st.pyplot(fig2)

# -----------------------------
# Monthly Trend
# -----------------------------
if not df.empty:
    st.subheader("📈 Monthly Trend")

    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()

    fig3, ax3 = plt.subplots()
    monthly.plot(kind="line", marker="o", ax=ax3)
    st.pyplot(fig3)

# -----------------------------
# Insights
# -----------------------------
if not df.empty:
    st.subheader("🧠 Insights")

    top_cat = df.groupby("Category")["Amount"].sum().idxmax()
    max_day = df.groupby("Date")["Amount"].sum().idxmax()

    st.write(f"💸 Highest spending category: **{top_cat}**")
    st.write(f"📅 Highest spending day: **{max_day}**")

# -----------------------------
# Download CSV
# -----------------------------
st.subheader("⬇ Download Data")

st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="expenses_export.csv",
    mime="text/csv"
)

# -----------------------------
# Reset Data
# -----------------------------
if st.button("⚠ Reset All Data"):
    os.remove(DATA_PATH)
    st.warning("Data Reset! Refresh app.")