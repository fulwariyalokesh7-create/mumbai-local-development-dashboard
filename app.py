"""
Mumbai Local Development Dashboard — Ward-Level Visualization
B.Sc Data Science Student Project
Framework: Flask (Python)
Backend: app.py
"""

import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, abort

import analysis

app = Flask(__name__)

# Base directory for relative file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "ward_development.csv")

def get_dataframe() -> pd.DataFrame:
    """
    Loads ward data. If MySQL is configured, attempts database query;
    otherwise falls back reliably to the clean CSV dataset.
    """
    mysql_host = os.environ.get("MYSQL_HOST")
    mysql_user = os.environ.get("MYSQL_USER")
    mysql_password = os.environ.get("MYSQL_PASSWORD")
    mysql_db = os.environ.get("MYSQL_DB", "mumbai_development")

    if mysql_host and mysql_user:
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database=mysql_db
            )
            query = "SELECT * FROM ward_development"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"[!] MySQL connection failed, falling back to CSV: {e}")

    # Fallback to local verified CSV
    return pd.read_csv(DATA_FILE)

# -------------------------------------------------------------
# Web Routes
# -------------------------------------------------------------

@app.route("/")
def index():
    """
    Main Dashboard View:
    Displays 5 KPI Cards, 6 Chart.js Visualizations, and Dynamic Insights.
    """
    df = get_dataframe()
    kpi = analysis.get_kpi_summary(df)
    insights = analysis.generate_data_driven_insights(df)
    
    # Sort wards by development score descending for chart 1
    df_sorted_score = df.sort_values(by="Development_Score", ascending=True)
    df_sorted_pop = df.sort_values(by="Population", ascending=False)
    
    chart_data = {
        "score_ranking": {
            "labels": [f"Ward {w}" for w in df_sorted_score["Ward_ID"]],
            "scores": df_sorted_score["Development_Score"].tolist(),
            "categories": df_sorted_score["Development_Category"].tolist()
        },
        "population": {
            "labels": [f"Ward {w}" for w in df_sorted_pop["Ward_ID"]],
            "values": df_sorted_pop["Population"].tolist(),
            "names": df_sorted_pop["Ward_Name"].tolist()
        },
        "infrastructure": {
            "labels": [f"Ward {w}" for w in df["Ward_ID"]],
            "water": df["Water_Supply_Coverage_pct"].tolist(),
            "drainage": df["Drainage_Coverage_pct"].tolist(),
            "waste": df["Waste_Collection_Coverage_pct"].tolist()
        },
        "facilities": {
            "labels": [f"Ward {w}" for w in df["Ward_ID"]],
            "schools": df["Schools_Count"].tolist(),
            "health": (df["Hospitals_Count"] + df["Health_Centres_Count"]).tolist(),
            "parks": df["Parks_Count"].tolist(),
            "toilets": df["Public_Toilets_Count"].tolist()
        },
        "categories": analysis.get_category_counts(df),
        "scatter": [
            {
                "x": int(row["Population_Density"]),
                "y": float(row["Development_Score"]),
                "ward": f"Ward {row['Ward_ID']} - {row['Ward_Name'].split(' - ')[0]}"
            }
            for _, row in df.iterrows()
        ]
    }
    
    zones = sorted(df["Zone"].unique().tolist())
    wards = df[["Ward_ID", "Ward_Name"]].to_dict(orient="records")
    
    return render_template(
        "index.html",
        kpi=kpi,
        insights=insights,
        chart_data=json.dumps(chart_data),
        zones=zones,
        wards=wards
    )

@app.route("/wards")
def wards_page():
    """
    Ward Data View:
    Displays searchable, sortable, and filterable table of all 24 wards.
    """
    df = get_dataframe()
    zone_filter = request.args.get("zone", "")
    cat_filter = request.args.get("category", "")
    
    filtered_df = df.copy()
    if zone_filter:
        filtered_df = filtered_df[filtered_df["Zone"] == zone_filter]
    if cat_filter:
        filtered_df = filtered_df[filtered_df["Development_Category"] == cat_filter]
        
    records = filtered_df.to_dict(orient="records")
    zones = sorted(df["Zone"].unique().tolist())
    categories = ["High Development", "Moderate Development", "Low Development"]
    
    return render_template(
        "wards.html",
        wards=records,
        zones=zones,
        categories=categories,
        selected_zone=zone_filter,
        selected_cat=cat_filter,
        total_count=len(records)
    )

