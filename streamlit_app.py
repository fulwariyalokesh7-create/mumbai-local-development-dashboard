"""
Mumbai Local Development Dashboard — Ward-Level Visualization
Streamlit Web Application
B.Sc Data Science Student Project
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="Mumbai Local Development Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #1e3a8a;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-box {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Data Loading & Caching
# -------------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "ward_development.csv")
    df = pd.read_csv(file_path)
    return df

df = load_data()

# -------------------------------------------------------------
# Helper Calculations
# -------------------------------------------------------------
avg_score = round(df["Development_Score"].mean(), 1)
total_pop = int(df["Population"].sum())
top_ward = df.loc[df["Development_Score"].idxmax()]
lowest_ward = df.loc[df["Development_Score"].idxmin()]
density_top = df.loc[df["Population_Density"].idxmax()]
density_bottom = df.loc[df["Population_Density"].idxmin()]

corr_density = round(df["Population_Density"].corr(df["Development_Score"]), 3)
corr_infra = round(df["Infrastructure_Score"].corr(df["Development_Score"]), 3)
corr_health = round(df["Health_Score"].corr(df["Development_Score"]), 3)
corr_edu = round(df["Education_Score"].corr(df["Development_Score"]), 3)

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
st.sidebar.markdown("## 🏙️ Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "📋 Ward Data Directory", "🔍 Ward Profile Details", "⚖️ Ward Comparison", "📈 Analytics & Insights", "ℹ️ About & Viva Guide"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Project Info")
st.sidebar.info(
    "**Mumbai Local Development Dashboard**\n\n"
    "B.Sc Data Science Student Project\n\n"
    "Analyzes 24 Administrative Municipal Wards across Infrastructure, Health, Education & Sanitation."
)

# -------------------------------------------------------------
# PAGE 1: DASHBOARD
# -------------------------------------------------------------
if page == "📊 Dashboard":
    st.markdown('<div class="main-title">Mumbai Local Development Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Ward-Level Data Visualization & Development Insights across 24 Municipal Wards</div>', unsafe_allow_html=True)

    # KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Wards", len(df), "7 Admin Zones")
    with col2:
        st.metric("Total Population", f"{total_pop / 1000000:.2f} M", f"{total_pop:,} residents")
    with col3:
        st.metric("Avg Dev Score", f"{avg_score} / 100", "City Benchmark")
    with col4:
        st.metric("Top Score Ward", f"Ward {top_ward['Ward_ID']}", f"{top_ward['Development_Score']} (High)")
    with col5:
        st.metric("Lowest Score Ward", f"Ward {lowest_ward['Ward_ID']}", f"{lowest_ward['Development_Score']} (Priority)")

    st.markdown("---")

    # Filter Row
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        selected_zone = st.selectbox("Filter by Administrative Zone", ["All Zones"] + sorted(df["Zone"].unique().tolist()))
    with fcol2:
        selected_category = st.selectbox("Filter by Development Category", ["All Categories", "High Development", "Moderate Development", "Low Development"])

    filtered_df = df.copy()
    if selected_zone != "All Zones":
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["Development_Category"] == selected_category]

    # Row 1 Charts: Development Score Ranking & Category Distribution
    r1_col1, r1_col2 = st.columns([7, 5])
    
    with r1_col1:
        st.subheader("Chart 1 — Wards Ranked by Development Score")
        df_sorted_score = filtered_df.sort_values(by="Development_Score", ascending=True)
        color_map = {
            "High Development": "#16a34a",
            "Moderate Development": "#d97706",
            "Low Development": "#dc2626"
        }
        fig_score = px.bar(
            df_sorted_score,
            x="Development_Score",
            y="Ward_ID",
            orientation="h",
            color="Development_Category",
            color_discrete_map=color_map,
            hover_data=["Ward_Name", "Zone", "Population", "Population_Density"],
            labels={"Ward_ID": "Ward", "Development_Score": "Development Score (0-100)"},
            height=500
        )
        fig_score.update_layout(margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_score, use_container_width=True)

    with r1_col2:
        st.subheader("Chart 5 — Development Category Share")
        cat_counts = filtered_df["Development_Category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_pie = px.pie(
            cat_counts,
            values="Count",
            names="Category",
            color="Category",
            color_discrete_map=color_map,
            hole=0.45,
            height=240
        )
        fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("💡 Dynamic Data-Driven Insights")
        st.markdown(f"""
        <div class="insight-box">
            <strong>Top Performing:</strong> {top_ward['Ward_Name']} (Ward {top_ward['Ward_ID']}) has the highest score of <strong>{top_ward['Development_Score']}</strong>, which is <strong>{round(top_ward['Development_Score'] - avg_score, 1)}</strong> points above the Mumbai average.
        </div>
        <div class="insight-box">
            <strong>Priority Need:</strong> {lowest_ward['Ward_Name']} (Ward {lowest_ward['Ward_ID']}) has a score of <strong>{lowest_ward['Development_Score']}</strong> with lower relative healthcare and sanitation facility coverage.
        </div>
        <div class="insight-box">
            <strong>Infrastructure Correlation:</strong> Infrastructure score has a <strong>+{corr_infra}</strong> positive correlation with overall development.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Row 2 Charts: Population by Ward & Scatter Plot
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.subheader("Chart 2 — Population by Ward")
        fig_pop = px.bar(
            filtered_df.sort_values(by="Population", ascending=False),
            x="Ward_ID",
            y="Population",
            color_discrete_sequence=["#3b82f6"],
            hover_data=["Ward_Name", "Zone", "Area_sq_km"],
            labels={"Ward_ID": "Ward", "Population": "Census Population"},
            height=360
        )
        st.plotly_chart(fig_pop, use_container_width=True)

    with r2_col2:
        st.subheader("Chart 6 — Population Density vs. Development Score")
        fig_scatter = px.scatter(
            df,
            x="Population_Density",
            y="Development_Score",
            color="Development_Category",
            color_discrete_map=color_map,
            size="Population",
            hover_name="Ward_Name",
            hover_data=["Ward_ID", "Zone", "Area_sq_km"],
            labels={"Population_Density": "Population Density (persons/km²)", "Development_Score": "Development Score (0-100)"},
            height=360
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Row 3 Charts: Infrastructure Coverage & Public Facilities
    r3_col1, r3_col2 = st.columns(2)
    with r3_col1:
        st.subheader("Chart 3 — Infrastructure Coverage (%)")
        infra_melted = filtered_df.melt(
            id_vars=["Ward_ID"],
            value_vars=["Water_Supply_Coverage_pct", "Drainage_Coverage_pct", "Waste_Collection_Coverage_pct"],
            var_name="Indicator",
            value_name="Percentage"
        )
        fig_infra = px.bar(
            infra_melted,
            x="Ward_ID",
            y="Percentage",
            color="Indicator",
            barmode="group",
            height=360
        )
        st.plotly_chart(fig_infra, use_container_width=True)

    with r3_col2:
        st.subheader("Chart 4 — Public Facilities Distribution")
        filtered_df["Health_Institutions"] = filtered_df["Hospitals_Count"] + filtered_df["Health_Centres_Count"]
        fac_melted = filtered_df.melt(
            id_vars=["Ward_ID"],
            value_vars=["Schools_Count", "Health_Institutions", "Parks_Count", "Public_Toilets_Count"],
            var_name="Facility",
            value_name="Count"
        )
        fig_fac = px.bar(
            fac_melted,
            x="Ward_ID",
            y="Count",
            color="Facility",
            barmode="group",
            height=360
        )
        st.plotly_chart(fig_fac, use_container_width=True)

# -------------------------------------------------------------
# PAGE 2: WARD DATA DIRECTORY
# -------------------------------------------------------------
elif page == "📋 Ward Data Directory":
    st.markdown('<div class="main-title">Mumbai Municipal Wards Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Complete 24-Ward dataset with demographic, infrastructure and scoring metrics</div>', unsafe_allow_html=True)

    search_query = st.text_input("🔍 Search Ward Name or Locality", placeholder="Type e.g. Bandra, Colaba, Andheri...")
    display_df = df.copy()

    if search_query:
        display_df = display_df[
            display_df["Ward_Name"].str.contains(search_query, case=False, na=False) |
            display_df["Ward_ID"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(
        display_df[[
            "Ward_ID", "Ward_Name", "Zone", "Population", "Area_sq_km",
            "Population_Density", "Infrastructure_Score", "Health_Score",
            "Education_Score", "Sanitation_Score", "Environment_Score",
            "Development_Score", "Development_Category"
        ]],
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=csv_data,
        file_name="mumbai_ward_development.csv",
        mime="text/csv"
    )

# -------------------------------------------------------------
# PAGE 3: WARD PROFILE DETAILS
# -------------------------------------------------------------
elif page == "🔍 Ward Profile Details":
    st.markdown('<div class="main-title">Ward Profile Deep-Dive</div>', unsafe_allow_html=True)

    ward_choices = [f"Ward {w['Ward_ID']} — {w['Ward_Name']}" for _, w in df.iterrows()]
    selected_choice = st.selectbox("Select Ward to Inspect", ward_choices)
    selected_id = selected_choice.split(" — ")[0].replace("Ward ", "").strip()
    ward = df[df["Ward_ID"] == selected_id].iloc[0]

    pcol1, pcol2, pcol3 = st.columns(3)
    with pcol1:
        st.markdown(f"### Ward {ward['Ward_ID']} Overview")
        st.write(f"**Locality:** {ward['Ward_Name']}")
        st.write(f"**Zone:** {ward['Zone']}")
        st.write(f"**Population:** {ward['Population']:,}")
        st.write(f"**Area:** {ward['Area_sq_km']} km²")
        st.write(f"**Density:** {ward['Population_Density']:,} persons/km²")
        st.write(f"**Road Length:** {ward['Road_Length_km']} km")

    with pcol2:
        st.markdown("### Overall Evaluation")
        st.metric("Development Score", f"{ward['Development_Score']} / 100", f"{round(ward['Development_Score'] - avg_score, 1)} vs City Avg")
        st.write(f"**Category:** `{ward['Development_Category']}`")
        st.write(f"**City Average Score:** `{avg_score}`")

    with pcol3:
        st.markdown("### Public Amenities")
        st.write(f"🏫 **Schools:** {ward['Schools_Count']}")
        st.write(f"🏥 **Health Institutions:** {ward['Hospitals_Count'] + ward['Health_Centres_Count']}")
        st.write(f"🚻 **Public Toilets:** {ward['Public_Toilets_Count']}")
        st.write(f"🌳 **Parks & Gardens:** {ward['Parks_Count']}")
        st.write(f"🌱 **Green Coverage:** {ward['Green_Coverage_pct']}%")

    st.markdown("---")
    st.subheader("Benchmark Comparison: Selected Ward vs. Mumbai City Average")

    categories = ["Infrastructure", "Health", "Education", "Sanitation", "Environment", "Public Services"]
    ward_vals = [ward["Infrastructure_Score"], ward["Health_Score"], ward["Education_Score"], ward["Sanitation_Score"], ward["Environment_Score"], ward["Public_Services_Score"]]
    city_vals = [
        round(df["Infrastructure_Score"].mean(), 1),
        round(df["Health_Score"].mean(), 1),
        round(df["Education_Score"].mean(), 1),
        round(df["Sanitation_Score"].mean(), 1),
        round(df["Environment_Score"].mean(), 1),
        round(df["Public_Services_Score"].mean(), 1)
    ]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=ward_vals,
        theta=categories,
        fill='toself',
        name=f"Ward {ward['Ward_ID']}"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=city_vals,
        theta=categories,
        fill='toself',
        name="Mumbai City Average",
        line=dict(dash='dash')
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=450
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# -------------------------------------------------------------
# PAGE 4: WARD COMPARISON
# -------------------------------------------------------------
elif page == "⚖️ Ward Comparison":
    st.markdown('<div class="main-title">Side-by-Side Ward Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Compare two Mumbai wards across all demographic, civic and scoring parameters</div>', unsafe_allow_html=True)

    ward_options = [f"Ward {w['Ward_ID']} — {w['Ward_Name'].split(' - ')[0]}" for _, w in df.iterrows()]
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        pick_a = st.selectbox("Select Ward A", ward_options, index=0)
    with ccol2:
        pick_b = st.selectbox("Select Ward B", ward_options, index=16)

    id_a = pick_a.split(" — ")[0].replace("Ward ", "").strip()
    id_b = pick_b.split(" — ")[0].replace("Ward ", "").strip()

    row_a = df[df["Ward_ID"] == id_a].iloc[0]
    row_b = df[df["Ward_ID"] == id_b].iloc[0]

    st.markdown("### Comparison Overview")
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.info(f"**Ward {row_a['Ward_ID']} — {row_a['Ward_Name']}**\n\n"
                f"- **Score:** {row_a['Development_Score']} ({row_a['Development_Category']})\n"
                f"- **Population:** {row_a['Population']:,}\n"
                f"- **Density:** {row_a['Population_Density']:,} / km²")
    with mcol2:
        st.success(f"**Ward {row_b['Ward_ID']} — {row_b['Ward_Name']}**\n\n"
                   f"- **Score:** {row_b['Development_Score']} ({row_b['Development_Category']})\n"
                   f"- **Population:** {row_b['Population']:,}\n"
                   f"- **Density:** {row_b['Population_Density']:,} / km²")

    # Bar chart comparison
    ind_labels = ["Development Score", "Infrastructure", "Health", "Education", "Sanitation", "Environment", "Public Services"]
    scores_a = [row_a["Development_Score"], row_a["Infrastructure_Score"], row_a["Health_Score"], row_a["Education_Score"], row_a["Sanitation_Score"], row_a["Environment_Score"], row_a["Public_Services_Score"]]
    scores_b = [row_b["Development_Score"], row_b["Infrastructure_Score"], row_b["Health_Score"], row_b["Education_Score"], row_b["Sanitation_Score"], row_b["Environment_Score"], row_b["Public_Services_Score"]]

    fig_comp = go.Figure(data=[
        go.Bar(name=f"Ward {row_a['Ward_ID']}", x=ind_labels, y=scores_a, marker_color='#2563eb'),
        go.Bar(name=f"Ward {row_b['Ward_ID']}", x=ind_labels, y=scores_b, marker_color='#0d9488')
    ])
    fig_comp.update_layout(barmode='group', height=400, yaxis=dict(range=[0, 100], title="Score (0-100)"))
    st.plotly_chart(fig_comp, use_container_width=True)

# -------------------------------------------------------------
# PAGE 5: ANALYTICS & INSIGHTS
# -------------------------------------------------------------
elif page == "📈 Analytics & Insights":
    st.markdown('<div class="main-title">Civic Analytics & Correlation Matrix</div>', unsafe_allow_html=True)

    acol1, acol2, acol3, acol4 = st.columns(4)
    with acol1:
        st.metric("Density vs Score", f"{corr_density}", "Pearson r")
    with acol2:
        st.metric("Infra vs Score", f"+{corr_infra}", "Strong positive")
    with acol3:
        st.metric("Health vs Score", f"+{corr_health}", "Moderate positive")
    with acol4:
        st.metric("Education vs Score", f"+{corr_edu}", "Moderate positive")

    st.markdown("---")
    st.subheader("Zone-Level Development Aggregations")
    zone_agg = df.groupby("Zone").agg(
        Wards=("Ward_ID", "count"),
        Total_Population=("Population", "sum"),
        Avg_Density=("Population_Density", "mean"),
        Avg_Score=("Development_Score", "mean"),
        Avg_Infra=("Infrastructure_Score", "mean"),
        Avg_Health=("Health_Score", "mean"),
        Avg_Edu=("Education_Score", "mean")
    ).round(1).reset_index()

    st.dataframe(zone_agg, use_container_width=True, hide_index=True)

    st.markdown("---")
    tcol1, tcol2 = st.columns(2)
    with tcol1:
        st.subheader("Top 5 Wards by Score")
        st.dataframe(
            df.sort_values(by="Development_Score", ascending=False).head(5)[["Ward_ID", "Ward_Name", "Zone", "Development_Score", "Development_Category"]],
            use_container_width=True, hide_index=True
        )
    with tcol2:
        st.subheader("Priority Focus Wards (Lower Scores)")
        st.dataframe(
            df.sort_values(by="Development_Score", ascending=True).head(5)[["Ward_ID", "Ward_Name", "Zone", "Development_Score", "Development_Category"]],
            use_container_width=True, hide_index=True
        )

# -------------------------------------------------------------
# PAGE 6: ABOUT & VIVA GUIDE
# -------------------------------------------------------------
elif page == "ℹ️ About & Viva Guide":
    st.markdown('<div class="main-title">About the Project & Viva Voce Guide</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🎯 1. Project Overview & Problem Statement
    The **Mumbai Local Development Dashboard** is an academic Data Science web application built to analyze, benchmark, and visualize municipal development indicators across Greater Mumbai's **24 administrative municipal wards**.

    ### 📚 2. Official Data Sources
    - **Demographics & Population:** District Census Handbook — Mumbai & Suburban (Census of India 2011).
    - **Civic Infrastructure & Environment:** Environment Status Reports (ESR) — Brihanmumbai Municipal Corporation (BMC).
    - **Public Facilities:** Status of Civic Issues Reports — Praja Foundation & Open Municipal releases.

    ### 📐 3. Mathematical Normalization & Scoring Formula
    Because raw indicators have different scales (population is in hundreds of thousands, facility counts in tens), **Min-Max Normalization** is applied:
    $$\\text{Normalized Value} = \\frac{\\text{Value} - \\text{Minimum}}{\\text{Maximum} - \\text{Minimum}}$$

    The **Development Score (0 to 100)** is computed as a weighted linear combination:
    $$\\text{Development Score} = 0.25 \\times \\text{Infra} + 0.20 \\times \\text{Health} + 0.20 \\times \\text{Education} + 0.15 \\times \\text{Sanitation} + 0.10 \\times \\text{Environment} + 0.10 \\times \\text{Public Services}$$

    ### 🎓 4. 5-Minute Viva Voce Cheat Sheet
    - **Why normalize?** Different indicators have different scales; normalization brings them into a comparable 0 to 1 range.
    - **Why did we build this?** To visualize local disparities and understand how public facility access varies across Mumbai.
    - **Is this official?** No, it is a project-defined analytical model for educational study.
    """)

def main():
    pass

if __name__ == "__main__":
    main()
