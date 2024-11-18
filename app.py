import streamlit as st
import home
import individual_analysis
import comparative_analysis
import demand_analysis
import relative_analysis
import detailed_analysis



# List of page names and their display functions
pages = [
    ("Home", home.display),
    ("Individual Analysis", individual_analysis.display),
    ("Comparative Analysis", comparative_analysis.display),
    ("Demand Analysis", demand_analysis.display),
    ("Relative Analysis", relative_analysis.display),
    ("Detailed Analysis", detailed_analysis.display)
]

st.title("Wise internal data analysis for MXN-USD route")

# Create tabs for each page
tab_names = [page[0] for page in pages]
tabs = st.tabs(tab_names)


# Display content for each tab
for i, tab in enumerate(tabs):
    with tab:
        pages[i][1]()



# # Display all sections on the same page
# for page_name, display_function in pages:
#     st.header(page_name)
#     display_function()