@app.route("/ward/<ward_id>")
def ward_detail(ward_id):
    """
    Individual Ward Details View:
    Provides deep-dive profile for a specific ward and compares it against city averages.
    """
    df = get_dataframe()
    ward_id_clean = ward_id.strip().upper()
    
    # Check if ward exists
    match = df[df["Ward_ID"].str.upper() == ward_id_clean]
    if match.empty:
        # Try finding with slash if URL sanitized it
        match = df[df["Ward_ID"].str.upper() == ward_id_clean.replace("-", "/")]
        if match.empty:
            abort(404)
            
    ward = match.iloc[0].to_dict()
    
    # Calculate city benchmarks for comparison
    city_avg = {
        "Infrastructure_Score": round(float(df["Infrastructure_Score"].mean()), 1),
        "Health_Score": round(float(df["Health_Score"].mean()), 1),
        "Education_Score": round(float(df["Education_Score"].mean()), 1),
        "Sanitation_Score": round(float(df["Sanitation_Score"].mean()), 1),
        "Environment_Score": round(float(df["Environment_Score"].mean()), 1),
        "Public_Services_Score": round(float(df["Public_Services_Score"].mean()), 1),
        "Development_Score": round(float(df["Development_Score"].mean()), 1),
        "Population_Density": int(df["Population_Density"].mean())
    }
    
    # Calculate percentage differences
    diff_dev = round(ward["Development_Score"] - city_avg["Development_Score"], 1)
    
    comparison_radar = {
        "labels": ["Infrastructure", "Health", "Education", "Sanitation", "Environment", "Public Services"],
        "ward_scores": [
            ward["Infrastructure_Score"],
            ward["Health_Score"],
            ward["Education_Score"],
            ward["Sanitation_Score"],
            ward["Environment_Score"],
            ward["Public_Services_Score"]
        ],
        "city_avg": [
            city_avg["Infrastructure_Score"],
            city_avg["Health_Score"],
            city_avg["Education_Score"],
            city_avg["Sanitation_Score"],
            city_avg["Environment_Score"],
            city_avg["Public_Services_Score"]
        ]
    }
    
    all_wards = df[["Ward_ID", "Ward_Name"]].to_dict(orient="records")
    
    return render_template(
        "ward_detail.html",
        ward=ward,
        city_avg=city_avg,
        diff_dev=diff_dev,
        radar_data=json.dumps(comparison_radar),
        all_wards=all_wards
    )

@app.route("/compare")
def compare_page():
    """
    Ward Comparison View:
    Enables side-by-side comparison between any two Mumbai wards.
    """
    df = get_dataframe()
    ward_a_id = request.args.get("ward_a", "A")
    ward_b_id = request.args.get("ward_b", "M/East")
    
    # Get rows
    row_a = df[df["Ward_ID"] == ward_a_id]
    row_b = df[df["Ward_ID"] == ward_b_id]
    
    ward_a = row_a.iloc[0].to_dict() if not row_a.empty else df.iloc[0].to_dict()
    ward_b = row_b.iloc[0].to_dict() if not row_b.empty else df.iloc[16].to_dict()
    
    comparison_data = {
        "labels": ["Development Score", "Infrastructure", "Health", "Education", "Sanitation", "Environment", "Public Services"],
        "ward_a_scores": [
            ward_a["Development_Score"],
            ward_a["Infrastructure_Score"],
            ward_a["Health_Score"],
            ward_a["Education_Score"],
            ward_a["Sanitation_Score"],
            ward_a["Environment_Score"],
            ward_a["Public_Services_Score"]
        ],
        "ward_b_scores": [
            ward_b["Development_Score"],
            ward_b["Infrastructure_Score"],
            ward_b["Health_Score"],
            ward_b["Education_Score"],
            ward_b["Sanitation_Score"],
            ward_b["Environment_Score"],
            ward_b["Public_Services_Score"]
        ],
        "name_a": f"Ward {ward_a['Ward_ID']} ({ward_a['Ward_Name'].split(' - ')[0]})",
        "name_b": f"Ward {ward_b['Ward_ID']} ({ward_b['Ward_Name'].split(' - ')[0]})"
    }
    
    all_wards = df[["Ward_ID", "Ward_Name"]].to_dict(orient="records")
    
    return render_template(
        "compare.html",
        ward_a=ward_a,
        ward_b=ward_b,
        all_wards=all_wards,
        chart_data=json.dumps(comparison_data)
    )

