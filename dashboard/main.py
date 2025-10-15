import streamlit as st
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

from tabs import render_reports_tab, render_files_tab

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

st.set_page_config(layout="wide")
@st.cache_data(ttl=300)
def load_collection(collection_name: str):
    cursor = db[collection_name].find()
    return pd.DataFrame(list(cursor))

reports_df = load_collection("reports")
realtime_reports_df = load_collection("realtime_reports")
files_df = load_collection("files")
realtime_files_df = load_collection("realtime_files")

tab = st.tabs(["Reports", "Files"])

with tab[0]:
    render_reports_tab(reports_df, realtime_reports_df)

with tab[1]:
    render_files_tab(files_df, realtime_files_df)