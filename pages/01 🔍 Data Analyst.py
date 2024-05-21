import pandas as pd
import streamlit as st
import replicate

from arcticvault.data_analyst.data_analyst import DataAnalystAssistant
from arcticvault.data_analyst.utils import format_tables, execute_report_creation
from arcticvault.ui_functions import render_app_logo

st.set_page_config(
    page_title="Arctic Data Analyst",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(render_app_logo(), unsafe_allow_html=True)

st.title("Arctic Data Analyst")

with st.expander(
    label="🌟 Discover Arctic Data Analyst and Arctic Data Architect 🌟", expanded=False
):

    st.write(
        "🎉 **Meet Arctic Data Analyst!** 🎉\n"
        "Ready to revolutionize your data management? Enter your data, "
        "and our expert Data Analyst will guide you through every detail. "
        "By asking insightful questions, he ensures a deep understanding of your data, ",
        "providing you with all the information needed to craft a state-of-the-art Data Vault 2.0. 🚀",
    )

    st.write(
        "💡 **Meet Arctic Data Architect!** 💡\n"
        "Based on the thorough analysis from the Data Analyst, ",
        "the Data Architect will generate a comprehensive report. ",
        "This report summarizes all the requirements and provides ",
        "you with a clear blueprint to create your Data Vault 2.0 with ease and precision. 🏆",
    )


with st.sidebar:
    documents = st.file_uploader(
        label="Upload all tables you want to add to your Data Vault 2.0",
        type=["csv"],
        accept_multiple_files=True,
        help="Upload one or multiple csv files",
        key="analyst_documents",
    )

    if st.session_state.get("analyst_documents", None) is not None:
        format_tables(tables=documents)

    if len(st.session_state.get("analyst_documents", [])):
        with st.popover("Visualize a table 📊", use_container_width=True):
            _ = st.selectbox(
                label="Select a table you wish to inspect",
                options=st.session_state.get("analyst_documents", []),
                key="analyst_table_visualize",
                index=None,
                format_func=lambda x: x.name,
            )
            df_file_name = st.session_state.get("analyst_table_visualize", None)
            if df_file_name is not None:
                df = pd.read_csv(df_file_name)
                st.dataframe(df)

    if st.button("Clear chat 🧹", use_container_width=True):
        st.session_state["analyst_chat"] = [
            {
                "role": "user",
                "content": f"{st.session_state.get('table_information')}",
            }
        ]
    if st.button("Generate Report with Data Architect💡", use_container_width=True):
        execute_report_creation()

if len(st.session_state.get("table_information", "")) > 0:

    if "analyst_chat" not in st.session_state.keys():
        st.session_state["analyst_chat"] = [
            {
                "role": "user",
                "content": f"{st.session_state.get('table_information')}",
            }
        ]

    user_message = st.chat_input(placeholder="Enter your question")
    if user_message:
        st.session_state["analyst_chat"].append(
            {
                "role": "user",
                "content": user_message,
            }
        )

    for message in st.session_state["analyst_chat"][1:]:
        if message["role"] == "system":
            continue
        elif message["role"] == "assistant":
            with st.chat_message(
                name=message["role"], avatar="static/arctic-vault.png"
            ):
                st.write(message["content"], unsafe_allow_html=True)
        elif message["role"] == "error":
            st.error(message["content"])
        else:
            with st.chat_message(name=message["role"], avatar="⛷️"):
                st.write(message["content"], unsafe_allow_html=True)

    if st.session_state["analyst_chat"][-1]["role"] not in ("assistant", "system"):
        with st.chat_message(name="assistant", avatar="static/arctic-vault.png"):
            content = st.session_state["analyst_chat"][-1]["content"]

            model_chat_input = DataAnalystAssistant(
                history=st.session_state["analyst_chat"]
            ).get_chat_chain()

            model_chat_input["prompt"] = content

            chain_output = []
            placeholder = st.empty()
            for event in replicate.stream(
                "snowflake/snowflake-arctic-instruct",
                input=model_chat_input,
            ):
                chain_output.append(str(event))
                response = "".join(chain_output)
                placeholder.write(response, unsafe_allow_html=True)

            message = {
                "role": "assistant",
                "content": response,
            }

            st.session_state["analyst_chat"].append(message)
else:
    st.warning(
        "Before the chat will be enabled, you need to add some tables in CSV format on the upload button in the left sidebar"
    )
