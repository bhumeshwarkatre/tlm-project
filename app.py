# import asyncio
# import sys

# # ---------------------------------------------------
# # Windows + Playwright + Streamlit Fix
# # VERY IMPORTANT:
# # This must be before importing main.py
# # because main.py imports Playwright
# # ---------------------------------------------------

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsProactorEventLoopPolicy()
#     )

# import streamlit as st
# import pandas as pd
# import os

# from main import run_pipeline
# from config import COMPANIES_CSV

# # ---------------------------------------------------
# # Streamlit Page Config
# # ---------------------------------------------------

# st.set_page_config(
#     page_title="TLM Automation Bot",
#     page_icon="🚀",
#     layout="wide"
# )

# # ---------------------------------------------------
# # Page Header
# # ---------------------------------------------------

# st.title("🚀 TLM Automation Bot")
# st.subheader(
#     "ZIP → Google Maps → TLM Domain Check → External MX → CSV Save"
# )

# st.markdown("---")

# # ---------------------------------------------------
# # Sidebar
# # ---------------------------------------------------

# st.sidebar.header("Project Information")

# st.sidebar.info("""
# Safe automation workflow:

# ZIP → Google Maps → Domain → CSV Duplicate Check
# → TLM Domain Check → External MX → Final Save
# """)

# st.sidebar.success("Safe Mode Enabled")

# # ---------------------------------------------------
# # Main Input Section
# # ---------------------------------------------------

# zip_code = st.text_input(
#     "Enter ZIP Code",
#     placeholder="Example: 94107"
# )

# start_button = st.button("Start Automation")

# # ---------------------------------------------------
# # Start Process
# # ---------------------------------------------------

# if start_button:
#     if not zip_code:
#         st.error("Please enter ZIP code first.")
#     else:
#         with st.spinner("Running automation... Please wait..."):
#             try:
#                 count = run_pipeline(zip_code)

#                 st.success(
#                     f"Automation completed successfully.\n"
#                     f"Saved {count} fresh companies."
#                 )

#             except Exception as e:
#                 st.error(
#                     f"System Error:\n{str(e)}"
#                 )

# st.markdown("---")

# # ---------------------------------------------------
# # CSV Viewer Section
# # ---------------------------------------------------

# st.subheader("Saved Companies Database")

# if os.path.exists(COMPANIES_CSV):
#     try:
#         df = pd.read_csv(COMPANIES_CSV)

#         st.dataframe(
#             df,
#             use_container_width=True,
#             height=500
#         )

#         csv_data = df.to_csv(
#             index=False
#         ).encode("utf-8")

#         st.download_button(
#             label="Download Final CSV",
#             data=csv_data,
#             file_name="companies.csv",
#             mime="text/csv"
#         )

#     except Exception as e:
#         st.error(
#             f"CSV Read Error:\n{str(e)}"
#         )

# else:
#     st.warning(
#         "No company data found yet. Run automation first."
#     )



# import asyncio
# import sys

# # Windows + Playwright + Streamlit Fix
# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(
#         asyncio.WindowsProactorEventLoopPolicy()
#     )

# import streamlit as st
# import pandas as pd
# import os

# from main import run_pipeline
# from config import COMPANIES_CSV

# # ---------------------------------------------------
# # Page Config
# # ---------------------------------------------------

# st.set_page_config(
#     page_title="TLM Automation Bot",
#     page_icon="🚀",
#     layout="wide"
# )

# # ---------------------------------------------------
# # Header
# # ---------------------------------------------------

# st.title("🚀 TLM Automation Bot")

# st.subheader(
#     "Google Maps / Yellow Pages → TLM Domain Check → MX Check → CSV Save"
# )

# st.markdown("---")

# # ---------------------------------------------------
# # Sidebar
# # ---------------------------------------------------

# st.sidebar.header("Project Information")

# st.sidebar.info("""
# Safe workflow:

# Source → Company Extraction → Domain Clean
# → Duplicate Check → TLM Domain Check
# → MX Check → Final CSV Save
# """)

# st.sidebar.success("Safe Mode Enabled")

# # ---------------------------------------------------
# # Source Selection
# # ---------------------------------------------------

# source = st.selectbox(
#     "Select Data Source",
#     [
#         "Google Maps",
#         "Yellow Pages"
#     ]
# )

# # ---------------------------------------------------
# # Dynamic Inputs
# # ---------------------------------------------------

# zip_code = ""
# company_type = ""
# location = ""

# if source == "Google Maps":
#     zip_code = st.text_input(
#         "Enter ZIP Code",
#         placeholder="Example: 10020"
#     )

# elif source == "Yellow Pages":
#     company_type = st.text_input(
#         "Enter Company Type",
#         placeholder="Example: construction"
#     )

#     location = st.text_input(
#         "Enter Location",
#         placeholder="Example: Brooklyn, NY"
#     )

# # ---------------------------------------------------
# # Start Button
# # ---------------------------------------------------

# start_button = st.button("Start Automation")

# # ---------------------------------------------------
# # Run Pipeline
# # ---------------------------------------------------

