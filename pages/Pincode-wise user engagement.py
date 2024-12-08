import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("top_user_pin.csv")

# Business Problem Statement and Objectives
st.title("User Engagement and Analysis Dashboard")
st.markdown("""
### Business Problem Statement:
The key challenge is identifying districts with high user registrations but low app engagement, allowing targeted strategies to boost app usage. Understanding the correlation between registered users and app opens is crucial for improving marketing campaigns and user experience.

""")

# Sidebar filters
st.sidebar.header("Filter Options")
state_filter = st.sidebar.multiselect('Select State(s)', options=df['State'].unique(), default=df['State'].unique())
Pincode_filter = st.sidebar.multiselect('Select Pincode(s)', options=df['Pincode'].unique(), default=df['Pincode'].unique())
year_filter = st.sidebar.multiselect('Select Year(s)', options=df['Year'].unique(), default=df['Year'].unique())

# Apply filters
df_filtered = df[(df['State'].isin(state_filter)) & (df['Pincode'].isin(Pincode_filter)) & (df['Year'].isin(year_filter))]

# Registered Users and App Opens Over Time
st.subheader("User Growth and App Opens Analysis")

# Group by year and quarter for trend analysis
user_trends = df_filtered.groupby(['Year', 'Quarter']).agg(
    total_registered_users=('Registered_users', 'sum')
).reset_index()

# Line plot for Registered Users and App Opens
fig_trends = px.line(user_trends, x='Quarter', y='total_registered_users', color='Year',
                     title="Registered Users Over Time")
st.plotly_chart(fig_trends)


# User Distribution Across Pincodes
st.subheader("User Distribution Across Pincodes")
district_user_distribution = df_filtered.groupby('Pincode').agg(
    total_registered_users=('Registered_users', 'sum')
).reset_index()


# Pivot Table Analysis
st.subheader("Pivot Table Analysis")
pivot_table = df_filtered.pivot_table(values='Registered_users', index='Pincode', columns='Year', aggfunc='sum')
st.write("Pivot Table: Registered Users by Pincode and Year")
st.dataframe(pivot_table)

# Heatmap of Registered Users by Pincode and Year
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Heatmap of Registered Users by Pincode and Year")
st.pyplot(fig)

# Pincode-Level Quarterly Growth Rate
st.subheader("Pincode-Level Quarterly Growth Rate")
df_filtered['Growth_Rate'] = df_filtered.groupby('Pincode')['Registered_users'].pct_change() * 100
growth_rate_df = df_filtered[['Pincode', 'Year', 'Quarter', 'Growth_Rate']].dropna()


# Footer
st.write("This dashboard provides actionable insights into pincode-wise user engagement trends, helping stakeholders optimize strategies for increasing user registrations.")
