import streamlit as st
import pandas as pd
import duckdb
import os

st.title('Electricity Production')

# database connection
con = duckdb.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data.db'))
df = con.execute("SELECT * FROM analytics.fact_electricity_production").df()
df_countries = con.execute("SELECT * FROM analytics.dim_country").df()

df = df.merge(df_countries, left_on="country", right_on="name", how="left")
df["production_month"] = pd.to_datetime(df["production_month"])
df_monthly = df.groupby(["country", "production_month"])["production_gwh"].sum().reset_index()

# filters
with st.sidebar:
    st.header("Filters")
    min_date = df["production_month"].min()
    max_date = df["production_month"].max()
    selected_date_range = st.date_input("Select Date Range:", value=(min_date, max_date))
    
    country_list = sorted(df["country"].unique())
    selected_countries = st.multiselect("Select Countries:", country_list, default=[])
    split_by_country = st.checkbox("Split by Country", value=True)

if selected_countries:
    st.subheader("Electricity Production Trend by Country")
else:
    st.subheader("Electricity Production Trend Worldwide")

if not selected_countries:
    selected_countries = country_list

if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
    df_monthly = df_monthly[(df_monthly["country"].isin(selected_countries)) & 
                            (df_monthly["production_month"] >= pd.to_datetime(start_date)) & 
                            (df_monthly["production_month"] <= pd.to_datetime(end_date))]

if not split_by_country:
    df_filtered = df_monthly.groupby("production_month")["production_gwh"].sum().reset_index()
else:
    df_filtered = df_monthly

# Trend chart
if split_by_country:
    st.line_chart(df_filtered, x="production_month", y="production_gwh", color="country", 
                  x_label="Month", y_label="Production (GWh)")
else:
    st.line_chart(df_filtered, x="production_month", y="production_gwh", 
                  x_label="Month", y_label="Production (GWh)")


# Production by region
if split_by_country:
    df_regions = df[(df["country"].isin(selected_countries)) & 
                    (df["production_month"] >= pd.to_datetime(start_date)) & 
                    (df["production_month"] <= pd.to_datetime(end_date))].groupby(["region", "country"])["production_gwh"].sum().reset_index()
    df_regions = df_regions.sort_values(by="production_gwh", ascending=False)
    st.subheader("Electricity Production by Region and Country")
    st.bar_chart(df_regions, x="region", y="production_gwh", color="country", 
                 x_label="Region", y_label="Production (GWh)")
else:
    df_regions = df[(df["country"].isin(selected_countries)) & 
                    (df["production_month"] >= pd.to_datetime(start_date)) & 
                    (df["production_month"] <= pd.to_datetime(end_date))].groupby("region")["production_gwh"].sum().reset_index()
    df_regions = df_regions.sort_values(by="production_gwh", ascending=False)
    st.subheader("Electricity Production by Region")
    st.bar_chart(df_regions, x="region", y="production_gwh", 
                 x_label="Region", y_label="Production (GWh)")

# Average production by country
st.subheader("Average Yearly Electricity Production by Country")
df_countries_filtered = df[(df["country"].isin(selected_countries)) & 
                           (df["production_month"] >= pd.to_datetime(start_date)) & 
                           (df["production_month"] <= pd.to_datetime(end_date))].groupby("country")["production_gwh"].mean().reset_index().sort_values(by="production_gwh", ascending=False)
st.bar_chart(df_countries_filtered, y="production_gwh", x="country", y_label="Average Yearly Production (GWh)", x_label="Country")