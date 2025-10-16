import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_action_plans_tab(action_plans_df, realtime_action_plans_df):
    st.subheader("📋 Realtime Action Plans")
    if not realtime_action_plans_df.empty:
        f1, f2, f3 = st.columns([1, 2, 2]) 
        with f1:
            client_filter = st.multiselect("Realtime Client:", options=realtime_action_plans_df['client'].dropna().unique(), key="realtime_action_plans_client")
        with f2:
            organization_filter = st.multiselect("Realtime Organization:", options=realtime_action_plans_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_action_plans_organization")
        with f3:
            company_filter = st.multiselect("Realtime Company:", options=realtime_action_plans_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(), key="realtime_action_plans_company")

        filtered_realtime_action_plans_df = realtime_action_plans_df.copy()
        if client_filter:
            filtered_realtime_action_plans_df = filtered_realtime_action_plans_df[filtered_realtime_action_plans_df['client'].isin(client_filter)]
        if organization_filter:
            filtered_realtime_action_plans_df = filtered_realtime_action_plans_df[filtered_realtime_action_plans_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)]
        if company_filter:
            filtered_realtime_action_plans_df = filtered_realtime_action_plans_df[filtered_realtime_action_plans_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)]

        unique_action_plans = filtered_realtime_action_plans_df.drop_duplicates(subset=['action_plan'], keep='first')
        total_action_plans = len(unique_action_plans)
        status_counts = unique_action_plans['action_plan'].apply(lambda x: x.get('status') if isinstance(x, dict) else None).value_counts()

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.metric("Total Action Plans", total_action_plans)
        with col2:
            st.metric("TO DO", status_counts.get('TO DO', 0))
        with col3:
            st.metric("IN PROGRESS", status_counts.get('DOING', 0))
        with col4:
            st.metric("COMPLETED", status_counts.get('DONE', 0))
        with col5:
            st.metric("Unique Clients", realtime_action_plans_df['client'].nunique())
        with col6:
            st.metric("Organizations", realtime_action_plans_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).nunique())
        with col7:
            st.metric("Companies", realtime_action_plans_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).nunique())
        realtime_display = filtered_realtime_action_plans_df.copy()
        realtime_display["organization_name"] = realtime_display["organization"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        realtime_display["company_name"] = realtime_display["company"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        realtime_display["workstation_name"] = realtime_display["workstation"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        realtime_display["action_plan_title"] = realtime_display["action_plan"].apply(lambda x: x.get("title") if isinstance(x, dict) else None)
        realtime_display["action_plan_status"] = realtime_display["action_plan"].apply(lambda x: x.get("status") if isinstance(x, dict) else None)
    else:
        st.info("No realtime action plans data available.")

    st.subheader("Filters")
    default_start = datetime.today() - timedelta(days=60)
    default_end = datetime.today()
    date_range = st.date_input(
        "Date interval:",
        [default_start, default_end],
        key="action_plans_date"
    )

    col_client, col_org, col_comp, col_ws, col_status = st.columns(5)
    with col_client:
        client_filter = st.multiselect("Client:", options=action_plans_df['client'].dropna().unique(), key="action_plans_client")
    with col_org:
        organization_filter = st.multiselect(
            "Organization:",
            options=action_plans_df['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="action_plans_organization"
        )
    with col_comp:
        company_filter = st.multiselect(
            "Company:",
            options=action_plans_df['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="action_plans_company"
        )
    with col_ws:
        workstation_filter = st.multiselect(
            "Workstation:",
            options=action_plans_df['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).dropna().unique(),
            key="action_plans_workstation"
        )
    with col_status:
        status_filter = st.multiselect(
            "Status:",
            options=action_plans_df['status'].dropna().unique(),
            key="action_plans_status"
        )

    title_filter = st.text_input("Action Plan Title:", key="action_plans_title")
    priority_filter = st.selectbox("Priority:", options=["All"] + list(action_plans_df['priority'].dropna().unique()), key="action_plans_priority")

    filtered_action_plans = action_plans_df.copy()
    if len(date_range) == 2:
        filtered_action_plans = filtered_action_plans[
            (filtered_action_plans['created_at'] >= pd.to_datetime(date_range[0])) &
            (filtered_action_plans['created_at'] <= pd.to_datetime(date_range[1]))
        ]
    if not len(date_range) == 2:
        st.warning("Selecione um intervalo de datas válido.")
        filtered_action_plans = pd.DataFrame()
    if client_filter:
        filtered_action_plans = filtered_action_plans[filtered_action_plans['client'].isin(client_filter)]
    if organization_filter:
        filtered_action_plans = filtered_action_plans[
            filtered_action_plans['organization'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(organization_filter)
        ]
    if company_filter:
        filtered_action_plans = filtered_action_plans[
            filtered_action_plans['company'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(company_filter)
        ]
    if workstation_filter:
        filtered_action_plans = filtered_action_plans[
            filtered_action_plans['workstation'].apply(lambda x: x.get('name') if isinstance(x, dict) else None).isin(workstation_filter)
        ]
    if status_filter:
        filtered_action_plans = filtered_action_plans[filtered_action_plans['status'].isin(status_filter)]
    if title_filter:
        filtered_action_plans = filtered_action_plans[filtered_action_plans['title'].str.contains(title_filter, case=False, na=False)]
    if priority_filter != "All":
        filtered_action_plans = filtered_action_plans[filtered_action_plans['priority'] == priority_filter]

    if not filtered_action_plans.empty:
        filtered_action_plans["organization_name"] = filtered_action_plans["organization"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        filtered_action_plans["company_name"] = filtered_action_plans["company"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        filtered_action_plans["workstation_name"] = filtered_action_plans["workstation"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
        filtered_action_plans["file_name"] = filtered_action_plans["file"].apply(lambda x: x.get("original_name") if isinstance(x, dict) else None)

        col1, col2, col3, col4, col5 = st.columns(5)
        total_action_plans = len(filtered_action_plans)
        completed_action_plans = len(filtered_action_plans[filtered_action_plans['status'] == 'COMPLETED'])
        in_progress_action_plans = len(filtered_action_plans[filtered_action_plans['status'] == 'IN PROGRESS'])
        to_do_action_plans = len(filtered_action_plans[filtered_action_plans['status'] == 'TO DO'])
        avg_priority = filtered_action_plans['priority'].mean() if not filtered_action_plans['priority'].empty else 0
        
        col1.metric("Total Action Plans", total_action_plans)
        col2.metric("Completed", completed_action_plans)
        col3.metric("In Progress", in_progress_action_plans)
        col4.metric("To Do", to_do_action_plans)
        col5.metric("Avg Priority", round(avg_priority, 2) if avg_priority > 0 else "N/A")

        filtered_action_plans["priority_converted"] = filtered_action_plans["priority"].apply(lambda x: "LOW" if x == 1 else "MEDIUM" if x == 2 else "HIGH" if x == 3 else "VERY_HIGH" if x == 4 else "")

        display_df = filtered_action_plans[[
            "title", "description", "status", "priority_converted", "due_date",
            "client", "organization_name", "company_name", "workstation_name", "file_name",
            "created_at", "updated_at", "completed_at"
        ]]

        display_df = display_df.sort_values("created_at", ascending=False)

        st.dataframe(
            display_df,
            column_config={
                "title": "📋 Title",
                "description": "📝 Description",
                "status": "🔘 Status",
                "priority_converted": "⭐ Priority",
                "due_date": st.column_config.DatetimeColumn("📅 Due Date", format="YYYY-MM-DD"),
                "client": "👤 Client",
                "organization_name": "🏢 Organization",
                "company_name": "🏭 Company",
                "workstation_name": "💻 Workstation",
                "file_name": "📹 File",
                "created_at": st.column_config.DatetimeColumn("📅 Created At", format="YYYY-MM-DD"),
                "updated_at": st.column_config.DatetimeColumn("📅 Updated At", format="YYYY-MM-DD"),
                "completed_at": st.column_config.DatetimeColumn("✅ Completed At", format="YYYY-MM-DD"),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No action plans found for applied filters.")

    st.subheader("Status Resume")
    if not filtered_action_plans.empty:
        status_summary = filtered_action_plans.groupby("status").size().reset_index(name="count")
        st.bar_chart(status_summary.set_index("status"))

    st.subheader("Priority Distribution")
    if not filtered_action_plans.empty:
        priority_summary = filtered_action_plans.groupby("priority").size().reset_index(name="count")
        if not priority_summary.empty:
            st.bar_chart(priority_summary.set_index("priority"))

    st.subheader("Data Resume")
    if not filtered_action_plans.empty:
        filtered_action_plans["date_only"] = pd.to_datetime(filtered_action_plans["created_at"]).dt.date

        date_summary = (
            filtered_action_plans.groupby(["client", "date_only"])
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

    st.subheader("Completion Timeline")
    if not filtered_action_plans.empty and 'completed_at' in filtered_action_plans.columns:
        completed_plans = filtered_action_plans[filtered_action_plans['status'] == 'DONE'].copy()
        if not completed_plans.empty:
            completed_plans["completion_date"] = pd.to_datetime(completed_plans["completed_at"]).dt.date
            
            completion_summary = (
                completed_plans.groupby(["client", "completion_date"])
                .size()
                .reset_index(name="count")
                .sort_values(["completion_date"])
            )
            
            completion_daily = completion_summary.groupby("completion_date")["count"].sum()
            st.bar_chart(completion_daily)
