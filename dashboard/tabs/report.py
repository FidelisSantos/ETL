import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_reports_tab(reports_df, realtime_reports_df):
    st.subheader("📡 Realtime Last Update Reports")
    if not realtime_reports_df.empty:
        f1, f2, f3 = st.columns([1, 2, 2])
        with f1:
            client_filter = st.multiselect("Realtime Client:", options=realtime_reports_df['client'].dropna().unique(), key="realtime_reports_client")
        with f2:
            organization_filter = st.multiselect("Realtime Organization:", options=realtime_reports_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_reports_organization")
        with f3:
            company_filter = st.multiselect("Realtime Company:", options=realtime_reports_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_reports_company")
        
        filtered_realtime_reports_df = realtime_reports_df.copy()
        if client_filter:
            filtered_realtime_reports_df = filtered_realtime_reports_df[filtered_realtime_reports_df['client'].isin(client_filter)]
        if organization_filter:
            filtered_realtime_reports_df = filtered_realtime_reports_df[filtered_realtime_reports_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)]
        if company_filter:
            filtered_realtime_reports_df = filtered_realtime_reports_df[filtered_realtime_reports_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)]

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("Total Reports (Realtime)", filtered_realtime_reports_df["report_id"].nunique())
        with col2:
            total_reba = filtered_realtime_reports_df[filtered_realtime_reports_df["type"] == "REBA"].shape[0] if "type" in filtered_realtime_reports_df.columns else 0
            st.metric("Total REBA (Realtime)", total_reba)
        with col3:
            total_niosh = filtered_realtime_reports_df[filtered_realtime_reports_df["type"] == "NIOSH"].shape[0] if "type" in filtered_realtime_reports_df.columns else 0
            st.metric("Total NIOSH (Realtime)", total_niosh)
        with col4:
            total_kim_pp = filtered_realtime_reports_df[filtered_realtime_reports_df["type"] == "KIM_PP"].shape[0] if "type" in filtered_realtime_reports_df.columns else 0
            st.metric("Total KIM PP (Realtime)", total_kim_pp)
        with col5:
            total_kim_mho = filtered_realtime_reports_df[filtered_realtime_reports_df["type"] == "KIM_MHO"].shape[0] if "type" in filtered_realtime_reports_df.columns else 0
            st.metric("Total NIOSH (Realtime)", total_kim_mho)
        with col6:
            total_strain_index = filtered_realtime_reports_df[filtered_realtime_reports_df["type"] == "STRAIN_INDEX"].shape[0] if "type" in filtered_realtime_reports_df.columns else 0
            st.metric("Total STRAIN INDEX (Realtime)", total_strain_index)


    st.subheader("Filters")
    col_date, col_file, col_type = st.columns([3, 2, 1])
    with col_date:
        default_start = datetime.today() - timedelta(days=60)
        default_end = datetime.today()
        date_range = st.date_input(
            "Date interval:",
            [default_start, default_end],
            key="reports_date"
        )
    with col_file:
        file_filter = st.text_input("File name:", key="reports_file_name")
    with col_type:
        type_filter = st.multiselect(
            "Type:",
            options=reports_df['type'].dropna().unique(),
            key="reports_type"
        )

    col_client, col_org, col_comp, col_ws = st.columns(4)
    with col_client:
        client_filter = st.multiselect("Client:", options=reports_df['client'].dropna().unique(), key="reports_client")
    with col_org:
        organization_filter = st.multiselect(
            "Organization:",
            options=reports_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="reports_organization"
        )
    with col_comp:
        company_filter = st.multiselect(
            "Company:",
            options=reports_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="reports_company"
        )
    with col_ws:
        workstation_filter = st.multiselect(
            "Workstation:",
            options=reports_df['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="reports_workstation"
        )
    

    filtered_reports = reports_df.copy()
    filtered_reports = filtered_reports[
        (filtered_reports['created_at'] >= pd.to_datetime(date_range[0])) &
        (filtered_reports['created_at'] <= pd.to_datetime(date_range[1]))
    ]
    if client_filter:
        filtered_reports = filtered_reports[filtered_reports['client'].isin(client_filter)]
    if organization_filter:
        filtered_reports = filtered_reports[
            filtered_reports['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)
        ]
    if company_filter:
        filtered_reports = filtered_reports[
            filtered_reports['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)
        ]
    if workstation_filter:
        filtered_reports = filtered_reports[
            filtered_reports['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(workstation_filter)
        ]
    if type_filter:
        filtered_reports = filtered_reports[filtered_reports['type'].isin(type_filter)]
    if file_filter:
        filtered_reports = filtered_reports[filtered_reports['name'].str.contains(file_filter, case=False, na=False)]

    st.write(f"Total: {len(filtered_reports)}")
    if not filtered_reports.empty:
        st.subheader("📊 Reports Overview")
        filtered_reports["organization_name"] = filtered_reports["organization"].apply(
            lambda x: x.get("name") if isinstance(x, dict) else None
        )
        filtered_reports["company_name"] = filtered_reports["company"].apply(
            lambda x: x.get("name") if isinstance(x, dict) else None
        )
        filtered_reports["workstation_name"] = filtered_reports["workstation"].apply(
            lambda x: x.get("name") if isinstance(x, dict) else None
        )
        filtered_reports["file_name"] = filtered_reports["file"].apply(
            lambda x: x.get("original_name") if isinstance(x, dict) else None
        )

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Total Reports", len(filtered_reports))
        col2.metric("Organizations", filtered_reports['organization_name'].nunique())
        col3.metric("Companies", filtered_reports['company_name'].nunique())
        col4.metric("Workstations", filtered_reports['workstation_name'].nunique())
        col5.metric("Active", filtered_reports[filtered_reports["is_active"] == 1].shape[0])
        col6.metric("Inactive", filtered_reports[filtered_reports["is_active"] == 0].shape[0])
        
        filtered_reports["status_icon"] = filtered_reports["is_active"].apply(lambda x: "✅" if x else "❌")

        display_df = filtered_reports[[
            "name", "type", "risk","status_icon" ,"client",
            "organization_name", "company_name", "workstation_name",
            "created_at", "updated_at", "file_name"
        ]]

        display_df = display_df.sort_values("created_at", ascending=False)

        st.dataframe(
            display_df[[
                "name", "type", "risk", "status_icon", "client",
                "organization_name", "company_name", "workstation_name",
                "file_name","created_at", "updated_at"
            ]],
            column_config={
                "name": "📝 Report Name",
                "type": "📂 Type",
                "risk":  "⚠️ Risk Level",
                "status_icon": "🔘 Active",
                "client": "👤 Client",
                "file_name": "📹 File",
                "organization_name": "🏢 Organization",
                "company_name": "🏭 Company",
                "workstation_name": "💻 Workstation",
                "created_at": st.column_config.DatetimeColumn(
                    "📅 Created At",
                    format="YYYY-MM-DD",
                ),
                "updated_at": st.column_config.DatetimeColumn(
                    "🔄 Updated At",
                    format="YYYY-MM-DD",
                ),
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Nenhum report encontrado para os filtros aplicados.")

    st.subheader("Resumo por risco")
    if not filtered_reports.empty:
        risk_summary = filtered_reports.groupby("risk").size().reset_index(name="count")
        st.bar_chart(risk_summary.set_index("risk"))

    st.subheader("Resumo por data")
    if not filtered_reports.empty:
    # Criar coluna de data
        filtered_reports["date_only"] = pd.to_datetime(filtered_reports["created_at"]).dt.date

        # Resumo por data
        date_summary = (
            filtered_reports
            .groupby(["type", "client", "date_only"])
            .size()
            .reset_index(name="count")
            .sort_values(["date_only"])
        )

        # Preparar display_df padronizado
        display_date_df = date_summary.copy()
        display_date_df.rename(columns={
            "type": "📂 Type",
            "client": "👤 Client",
            "date_only": "📅 Date",
            "count": "🔢 Count"
        }, inplace=True)

        # Exibir com column_config
        st.dataframe(
            display_date_df,
            column_config={
                "📂 Type": "📂 Type",
                "👤 Client": "👤 Client",
                "📅 Date": st.column_config.DatetimeColumn("📅 Date", format="YYYY-MM-DD"),
                "🔢 Count": "🔢 Count"
            },
            use_container_width=True,
            hide_index=True
        )