# if start_button:
#     try:
#         with st.spinner("Running automation... Please wait..."):

#             if source == "Google Maps":
#                 if not zip_code:
#                     st.error("Please enter ZIP Code")
#                 else:
#                     count = run_pipeline(
#                         source=source,
#                         zip_code=zip_code
#                     )

#                     st.success(
#                         f"Completed Successfully. Saved {count} companies."
#                     )

#             elif source == "Yellow Pages":
#                 if not company_type or not location:
#                     st.error("Please enter Company Type and Location")
#                 else:
#                     count = run_pipeline(
#                         source=source,
#                         company_type=company_type,
#                         location=location
#                     )

#                     st.success(
#                         f"Completed Successfully. Saved {count} companies."
#                     )

#     except Exception as e:
#         st.error(f"System Error: {str(e)}")

# st.markdown("---")

# # ---------------------------------------------------
# # CSV Viewer
# # ---------------------------------------------------

# st.subheader("Saved Companies Database")

# if os.path.exists(COMPANIES_CSV):
#     try:
#         df = pd.read_csv(COMPANIES_CSV)

#         st.dataframe(
#             df,
#             # use_container_width=True,
#             width="stretch",
#             height=500
#         )

#         csv_data = df.to_csv(
#             index=False
#         ).encode("utf-8")

#         st.download_button(
#             label="Download Final CSV",
#             data=csv_data,
#             file_name="companies.csv",
#             mime="text/csv"
#         )

#     except Exception as e:
#         st.error(f"CSV Read Error: {str(e)}")

# else:
#     st.warning("No saved companies found yet.")


import asyncio
import sys

# Windows + Playwright + Streamlit Fix
if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

import streamlit as st
import pandas as pd
import os

from main import run_pipeline
from config import COMPANIES_CSV

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="TLM Automation Bot",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🚀 TLM Automation Bot")

st.subheader(
    "Google Maps / Yellow Pages / LinkedIn → TLM → MX → CSV"
)

st.markdown("---")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("Project Information")

st.sidebar.info("""
Safe workflow:

Source → Company Extraction → Domain Clean
→ Duplicate Check → TLM Domain Check
→ MX Check → Final CSV Save
""")

st.sidebar.success("Safe Mode Enabled")

# ---------------------------------------------------
# Source Selection
# ---------------------------------------------------

source = st.selectbox(
    "Select Data Source",
    [
        "Google Maps",
        "Yellow Pages",
        "LinkedIn"
    ]
)

# ---------------------------------------------------
# Dynamic Inputs
# ---------------------------------------------------

zip_code = ""
company_type = ""
location = ""
size = ""

if source == "Google Maps":
    zip_code = st.text_input(
        "Enter ZIP Code",
        placeholder="Example: 10020"
    )

elif source == "Yellow Pages":
    company_type = st.text_input(
        "Enter Company Type",
        placeholder="Example: construction"
    )

    location = st.text_input(
        "Enter Location",
        placeholder="Example: Brooklyn, NY"
    )

elif source == "LinkedIn":
    company_type = st.text_input(
        "Enter Company Type",
        placeholder="Example: IT company"
    )

    location = st.text_input(
        "Enter ZIP Code or Location",
        placeholder="Example: 10001 or New York"
    )

    size = st.selectbox(
        "Select Company Size",
        [
            "2-10",
            "11-50",
            "Both"
        ]
    )

# ---------------------------------------------------
# Start Button
# ---------------------------------------------------

start_button = st.button("Start Automation")

# ---------------------------------------------------
# Run Pipeline
# ---------------------------------------------------

if start_button:
    try:
        with st.spinner("Running automation... Please wait..."):

            if source == "Google Maps":
                if not zip_code:
                    st.error("Please enter ZIP Code")
                else:
                    count = run_pipeline(
                        source=source,
                        zip_code=zip_code
                    )

                    st.success(
                        f"Completed Successfully. Saved {count} companies."
                    )

            elif source == "Yellow Pages":
                if not company_type or not location:
                    st.error("Please enter Company Type and Location")
                else:
                    count = run_pipeline(
                        source=source,
                        company_type=company_type,
                        location=location
                    )

                    st.success(
                        f"Completed Successfully. Saved {count} companies."
                    )

            elif source == "LinkedIn":
                if not company_type or not location:
                    st.error("Please enter Company Type and Location")
                else:
                    count = run_pipeline(
                        source=source,
                        company_type=company_type,
                        location=location,
                        size=size
                    )

                    st.success(
                        f"Completed Successfully. Saved {count} companies."
                    )

    except Exception as e:
        st.error(f"System Error: {str(e)}")

st.markdown("---")

# ---------------------------------------------------
# CSV Viewer
# ---------------------------------------------------

st.subheader("Saved Companies Database")

if os.path.exists(COMPANIES_CSV):
    try:
        df = pd.read_csv(COMPANIES_CSV)

        st.dataframe(
            df,
            width="stretch",
            height=500
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Final CSV",
            data=csv_data,
            file_name="companies.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"CSV Read Error: {str(e)}")

else:
    st.warning("No saved companies found yet.")