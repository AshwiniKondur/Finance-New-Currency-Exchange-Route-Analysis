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
    st.title("Comparative Analysis of Key User Attributes")
    st.write("The following plots contain the comparative analysis for most important / key aspects of the given data.")

    # Event by Region
    st.header("6. Event by Region")
    st.markdown("**Type:** Grouped Bar Chart")
    st.markdown("**Description:** This chart displays the number of events by region. The stacked bars show how each event is distributed across different regions.")
    event_region = pd.crosstab(df['event_name'], df['region'])
    fig, ax = plt.subplots(figsize=(10, 6))
    event_region.plot(kind='bar', colormap='coolwarm', figsize=(10, 6), ax=ax)
    plt.title('Event vs. Region')
    plt.xlabel('Event Name')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Region')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - Compared to **North America**, the **Europe** and **Other** regions are facing challenges in the transfer process.
        - The number of **Transfer Created** events is much higher than **Transfer Transferred**, particularly in these regions.
        - This could be due to the use of **MXN-USD** (Mexico to US) transfers, which might be more prevalent in the North American region.
        - A deeper investigation is needed to understand why transfers are not progressing as smoothly in other regions.
    """)

    # Platform Usage by Region
    st.header("7. Platform Usage by Region")
    st.markdown("**Type:** Stacked Bar Chart")
    st.markdown("**Description:** This chart shows the distribution of platform usage across different regions. It provides insights into which platform is most popular in each region.")
    platform_region = pd.crosstab(df['platform'], df['region'])
    fig, ax = plt.subplots(figsize=(10, 6))
    platform_region.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6), ax=ax)
    plt.title('Platform Usage by Region')
    plt.xlabel('Platform')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Region')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - More transfers in **Europe** were made using **iOS**, while in the **Other** regions, **Android** was the more preferred platform.
        - To improve user experience, platform-specific facilities should be enhanced based on regional preferences.
        - **Android** support, especially in regions with high Android usage, and increased **iOS** support in Europe, should be prioritized.
    """)

    # Experience by Platform
    st.header("8. Experience by Platform")
    st.markdown("**Type:** Grouped Bar Chart")
    st.markdown("**Description:** This chart compares the user experience distribution across platforms, distinguishing between new and existing users.")
    experience_platform = pd.crosstab(df['experience'], df['platform'])
    fig, ax = plt.subplots(figsize=(10, 6))
    experience_platform.plot(kind='bar', colormap='cividis', figsize=(10, 6), ax=ax)
    plt.title('Experience by Platform')
    plt.xlabel('Experience')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(title='Platform')
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - There are more **existing iOS users** compared to new users, suggesting that the platform has a loyal user base.
        - **Android**, however, sees a higher number of **new users**, indicating that improvements in Android services and technical aspects are needed.
        - **Web** usage, although not as high, is slowly increasing, indicating that web services are gaining traction and should be supported more.
        - Focusing on **Android** and improving its services could increase retention and satisfaction.
    """)

    # Daily Transfers by Experience
    st.header("9. Daily Transfers by Experience")
    st.markdown("**Type:** Line Chart")
    st.markdown("**Description:** This chart tracks the number of daily transfers made by users based on their experience (new or existing).")
    daily_experience = df.groupby([df['dt'], 'experience']).size().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_experience.plot(kind='line', figsize=(12, 6), marker='o', title='Daily Transfers by Experience', ax=ax)
    plt.xlabel('Date')
    plt.ylabel('Number of Transfers')
    plt.legend(title='Experience')
    plt.grid(True)
    st.pyplot(fig)
    st.markdown("""
        ##### Insight:
        - In **January**, the number of transfers made by **new** and **existing** users was almost **equal**.
        - However, by the end of **January** and the start of **February**, there was a **significant rise in transfers made by new users**.
        - This increase suggests a growing interest from new users, which could indicate higher engagement or marketing efforts targeting new users.
        - To ensure continued growth, it will be important to focus on retaining both **new** and **existing users**, as the data shows positive growth for new user transfers.
    """)

    # Percentage of Transfers Completed by Region and Experience
    st.header("10. Percentage of Transfers Completed by Region and Experience")
    st.markdown("**Type:** Pie Chart")
    st.markdown("**Description:** This set of pie charts displays the percentage of users completing transfers categorized by region and experience.")
    transferred_users = df[df['event_name'] == 'Transfer Transferred'].groupby(['region', 'experience'])['user_id'].nunique()
    total_users = df.groupby(['region', 'experience'])['user_id'].nunique()
    percentage_transferred = (transferred_users / total_users * 100).unstack()

    # Columns for layout
    col1, col2, col3 = st.columns(3)

    # North America Pie Chart
    with col1:
        st.markdown("**North America**")
        if 'NorthAm' in percentage_transferred.index:
            north_america_data = percentage_transferred.loc['NorthAm']
            fig, ax = plt.subplots(figsize=(8, 8))  # Increased figure size
            ax.pie(north_america_data, labels=north_america_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
            ax.set_title("Transfers Completed in North America")
            st.pyplot(fig)

    # Europe Pie Chart
    with col2:
        st.markdown("**Europe**")
        if 'Europe' in percentage_transferred.index:
            europe_data = percentage_transferred.loc['Europe']
            fig, ax = plt.subplots(figsize=(8, 8))  # Increased figure size
            ax.pie(europe_data, labels=europe_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
            ax.set_title("Transfers Completed in Europe")
            st.pyplot(fig)

    # Other Pie Chart
    with col3:
        st.markdown("**Other**")
        if 'Other' in percentage_transferred.index:
            other_data = percentage_transferred.loc['Other']
            fig, ax = plt.subplots(figsize=(8, 8))  # Increased figure size
            ax.pie(other_data, labels=other_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
            ax.set_title("Transfers Completed in Other Regions")
            st.pyplot(fig)

    # Insight for the Pie Charts
    st.markdown("""
    ##### Insight:
    - **North America** and **Other** regions have a similar distribution of users, with around **63% existing users** and **37% new users** completing transfers. This suggests strong user retention, but there is still room for attracting new users, especially in the **Other** region.
    - **Europe**, however, has a higher proportion of **existing users (73%)** compared to **new users (27%)**. This indicates that the MXN-USD route, although successful for existing users, is not drawing in as many new users in Europe. Efforts to market and promote this route to new users in Europe could help improve growth in this region.
    """)