@app.route("/analytics")
def analytics_page():
    """
    Analytics Deep-Dive View:
    Presents Population, Infrastructure, Public Facility, and Correlation statistics.
    """
    df = get_dataframe()
    kpi = analysis.get_kpi_summary(df)
    zone_stats = analysis.get_zone_summary(df)
    correlations = analysis.get_correlations(df)
    insights = analysis.generate_data_driven_insights(df)
    
    # Top 5 and Bottom 5 by score
    top_5 = df.sort_values(by="Development_Score", ascending=False).head(5).to_dict(orient="records")
    bottom_5 = df.sort_values(by="Development_Score", ascending=True).head(5).to_dict(orient="records")
    
    # Top 5 by Population & Density
    top_pop = df.sort_values(by="Population", ascending=False).head(5).to_dict(orient="records")
    top_density = df.sort_values(by="Population_Density", ascending=False).head(5).to_dict(orient="records")
    
    zone_chart = {
        "zones": [z["Zone"] for z in zone_stats],
        "dev_scores": [z["Avg_Dev_Score"] for z in zone_stats],
        "infra_scores": [z["Avg_Infra_Score"] for z in zone_stats],
        "health_scores": [z["Avg_Health_Score"] for z in zone_stats],
        "edu_scores": [z["Avg_Edu_Score"] for z in zone_stats]
    }
    
    return render_template(
        "analytics.html",
        kpi=kpi,
        zone_stats=zone_stats,
        correlations=correlations,
        insights=insights,
        top_5=top_5,
        bottom_5=bottom_5,
        top_pop=top_pop,
        top_density=top_density,
        zone_chart=json.dumps(zone_chart)
    )

@app.route("/about")
def about_page():
    """
    About Project & Viva Guide View:
    Documenting problem statement, data sources, formulas, normalization,
    ethical guidelines, viva script, limitations, and future scope.
    """
    return render_template("about.html")

# -------------------------------------------------------------
# JSON API Endpoints (For client-side AJAX updates)
# -------------------------------------------------------------

@app.route("/api/wards")
def api_wards():
    df = get_dataframe()
    zone = request.args.get("zone")
    category = request.args.get("category")
    
    filtered = df.copy()
    if zone:
        filtered = filtered[filtered["Zone"] == zone]
    if category:
        filtered = filtered[filtered["Development_Category"] == category]
        
    return jsonify(filtered.to_dict(orient="records"))

@app.route("/api/ward/<ward_id>")
def api_ward_detail(ward_id):
    df = get_dataframe()
    match = df[df["Ward_ID"].str.upper() == ward_id.strip().upper()]
    if match.empty:
        return jsonify({"error": "Ward not found"}), 404
    return jsonify(match.iloc[0].to_dict())

@app.route("/api/stats")
def api_stats():
    df = get_dataframe()
    return jsonify({
        "kpi": analysis.get_kpi_summary(df),
        "correlations": analysis.get_correlations(df),
        "categories": analysis.get_category_counts(df)
    })

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🚀 MUMBAI LOCAL DEVELOPMENT DASHBOARD IS LIVE!")
    print("  👉 Click or open in browser: http://127.0.0.1:5000")
    print("  👉 Or: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
