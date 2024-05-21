from typing import List

import replicate
import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from arcticvault.data_analyst.data_analyst import DataAnalystAssistant

@st.experimental_dialog("Add your data", width="large")
def add_data_table():
    documents = st.file_uploader(
        label="Upload all tables you want to add to your Data Vault",
        type=["csv"],
        accept_multiple_files=True,
        help="Upload one or multiple csv files",
        key="analyst_documents",
    )
    
    if st.session_state.get("analyst_documents", None) is not None:
        _ = st.selectbox(
            label="Select a table you wish to inspect",
            options=st.session_state.get("analyst_documents", []),
            key="analyst_table_visualize",
            index=None,
            format_func=lambda x: x.name,
        )
        df_file_name = st.session_state.get("analyst_table_visualize", None)
        if df_file_name is not None:
            st.dataframe(df_file_name)

    if st.button("Close"):
        if st.session_state.get("analyst_documents", None) is not None:
            format_tables(tables=documents)
            st.rerun()


def format_tables(tables: List[UploadedFile]) -> None:
    """
    Format and display metadata information for a list of uploaded CSV tables.

    :param tables: A list of UploadedFile objects representing CSV tables.
    :type tables: List[UploadedFile]
    :return: None

    This function takes a list of UploadedFile objects representing CSV tables,
    reads each table into a pandas DataFrame, and generates a metadata string
    containing information about the table name, number of rows and columns,
    column names, data types, and null counts. The metadata string is then
    stored in the Streamlit session state under the key "table_information".

    """
    tables_information = []

    for table in tables:
        table_name = "".join(table.name.split(".")[:-1])
        df = pd.read_csv(table)

        column_info = "\n".join(
            [
                f"- {col}"
                for col in df.columns
            ]
        )

        metadata_string = (
            f"Table Name: {table_name}\n"
            f"Columns:\n"
            f"{column_info}\n"
        )

        tables_information.append(metadata_string)

    table_information_output = "\n".join(tables_information)
    st.session_state["table_information"] = table_information_output

@st.experimental_dialog("Generate Data Architect Report", width="large")
def execute_report_creation() -> None:
    if "analyst_chat" not in st.session_state.keys():
        st.warning("Please start chatting with Arctic Data Analist first")
    else:    
        if st.button("Generate Summary", use_container_width=True):
            with st.spinner("Generating Summary..."):
                input_ = DataAnalystAssistant(
                    history=st.session_state["analyst_chat"]
                ).get_generate_summary_chain()
                
                summary = replicate.run(
                    "snowflake/snowflake-arctic-instruct",
                    input=input_,
                )
                summary_output = "".join(summary)
                summary_output = summary_output.replace("|im_start|assistant: ", "")
                st.write(summary_output, unsafe_allow_html=True)
                st.session_state["analyst_report"] = "".join(summary_output)
            if st.session_state.get("analyst_report", None) is not None:
                st.download_button(
                    label="Download Report📥",
                    mime="text/plain",
                    use_container_width=True,
                    data=st.session_state["analyst_report"],
                    file_name="Data Vault Report.txt",
                )
                
