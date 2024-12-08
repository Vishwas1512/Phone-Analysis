import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv(r'Data_CSV\agg_user.csv')

st.title("Brand-wise Transaction Analysis Dashboard")

st.subheader("Business Problem Statement")
st.write("This dashboard helps in analyzing brand-wise transaction trends for PhonePe services. "
         "The objective is to identify top-performing brands, examine market penetration, and "
         "extract actionable insights for brand promotion and strategic decision-making.")


st.sidebar.header("Filter Options")
brand_filter = st.sidebar.multiselect('Select Brand(s)', options=df['Brand'].unique(), default=df['Brand'].unique())
quarter_filter = st.sidebar.multiselect('Select Quarter(s)', options=df['Quarter'].unique(), default=df['Quarter'].unique())

df_filtered = df[(df['Brand'].isin(brand_filter)) & (df['Quarter'].isin(quarter_filter))]


st.header('Brand-wise Transaction Count and Market Share')
transaction_count_by_brand = df_filtered.groupby('Brand')['Transaction_count'].sum().reset_index()
transaction_percentage_by_brand = df_filtered.groupby('Brand')['Percentage'].mean().reset_index()

fig_transaction_count = px.bar(transaction_count_by_brand, x='Brand', y='Transaction_count', 
                               title='Total Transaction Count by Brand',
                               labels={'Transaction_count': 'Transaction Count'})
st.plotly_chart(fig_transaction_count)

fig_market_share = px.pie(transaction_percentage_by_brand, values='Percentage', names='Brand', 
                          title='Market Share by Brand (%)')
st.plotly_chart(fig_market_share)

st.header('Quarterly Transaction Trends')
transaction_trends = df_filtered.groupby(['Brand', 'Quarter'])['Transaction_count'].sum().reset_index()

fig_transaction_trends = px.bar(transaction_trends, x='Quarter', y='Transaction_count', color='Brand', 
                                 title='Quarterly Transaction Trends by Brand')
st.plotly_chart(fig_transaction_trends)

# Yearly Brand Performance (Year can be updated if you have multi-year data)
st.header('Yearly Brand Performance')

transaction_amount_and_year = df_filtered.groupby(['Brand', 'Year'])['Transaction_count'].sum().reset_index()

fig_yearly_performance = px.bar(transaction_amount_and_year, x='Brand', y='Transaction_count', color='Year', 
                                title="Yearly Brand Performance (Transaction Count)")
st.plotly_chart(fig_yearly_performance)

# Correlation Between Transaction Count and Market Share
st.header("Correlation Analysis: Transaction Count vs Market Share")

correlation_data = df_filtered[['Transaction_count', 'Percentage']].corr().iloc[0,1]
st.write(f"Correlation between Transaction Count and Market Share: {correlation_data:.2f}")

# Scatter plot for correlation visualization
fig_correlation = px.scatter(df_filtered, x='Transaction_count', y='Percentage', color='Brand', 
                             title='Correlation Between Transaction Count and Market Share')
st.plotly_chart(fig_correlation)

# Growth Rate Analysis
st.header('Growth Rate Analysis')
df_filtered['Growth_Rate'] = df_filtered.groupby('Brand')['Transaction_count'].pct_change() * 100
growth_rate_df = df_filtered[['Brand', 'Year', 'Quarter', 'Growth_Rate']].dropna()

fig_growth_rate = px.bar(growth_rate_df, x='Brand', y='Growth_Rate', color='Quarter', 
                         title='Brand-wise Quarterly Growth Rate (%)')
st.plotly_chart(fig_growth_rate)



# Summary Insights
st.header("Key Insights")
st.write(f"Total Transactions Analyzed: {df_filtered['Transaction_count'].sum()}")
top_brand = df_filtered.groupby('Brand')['Transaction_count'].sum().idxmax()
st.write(f"Top Brand by Transaction Count: {top_brand}")
st.write(f"Top Brand Market Share: {transaction_percentage_by_brand[transaction_percentage_by_brand['Brand'] == top_brand]['Percentage'].values[0]:.2%}")

# Footer
st.write("This expanded analysis provides deeper insights into the brand-wise performance of PhonePe transactions, "
         "offering actionable insights on market dynamics, growth, and correlation trends. "
         "PhonePe can leverage these findings to refine their marketing strategies and focus on key brands or emerging markets.")



# 