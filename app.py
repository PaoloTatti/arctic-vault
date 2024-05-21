import os

import streamlit as st

from arcticvault.ui_functions import render_app_logo

st.set_page_config(
    page_title="Arctic Vault",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(render_app_logo(), unsafe_allow_html=True)

os.environ["REPLICATE_API_TOKEN"] = st.secrets["api_key"]["REPLICATE_API_TOKEN"]

st.title("❄️ Arctic Vault")

st.subheader("What is **Arctic Vault**")
st.write(
    "Arctic Vault is a tool that allows you to to create your personal Data Vault 2.0 using AI assistance."
)
st.write(
    """
    🎯 **The Arctic Vault Agent will help you to perform the following tasks:**

    1. **🔍 Data Analysis and Requirement Gathering:**
        - Analyze the input data to understand its structure, relationships, and business context.
        - Identify all the entities (🏢 Hubs), relationships (🔗 Links), and descriptive attributes (🛰️ Satellites) in the data.
        - Determine any specific requirements or constraints for modeling the data, such as compliance regulations or performance considerations.
    """,
    unsafe_allow_html=True,
)
st.page_link(
    "pages/01 🔍 Data Analyst.py",
    label="Arctic Data Analyst",
    icon="🔍",
    use_container_width=True,
)
st.write(
    """2. **📊 Data Model Creation:**
    - Based on the analysis, design the Data Vault 2.0 model by defining 🏢 Hubs, 🔗 Links, and 🛰️ Satellites.
    - Establish the relationships between entities and determine the keys and attributes for each table.
    - Ensure that the model meets the identified requirements and aligns with best practices for Data Vault 2.0.""",
    unsafe_allow_html=True,
)
st.write(
    """3. **💻 SQL Code Generation:**
    - Generate SQL code to create the tables based on the designed Data Vault 2.0 model.
    - Include appropriate data types, constraints, and indexes in the SQL code to optimize performance and ensure data integrity.
    - Handle any additional SQL statements required for setting up sequences, triggers, or other database-specific configurations.
""",
    unsafe_allow_html=True,
)
st.page_link(
    "pages/02 💻 Data Engineer.py",
    label="Arctic Data Engineer",
    icon="💻",
    use_container_width=True,
)