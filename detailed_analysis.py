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
    st.title("Detailed Transfer Analysis")
    st.write("""
    This section visualizes the transfer funnels for each region. The funnel plots display the transition of users through different events, such as 
    'Transfer Created', 'Transfer Transferred', etc., in terms of raw counts and percentages.
    """)

    st.header("13. Region Wise Transfer Funnels")
    region_funnel = df.groupby(['region', 'event_name']).size().unstack(fill_value=0)
    for idx, region in enumerate(region_funnel.index):
        st.subheader(f"13.{idx + 1} {region}: Transfer Funnel for {region}")
        st.write(f"**Region: {region}** - The funnel plot below represents the number of users transitioning through different events.")
        region_data = region_funnel.loc[region]
        region_funnel_percentage = (region_data / region_data.sum()) * 100

        fig = px.funnel(
            y=region_data.index, 
            x=region_data.values, 
            title=f'Transfer Funnel for Region: {region}',
            color_discrete_sequence=px.colors.sequential.Agsunset
        )
        hover_text = [
            f"Event: {y}<br>Count: {x}<br>Percentage: {percent:.2f}%"
            for x, y, percent in zip(region_data.values, region_data.index, region_funnel_percentage.values)
        ]
        fig.update_traces(hovertemplate=hover_text)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ##### Insight:
    - Europe and Other regions have high 'Transfer Created' counts but much lower 'Transfer Funded' and 'Transfer Transferred' counts, suggesting possible issues like partner bank delays or technical problems.
    - In Europe, the 'Transfer Transferred' count is unexpectedly higher than 'Transfer Funded', which may point to data discrepancies or misconfiguration in event tracking.
    """)

    # Region-Platform Funnel Analysis
    st.header("14. Region-Platform Funnel Analysis")
    st.write("""
    This section visualizes funnel charts for each region-platform combination. 
    The subplots provide insights into user transitions across events based on their region and platform. 
    Each subplot represents a specific region-platform combination.
    """)
    platform_region_funnel = df.groupby(['region', 'platform', 'event_name']).size().unstack(fill_value=0)
    platform_region_funnel_percentage = (
        platform_region_funnel.div(platform_region_funnel.sum(axis=1), axis=0) * 100
    ).round(2)

    regions = ['NorthAm', 'Europe', 'Other']
    platforms = ['iOS', 'Android', 'Web']

    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[f'{region} - {platform}' for region in regions for platform in platforms],
        shared_yaxes=True,
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    for i, region in enumerate(regions):
        for j, platform in enumerate(platforms):
            region_platform_data = platform_region_funnel.loc[(region, platform)]
            total_count = region_platform_data.sum()
            percentages = (region_platform_data / total_count) * 100

            hover_data = [
                f"Event Name = {event}<br>Count = {count}<br>Percentage = {percentage:.2f}%"
                for event, count, percentage in zip(region_platform_data.index, region_platform_data.values, percentages)
            ]
            trace = go.Funnel(
                y=region_platform_data.index,
                x=region_platform_data.values,
                hovertemplate=hover_data,
                name=f'{region} - {platform}'
            )
            fig.add_trace(
                trace, row=i+1, col=j+1
            )

    fig.update_layout(
        height=900,
        width=1400,
        title_text="Funnel by Region and Platform",
        showlegend=False, 
        title_x=0.5, 
        title_y=0.95 
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ##### Insight:
    - In North America, both iOS and Android platforms perform well, but the Web platform is underperforming, particularly in the 'Transfer Funded' stage.
    - In Europe, across all platforms, the 'Transfer Transferred' count exceeds 'Transfer Funded', which may indicate issues with event tracking or a data anomaly.
    """)