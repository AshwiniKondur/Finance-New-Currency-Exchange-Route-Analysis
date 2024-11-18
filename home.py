import streamlit as st

def display():
    st.title("User Activity and Event Analysis")
    st.subheader("Overview")

    st.markdown("""
    This dashboard provides an in-depth analysis of user activities and events related to regional transfers at Wise. The dataset contains detailed records to help uncover insights about trends, user behaviors, platform preferences, and regional variations.

    ### Dataset Description
    The dataset comprises records of events associated with user interactions and transfers. It enables tracking of activity over time, categorization of user experiences, and analysis across various regions and platforms.

    ##### Key Columns
    - **dt**: The date and time of the event, used for analyzing trends over time.
    - **event_name**: The type of event, such as `Transfer Created`, `Transfer Transferred`, etc.
    - **user_id**: A unique identifier for each user, useful for grouping and tracking individual behavior.
    - **region**: The geographical region of the user (e.g., North America, Europe).
    - **platform**: The platform used by the user to interact with Wise services (e.g., iOS, Android, Web).
    - **experience**: The user experience category, including classifications such as new and existing users.

    ##### Additional Derived Columns
    To facilitate time-based analysis, the following columns have been derived:
    - **month**: Extracted from `dt` to analyze monthly trends.
    - **week**: Extracted from `dt` to analyze weekly trends.
    - **day**: Extracted from `dt` to analyze daily trends.

    This dataset offers a comprehensive lens through which we can understand how users engage with Wise's services and observe variations across different segments.
    """)
