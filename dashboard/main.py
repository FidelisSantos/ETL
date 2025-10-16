import streamlit as st
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

from tabs import render_reports_tab, render_files_tab, render_action_plans_tab

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:password@mongodb:27017/")
DB_NAME = os.getenv("DB_NAME", "etl")

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
action_plans_df = load_collection("action_plans")
realtime_action_plans_df = load_collection("realtime_action_plans_actions")

tab = st.tabs(["Reports", "Files", "Action Plans"])

with tab[0]:
    render_reports_tab(reports_df, realtime_reports_df)

with tab[1]:
    render_files_tab(files_df, realtime_files_df)

with tab[2]:
    render_action_plans_tab(action_plans_df, realtime_action_plans_df)