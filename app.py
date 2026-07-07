import streamlit as st
import pandas as pd

# Page Title
st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")

st.title("Customer Engagement & Product Utilization Analytics")
st.subheader("Customer Retention Strategy Dashboard")

st.write(
    "This dashboard analyzes customer engagement and product utilization to identify customer retention opportunities. Use the filters on the left to explore customer data."
)

# Load Data
df = pd.read_csv("European_Bank.csv")

# Sidebar Filters
st.sidebar.header("Filters")

active_filter = st.sidebar.selectbox(
    "Customer Activity",
    ["All", "Active", "Inactive"]
)

product_filter = st.sidebar.slider(
    "Number of Products",
    int(df["NumOfProducts"].min()),
    int(df["NumOfProducts"].max()),
    (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()))
)

# Apply Filters
filtered_df = df.copy()

if active_filter == "Active":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]

elif active_filter == "Inactive":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

filtered_df = filtered_df[
    (filtered_df["NumOfProducts"] >= product_filter[0]) &
    (filtered_df["NumOfProducts"] <= product_filter[1])
]

# KPI Section
st.header("KPI Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Total Customers",
    len(filtered_df)
)

col2.metric(
    "Churn Rate (%)",
    round(filtered_df["Exited"].mean()*100, 2)
)

col3.metric(
    "Average Balance",
    f"{filtered_df['Balance'].mean():,.0f}"
)

col4.metric(
    "Average Credit Score",
    round(filtered_df["CreditScore"].mean(), 0)
)

# Geography Analysis
st.header("Geography-wise Churn")

geo_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    * 100
)

st.bar_chart(geo_churn)
# Product Utilization
st.header("Product Utilization Analysis")

product_churn = (
    filtered_df.groupby("NumOfProducts")["Exited"]
    .mean()
    * 100
)

st.bar_chart(product_churn)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Filtered_Customers.csv",
    mime="text/csv"
)
# Customer Data
st.header("Customer Records")

st.dataframe(filtered_df)
st.markdown("---")

st.caption(
    "Customer Retention Dashboard | MBA Internship Project | Built using Python, Pandas and Streamlit"
)