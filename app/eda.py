import streamlit as st
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

def visualize(uploaded_file):
    if type(uploaded_file) is not str:
        uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
    st.title("Visualize Data")
    st.markdown('**1. Glimpse of dataset**')
    st.write(df)
    pr = df.profile_report()
    with st.expander("REPORT", expanded=True):
        st_profile_report(pr)