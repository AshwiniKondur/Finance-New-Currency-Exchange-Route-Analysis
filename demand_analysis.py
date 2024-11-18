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

    st.title("Regional Demand Analysis")
    st.write("This section analyzes the demand for transfers by time intervals: weekly, monthly, and daily, focusing on the behavior of new and existing users.")

    # Weekly, Monthly, and Daily Demand Analysis
    st.header("11. Weekly, Monthly, and Daily Demand Analysis")

    # Monthly Demand Analysis: Heatmap
    st.subheader("11.1 Monthly Demand Analysis")
    st.markdown("**Type:** Heatmap")
    st.markdown("**Description:** The heatmap below displays the monthly demand for transfers, broken down by region. Darker shades indicate higher demand.")

    monthly_heatmap = df[df['event_name'] == 'Transfer Created'].groupby(['month', 'region']).size().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(monthly_heatmap, cmap='YlGnBu', annot=True, fmt='.0f', cbar_kws={'label': 'Number of Transfers'}, ax=ax)
    plt.title('Monthly Demand for Transfers by Region')
    plt.ylabel('Month')
    plt.xlabel('Region')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # Weekly Demand Analysis: Double Bar Charts
    st.subheader("11.2 Weekly Demand Analysis")
    st.markdown("**Type:** Double Bar Chart")
    st.markdown("**Description:** This bar chart shows the weekly demand for transfers, categorized by regions.")

    # Group by week and region to calculate transfer counts
    demand_weekly_bar_region = df[df['event_name'] == 'Transfer Created'].groupby(['week', 'region']).size().reset_index(name='transfers')

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=demand_weekly_bar_region,
        x='week', y='transfers', hue='region',
        errorbar=None, palette='viridis', ax=ax
    )
    plt.title('Weekly Demand for Transfers by Region')
    plt.ylabel('Number of Transfers')
    plt.xlabel('Week')
    plt.xticks(rotation=45)
    plt.legend(title='Region')
    plt.tight_layout()
    st.pyplot(fig)

    # Daily Demand Analysis: Stacked Area Chart
    st.subheader("11.3 Daily Demand Analysis")
    st.markdown("**Type:** Line Chart")
    st.markdown("**Description:** This line chart shows the daily demand for transfers, broken down by region.")

    daily_demand = df[df['event_name'] == 'Transfer Created'].groupby(['day', 'region']).size().unstack(fill_value=0)
    daily_demand.index = daily_demand.index.astype(str)

    fig, ax = plt.subplots(figsize=(12, 6))
    daily_demand.plot(kind='line', colormap='viridis', marker='o', ax=ax)
    plt.title('Daily Demand for Transfers by Region')
    plt.ylabel('Number of Transfers')
    plt.xlabel('Day')
    tick_interval = max(1, len(daily_demand.index) // 10)
    plt.xticks(
        ticks=range(0, len(daily_demand.index), tick_interval),
        labels=daily_demand.index[::tick_interval],
        rotation=45
    )
    plt.legend(title='Region')
    plt.tight_layout()
    st.pyplot(fig)

    # Insight for all three charts
    st.markdown("""
    ##### Insight:
    - In the initial period, the demand for transfers in all three regions—**Europe**, **North America**, and **Other**—was relatively low. This can be attributed to the newly launched route, which had not yet reached significant adoption. The early stages of product or service launches often show low engagement as users are still becoming acquainted with the platform.

    - However, **Europe** saw a significant rise in demand starting from **February 1st**. The total number of transfers in February increased by more than **9,000** compared to January, highlighting a strong growth trend in the region. This spike indicates that users in Europe have started to adopt the new route, likely driven by better awareness, improved marketing, or increased user interest.

    - In contrast, both **North America** and **Other regions** experienced a slight reduction in transfer demand during the same period. While the decrease was not drastic, it suggests that there may be underlying issues in these regions. These issues could stem from user experience concerns, technical challenges, or limited awareness of the new route. Further investigation is needed to understand why demand declined slightly in these regions, especially after the initial launch phase.

    - **Conclusion:** The overall trend suggests that Europe is showing positive growth in transfer demand, particularly in February, while North America and Other regions may need further attention to address potential barriers to sustained engagement. Targeted marketing, customer support, or product improvements in these regions could help reverse the downward trend and drive higher adoption in the upcoming months.
    """)
