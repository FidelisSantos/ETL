import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_files_tab(files_df, realtime_files_df):
    st.subheader("📡 Realtime Active Files")
    if not realtime_files_df.empty:
        f1, f2, f3 = st.columns([1, 2, 2]) 
        with f1:
            client_filter = st.multiselect("Realtime Client:", options=realtime_files_df['client'].dropna().unique(), key="realtime_files_client")
        with f2:
            organization_filter = st.multiselect("Realtime Organization:", options=realtime_files_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_files_organization")
        with f3:
            company_filter = st.multiselect("Realtime Company:", options=realtime_files_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_files_company")

        has_report_bool = realtime_files_df["has_report"].astype(bool)

        filtered_realtime_files_df = realtime_files_df.copy()
        if client_filter:
            filtered_realtime_files_df = filtered_realtime_files_df[filtered_realtime_files_df['client'].isin(client_filter)]
        if organization_filter:
            filtered_realtime_files_df = filtered_realtime_files_df[filtered_realtime_files_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)]
        if company_filter:
            filtered_realtime_files_df = filtered_realtime_files_df[filtered_realtime_files_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)]

        total_files = filtered_realtime_files_df["total_files"].sum()
        files_com_report = filtered_realtime_files_df.loc[has_report_bool, "total_files"].sum()
        files_sem_report = filtered_realtime_files_df.loc[~has_report_bool, "total_files"].sum()

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.metric("Total Files", total_files)
        with col2:
            st.metric("Files with Report", files_com_report)
        with col3:
            st.metric("Files without Report", files_sem_report)
        with col4:
            st.metric("Unique Clients", realtime_files_df['client'].nunique())
        with col5:
            st.metric("Organizations", realtime_files_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).nunique())
        with col6:
            st.metric("Companies", realtime_files_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).nunique())
        with col7:
            st.metric("Workstations", realtime_files_df['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).nunique())

        realtime_display = realtime_files_df.copy()
        realtime_display["organization_name"] = realtime_display["organization"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        realtime_display["company_name"] = realtime_display["company"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        realtime_display["workstation_name"] = realtime_display["workstation"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)

    st.subheader("Filters")
    default_start = datetime.today() - timedelta(days=60)
    default_end = datetime.today()
    date_range = st.date_input(
        "Date interval:",
        [default_start, default_end],
        key="files_date"
    )

    col_client, col_org, col_comp, col_ws = st.columns(4)
    with col_client:
        client_filter = st.multiselect("Cliente:", options=files_df['client'].dropna().unique(), key="files_client")
    with col_org:
        organization_filter = st.multiselect(
            "Organization:",
            options=files_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="files_organization"
        )
    with col_comp:
        company_filter = st.multiselect(
            "Company:",
            options=files_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="files_company"
        )
    with col_ws:
        workstation_filter = st.multiselect(
            "Workstation:",
            options=files_df['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="files_workstation"
        )

    file_filter = st.text_input("File name:", key="files_file_name")

    filtered_files = files_df.copy()
    if len(date_range) == 2:
        filtered_files = filtered_files[
            (filtered_files['created_at'] >= pd.to_datetime(date_range[0])) &
            (filtered_files['created_at'] <= pd.to_datetime(date_range[1]))
        ]
    if not len(date_range) == 2:
        st.warning("Selecione um intervalo de datas válido.")
        filtered_files = pd.DataFrame()
    if client_filter:
        filtered_files = filtered_files[filtered_files['client'].isin(client_filter)]
    if organization_filter:
        filtered_files = filtered_files[
            filtered_files['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)
        ]
    if company_filter:
        filtered_files = filtered_files[
            filtered_files['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)
        ]
    if workstation_filter:
        filtered_files = filtered_files[
            filtered_files['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(workstation_filter)
        ]
    if file_filter:
        filtered_files = filtered_files[filtered_files['original_name'].str.contains(file_filter, case=False, na=False)]

    if not filtered_files.empty:
        filtered_files["organization_name"] = filtered_files["organization"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        filtered_files["company_name"] = filtered_files["company"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        filtered_files["workstation_name"] = filtered_files["workstation"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)

        col1, col2, col3, col4 = st.columns(4)
        total_files = len(filtered_files)
        avg_duration = filtered_files["duration"].mean() if not filtered_files["duration"].empty else 0
        col1.metric("Total Files", total_files)
        col2.metric("Average Duration (s)", round(avg_duration, 2))
        col3.metric("Organizations", filtered_files['organization_name'].nunique())
        col4.metric("Companies", filtered_files['company_name'].nunique())

        display_df = filtered_files[[
            "original_name", "generated_name", "duration", "status",
            "client", "organization_name", "company_name", "workstation_name",
            "created_at"
        ]]

        display_df = display_df.sort_values("created_at", ascending=False)

        st.dataframe(
            display_df,
            column_config={
                "original_name": "📹 Original Name",
                "generated_name": "📹 Generated Name",
                "duration": "⏱ Duration",
                "status": "🔘 Status",
                "client": "👤 Client",
                "organization_name": "🏢 Organization",
                "company_name": "🏭 Company",
                "workstation_name": "💻 Workstation",
                "created_at": st.column_config.DatetimeColumn("📅 Created At", format="YYYY-MM-DD"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No files found for applied filters.")

    st.subheader("Status Resume")
    if not filtered_files.empty:
        status_summary = filtered_files.groupby("status").size().reset_index(name="count")
        st.bar_chart(status_summary.set_index("status"))

    st.subheader("Data Resume")
    if not filtered_files.empty:
        filtered_files["date_only"] = pd.to_datetime(filtered_files["created_at"]).dt.date

        date_summary = (
            filtered_files.groupby(["client", "date_only"])
            .size()
            .reset_index(name="count")
            .sort_values(["date_only"])
        )

        display_date_df = date_summary.copy()
        display_date_df.rename(columns={
            "client": "👤 Client",
            "date_only": "📅 Date",
            "count": "🔢 Count"
        }, inplace=True)

        st.dataframe(
            display_date_df,
            column_config={
                "👤 Client": "👤 Client",
                "📅 Date": st.column_config.DatetimeColumn("📅 Date", format="YYYY-MM-DD"),
                "🔢 Count": "🔢 Count"
            },
            use_container_width=True,
            hide_index=True
        )

        daily_summary = date_summary.groupby("date_only")["count"].sum()
        st.bar_chart(daily_summary)

