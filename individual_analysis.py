# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
    st.title("Individual Analysis of Key User Attributes")
    st.write("The following plots contain the individual analysis for all the columns present in the dataset.")

    # Event Breakdown
    st.header("1. Event Breakdown")
    st.markdown("**Type:** Funnel Chart")
    st.markdown("**Description:** This chart illustrates the total amount of transfers associated with each key event: Transfer Created, Transfer Funded, and Transfer Transferred.")
    transition_counts = df['event_name'].value_counts()
    labels = transition_counts.index.tolist()
    values = transition_counts.values.tolist()
    fig = px.funnel(
        y=labels,
        x=values,
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig)
    st.markdown("""
        ##### Insight:
        - The most frequent event is **Transfer Created**, indicating that initiating transfers is the primary activity among users.
        - However, the relatively lower occurrences of **Transfer Funded** and **Transfer Transferred** suggest a significant drop-off in the transfer process.
        - This highlights a potential opportunity to investigate why many transfers are created but do not progress to completion. Addressing this gap could improve overall user satisfaction and business outcomes.
    """)

    # Transfers Distribution Over Month
    st.header("2. Transfer Distribution")
    st.markdown("**Description:** This section explores the distribution of transfers over time, analyzed by month, week, and day. These visualizations provide insights into how the transfer activity evolves and fluctuates over different time intervals.")

    # By Month
    st.subheader("2.1. By Month")
    st.markdown("**Type:** Line Chart")
    st.markdown("**Description:** This chart visualizes the monthly trends in the number of transfers, providing an aggregated view of how activity evolves over time.")
    monthly_counts = df.groupby('month')['event_name'].count()
    fig, ax = plt.subplots(figsize=(12, 5))
    monthly_counts.plot(kind='line', marker='o', title='Transfers Distribution by Month', color='teal', ax=ax)
    plt.xlabel('Month')
    plt.ylabel('Number of Transfers')
    plt.grid(True)
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - The data is available only for **January** and **February**.
        - In **January**, the number of transfers was around **30,000**, while in **February** it increased to approximately **40,000**.
        - This shows a **positive growth trend**, indicating increased user engagement or system usage from January to February.
    """)

    # By Week
    st.subheader("2.2. By Week")
    st.markdown("**Type:** Line Chart")
    st.markdown("**Description:** This chart visualizes the weekly trends in the number of transfers, highlighting fluctuations and patterns in user activity throughout the weeks.")
    weekly_counts = df.groupby('week')['event_name'].count()
    fig, ax = plt.subplots(figsize=(12, 5))
    weekly_counts.plot(kind='line', marker='o', title='Transfers Distribution by Week', color='orange', ax=ax)
    plt.xlabel('Week')
    plt.ylabel('Number of Transfers')
    plt.grid(True)
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - **Weekly fluctuations** can be seen in the chart, with some weeks having more transfers than others.
        - The **peak weeks** indicate high user activity, while **dip weeks** may suggest lower engagement or external factors affecting transfer volume.
        - This analysis is useful for identifying weekly trends, and understanding which weeks have higher or lower transfer activity.
    """)

    # By Day
    st.subheader("2.3. By Day")
    st.markdown("**Type:** Line Chart")
    st.markdown("**Description:** This chart provides a daily breakdown of transfer events, showing how user activity varies from day to day.")
    daily_counts = df.groupby('day')['event_name'].count()
    fig, ax = plt.subplots(figsize=(12, 5))
    daily_counts.plot(kind='line', marker='o', title='Transfers Distribution by Day', color='purple', ax=ax)
    plt.xlabel('Day')
    plt.ylabel('Number of Transfers')
    plt.grid(True)
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - This chart shows the **daily trends** in transfers, highlighting specific days with **higher or lower activity**.
        - Certain days may show spikes in transfer activity, which could correlate with user behavior, promotions, or external factors (e.g., weekends or holidays).
        - Analyzing these trends helps identify specific days where user activity is concentrated, allowing for targeted strategies or operational adjustments.
    """)

    # Region Distribution
    st.header("3. Region Distribution")
    st.markdown("**Type:** Pie Chart")
    st.markdown("**Description:** This chart illustrates the distribution of events across various regions, providing a visual representation of where the majority of user activity is concentrated.")
    region_counts = df['region'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    region_counts.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('pastel'), ax=ax)
    plt.ylabel('')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - The distribution of transfers across three regions is as follows:
            - **Other**: 38.2%
            - **Europe**: 35.1%
            - **North America**: 26.7%
        - The highest proportion of transfers comes from the **Other** region, which may include various smaller or emerging markets.
        - Europe follows closely behind, while North America accounts for a smaller share of the total transfer activity.
    """)

    # Platform Distribution
    st.header("4. Platform Distribution")
    st.markdown("**Type:** Bar Chart")
    st.markdown("**Description:** This chart displays the distribution of platforms used for transfers, offering a detailed look at how users engage with the platform across different devices.")
    platform_counts = df['platform'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=platform_counts.index, y=platform_counts.values, palette='viridis', ax=ax)
    plt.title('Platform Distribution')
    plt.xlabel('Platform')
    plt.ylabel('Number of Transfers')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - **Android** leads with the highest number of transfers, with approximately **26,000** transfers made from this platform.
        - **iOS** follows with around **24,000** transfers, while the **Web** platform accounts for around **18,000** transfers.
        - This suggests that mobile platforms (Android and iOS) are the preferred choice for users, with web usage trailing behind.
    """)

    # User Experience Distribution
    st.header("5. User Experience Distribution")
    st.markdown("**Type:** Bar Chart")
    st.markdown("**Description:** This chart provides a clear view of the distribution of user experience categories, showcasing the breakdown of users based on their experience level with the platform. ")
    experience_counts = df['experience'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=experience_counts.index, y=experience_counts.values, palette='muted', ax=ax)
    plt.title('User Experience Distribution')
    plt.xlabel('Experience')
    plt.ylabel('Count')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - The distribution of user experiences shows a mix of **new** and **existing** users.
        - Understanding the breakdown between new users and those with more experience can provide insights into onboarding effectiveness, user retention, and overall satisfaction with the platform.
        - Strategies aimed at improving the experience for both groups may be beneficial.
    """)