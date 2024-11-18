# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display():
    sns.set(style="whitegrid")

    # Load data function with caching
    @st.cache_data
    def load_data(file_path):
        df = pd.read_excel(file_path)
        df['dt'] = pd.to_datetime(df['dt'])
        df['month'] = df['dt'].dt.to_period('M')
        df['week'] = df['dt'].dt.to_period('W')
        df['day'] = df['dt'].dt.date
        return df

    # File path
    file_path = 'data/Wise funnel events regional - Data.xlsx'

    # Load the dataset
    df = load_data(file_path)

    # Streamlit layout starts here
    st.title("Relative Analysis")
    st.write("This section focuses on comparing different regions and platforms to gain insights into the performance and behavior of users in terms of transfers. ")

    # Heading 14: Relative Metrics
    st.header("12. Relative Metrics")

    # (a) Transfer Created vs. Transfer Transferred Ratios by Region
    st.subheader("12.1 Transfer Created vs. Transfer Transferred Ratios by Region")
    st.write("""
    This pie chart compares the percentage of users who created transfers to those who completed transfers (transferred) in each region. The data shows the relative ratio, providing insight into the completion rate for each region.
    """)

    transfer_created = df[df['event_name'] == 'Transfer Created'].groupby('region')['user_id'].count()
    transfer_transferred = df[df['event_name'] == 'Transfer Transferred'].groupby('region')['user_id'].count()
    relative_ratios = (transfer_transferred / transfer_created * 100).fillna(0)

    regions = relative_ratios.index
    completed_transfers = relative_ratios.values
    created_transfers = 100 - completed_transfers  

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, region in enumerate(regions):
        sizes = [completed_transfers[i], created_transfers[i]]
        labels = ['Completed Transfers', 'Created Transfers']
        colors = ['#66b3ff', '#ff9a98']  
        
        wedges, texts, autotexts = axes[i].pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
        )
        
        axes[i].axis('equal')
        axes[i].set_title(f'Ratio of Transfers in {region}')
        
        for w in wedges:
            w.set_edgecolor('white')
    st.pyplot(fig)

    st.markdown("""
    ##### Insight:
    - The European and Other regions have less than 25% completed transfer ratios compared to created transfers. This indicates significant issues, possibly related to server issues or partner bank conversion delays.
    - North America also faces a lower completion rate of 32%, though the number of transfers is relatively lower, suggesting that this region may also need further attention in improving transfer completion.
    """)

    # (b) Platform Preferences per Region (Relative Percentages)
    st.subheader("12.2 Platform Preferences per Region (Relative Percentages)")
    st.write("""
    This bar chart displays the platform preferences for each region as relative percentages. 
    It helps in understanding platform popularity in different regions.
    """)

    platform_region_counts = pd.crosstab(df['platform'], df['region'], normalize='columns') * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    platform_region_counts.plot(kind='bar', colormap='viridis', figsize=(10, 6), ax=ax)
    plt.title('Platform Preferences by Region (Relative)')
    plt.ylabel('Percentage')
    plt.xlabel('Platform')
    plt.legend(title='Region')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("""
    ##### Insight:
    - In the Other region, approximately 50% of transfers are made from Android, indicating that Android support should be improved in these areas.
    - In both North America and Europe, iOS holds more than 40% of the share, suggesting that continued development on iOS platforms is crucial in these regions.
    """)

    # (c) Regional Demand Share
    st.subheader("12.3 Regional Demand Share")
    st.write("""
    The pie chart below illustrates the share of demand for transfers across different regions, based on the number of users who created a transfer.
    """)

    regional_demand_share = df[df['event_name'] == 'Transfer Created'].groupby('region')['user_id'].nunique()

    fig, ax = plt.subplots(figsize=(8, 5))
    regional_demand_share.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'), title='Regional Demand Share', ax=ax)
    plt.ylabel('') 
    st.pyplot(fig)

    st.markdown("""
    ##### Insight:
    - Europe and Other regions have a higher share of demand, each accounting for around 38% of the total demand. This indicates that services in these regions should be enhanced to meet growing user demand.
    - Despite the MXN-USD route being North American, its demand share is only about 23%, which suggests that more research is needed to understand the factors contributing to this lower demand.
    """)