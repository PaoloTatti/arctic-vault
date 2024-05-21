import replicate
import streamlit as st

from arcticvault.data_engineer.data_engineer import DataEngineerAssistant
from arcticvault.data_engineer.utils import extract_sql_blocks
from arcticvault.ui_functions import render_app_logo


st.set_page_config(
    page_title="❄️ Arctic Data Engineer ❄️",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(render_app_logo(), unsafe_allow_html=True)

st.title("Data Engineer")

with st.expander(label="🚀 Discover Arctic Data Engineer 🚀", expanded=False):

    st.write(
        "👋 **Meet Arctic Data Engineer!** 👋<br>"
        "Harness the full power of your data with our cutting-edge Data Engineer.",
        " Upon receiving the comprehensive report from the Data Architect, "
        "the Data Engineer meticulously generates all the SQL ",
        "queries you need to create your Data Vault 2.0 tables. 🗄️✨",
        unsafe_allow_html=True
    )

    st.write(
        "With precision and expertise, our Arctic Data Engineer ensures that your",
        " data is structured perfectly, enabling you to unlock the full potential of your Data Vault 2.0.<br> "
        "Say goodbye to manual query writing and hello to seamless data management! 🔍💡",
        unsafe_allow_html=True
    )



with st.sidebar:
    documents = st.file_uploader(
        label="Upload The report created by the data engineer",
        type=["txt"],
        accept_multiple_files=False,
        help="Upload one or multiple csv files",
        key="report_data_analysis",
    )

    if (
        "report_data_analysis" in st.session_state.keys()
        and st.session_state.get("report_data_analysis", []) is not None
    ):
        with st.popover("Report Data Analyst", use_container_width=True):
            report_file = (
                st.session_state.get("report_data_analysis", None)
                .getvalue()
                .decode("utf-8")
            )
            st.write(report_file)

if "data_engineer_chat" not in st.session_state.keys():
    st.session_state["data_engineer_chat"] = []

sql_code_generation_column, chat_session_data_vault = st.columns(2)

if st.session_state.get("report_data_analysis", None) is not None:
    # with sql_code_generation_column:
    if st.button("Generate SQL code", use_container_width=True):
        
        input_report = st.session_state.get("report_data_analysis").getvalue().decode("utf-8")

        input_hubs = DataEngineerAssistant(
            table_type="hubs",
            input_report=input_report
        ).get_model_input_sql_generation()
        
        input_links = DataEngineerAssistant(
            table_type="links",
            input_report=input_report
        ).get_model_input_sql_generation()
        

        input_satellites = DataEngineerAssistant(
            table_type="satellites",
            input_report=input_report
        ).get_model_input_sql_generation()
        

        st.write("**🏢 Hub Tables 🏢**")

        
        with st.spinner("Generating 🏢 Hub Tables SQL Code..."):
            chain_output_hubs = []
            
            for event_hubs in replicate.run(
                "snowflake/snowflake-arctic-instruct",
                input=input_hubs,
            ):  
                chain_output_hubs.append(str(event_hubs))
                response_hubs = "".join(chain_output_hubs)
            
            sql_code_hubs = "```sql\n"+ extract_sql_blocks(response_hubs) + "```"
            st.write(sql_code_hubs, unsafe_allow_html=True)
                
        

        st.write("**🔗 Link Tables 🔗**")

        with st.spinner("Generating 🔗 Link Tables SQL Code..."):
            chain_output_links = []
            
            for event_links in replicate.stream(
                "snowflake/snowflake-arctic-instruct",
                input=input_links,
            ):  
                chain_output_links.append(str(event_links))
                response_links = "".join(chain_output_links)
            
            sql_code_links = "```sql\n"+ extract_sql_blocks(response_links) + "```"
            st.write(sql_code_links, unsafe_allow_html=True)
                
        
        st.write("**🛰️ Satellite Tables 🛰️**")
        
        with st.spinner("Generating 🛰️ Satellite Tables SQL Code..."):
            chain_output_satellites = []
            for event_satellite in replicate.stream(
                "snowflake/snowflake-arctic-instruct",
                input=input_satellites,
            ):  
                chain_output_satellites.append(str(event_satellite))
                response_satellites = "".join(chain_output_satellites)
        
        sql_code_satellites = "```sql\n"+ extract_sql_blocks(response_satellites) + "```"
        st.write(sql_code_satellites, unsafe_allow_html=True)
                


        