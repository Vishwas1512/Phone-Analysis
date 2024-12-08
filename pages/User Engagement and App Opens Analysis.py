import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv(r"Data_CSV\map_user.csv")

# Business Problem Statement and Objectives
st.title("User Engagement and App Opens Analysis Dashboard")
st.markdown("""
### Business Problem Statement:
The key challenge is identifying districts with high user registrations but low app engagement, allowing targeted strategies to boost app usage. Understanding the correlation between registered users and app opens is crucial for improving marketing campaigns and user experience.

""")

# Sidebar filters
st.sidebar.header("Filter Options")
state_filter = st.sidebar.multiselect('Select State(s)', options=df['State'].unique(), default=df['State'].unique())
district_filter = st.sidebar.multiselect('Select District(s)', options=df['District'].unique(), default=df['District'].unique())
year_filter = st.sidebar.multiselect('Select Year(s)', options=df['Year'].unique(), default=df['Year'].unique())

# Apply filters
df_filtered = df[(df['State'].isin(state_filter)) & (df['District'].isin(district_filter)) & (df['Year'].isin(year_filter))]

# Registered Users and App Opens Over Time
st.subheader("User Growth and App Opens Analysis")

# Group by year and quarter for trend analysis
user_trends = df_filtered.groupby(['Year', 'Quarter']).agg(
    total_registered_users=('Registered_users', 'sum'),
    total_app_opens=('App_opens', 'sum')
).reset_index()

# Line plot for Registered Users and App Opens
fig_trends = px.line(user_trends, x='Quarter', y='total_registered_users', color='Year',
                     title="Registered Users Over Time")
st.plotly_chart(fig_trends)

# App opens trend
fig_app_opens_trend = px.line(user_trends, x='Quarter', y='total_app_opens', color='Year',
                              title="App Opens Over Time")
st.plotly_chart(fig_app_opens_trend)

# User Distribution Across Districts
st.subheader("User Distribution Across Districts")
district_user_distribution = df_filtered.groupby('District').agg(
    total_registered_users=('Registered_users', 'sum')
).reset_index()

# Bar chart for district-wise registered users
fig_district_users = px.bar(district_user_distribution, x='District', y='total_registered_users',
                            title="District-Wise Registered Users",
                            labels={'total_registered_users': 'Registered Users'})
st.plotly_chart(fig_district_users)

# Correlation Between Registered Users and App Opens
st.subheader("Correlation Between Registered Users and App Opens")
correlation = df_filtered[['Registered_users', 'App_opens']].corr().iloc[0, 1]
st.write(f"Correlation between Registered Users and App Opens: {correlation:.2f}")

# Scatter plot for correlation
fig_correlation = px.scatter(df_filtered, x='Registered_users', y='App_opens', color='District',
                             title="Correlation Between Registered Users and App Opens")
st.plotly_chart(fig_correlation)

# Pivot Table Analysis
st.subheader("Pivot Table Analysis")
pivot_table = df_filtered.pivot_table(values='Registered_users', index='District', columns='Year', aggfunc='sum')
st.write("Pivot Table: Registered Users by District and Year")
st.dataframe(pivot_table)

# Heatmap of Registered Users by District and Year
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".0f")
plt.title("Heatmap of Registered Users by District and Year")
st.pyplot(fig)

# District-Level Quarterly Growth Rate
st.subheader("District-Level Quarterly Growth Rate")
df_filtered['Growth_Rate'] = df_filtered.groupby('District')['Registered_users'].pct_change() * 100
growth_rate_df = df_filtered[['District', 'Year', 'Quarter', 'Growth_Rate']].dropna()

# Bar chart for growth rate
fig_growth_rate = px.bar(growth_rate_df, x='District', y='Growth_Rate', color='Quarter',
                         title='District-Wise Quarterly Growth Rate (%)')
st.plotly_chart(fig_growth_rate)



# Footer
st.write("This dashboard provides actionable insights into district-wise user engagement trends, helping stakeholders optimize strategies for increasing user registrations and app opens.")
