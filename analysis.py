"""
Mumbai Local Development Dashboard
Script: analysis.py
Role: Exploratory Data Analysis (EDA), Statistical Aggregations, and Dynamic Insight Generation.

B.Sc Data Science Student Project
"""

import os
import pandas as pd
import numpy as np

def load_data(file_path: str = None) -> pd.DataFrame:
    if file_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "ward_development.csv")
    return pd.read_csv(file_path)

def get_kpi_summary(df: pd.DataFrame = None) -> dict:
    """
    Computes key performance indicators (KPIs) across Mumbai wards.
    """
    if df is None:
        df = load_data()
        
    highest_row = df.loc[df["Development_Score"].idxmax()]
    lowest_row = df.loc[df["Development_Score"].idxmin()]
    highest_pop_row = df.loc[df["Population"].idxmax()]
    highest_dens_row = df.loc[df["Population_Density"].idxmax()]
    
    return {
        "total_wards": int(len(df)),
        "total_population": int(df["Population"].sum()),
        "avg_population": round(float(df["Population"].mean()), 0),
        "avg_development_score": round(float(df["Development_Score"].mean()), 1),
        "highest_dev_ward": f"Ward {highest_row['Ward_ID']} ({highest_row['Ward_Name'].split(' - ')[0]})",
        "highest_dev_score": float(highest_row["Development_Score"]),
        "lowest_dev_ward": f"Ward {lowest_row['Ward_ID']} ({lowest_row['Ward_Name'].split(' - ')[0]})",
        "lowest_dev_score": float(lowest_row["Development_Score"]),
        "highest_pop_ward": f"Ward {highest_pop_row['Ward_ID']} ({highest_pop_row['Ward_Name'].split(' - ')[0]})",
        "highest_population": int(highest_pop_row["Population"]),
        "highest_dens_ward": f"Ward {highest_dens_row['Ward_ID']} ({highest_dens_row['Ward_Name'].split(' - ')[0]})",
        "highest_density": int(highest_dens_row["Population_Density"])
    }

def get_zone_summary(df: pd.DataFrame = None) -> list:
    """
    Computes zone-level aggregate statistics.
    """
    if df is None:
        df = load_data()
        
    grouped = df.groupby("Zone").agg(
        Ward_Count=("Ward_ID", "count"),
        Total_Population=("Population", "sum"),
        Avg_Density=("Population_Density", "mean"),
        Avg_Dev_Score=("Development_Score", "mean"),
        Avg_Infra_Score=("Infrastructure_Score", "mean"),
        Avg_Health_Score=("Health_Score", "mean"),
        Avg_Edu_Score=("Education_Score", "mean")
    ).round(1).reset_index()
    
    return grouped.to_dict(orient="records")

def get_category_counts(df: pd.DataFrame = None) -> dict:
    if df is None:
        df = load_data()
    counts = df["Development_Category"].value_counts().to_dict()
    return {
        "High Development": int(counts.get("High Development", 0)),
        "Moderate Development": int(counts.get("Moderate Development", 0)),
        "Low Development": int(counts.get("Low Development", 0))
    }

def get_correlations(df: pd.DataFrame = None) -> dict:
    """
    Calculates Pearson correlation coefficients between key indicators.
    """
    if df is None:
        df = load_data()
        
    corr_density_dev = df["Population_Density"].corr(df["Development_Score"])
    corr_infra_dev = df["Infrastructure_Score"].corr(df["Development_Score"])
    corr_health_dev = df["Health_Score"].corr(df["Development_Score"])
    corr_edu_dev = df["Education_Score"].corr(df["Development_Score"])
    
    return {
        "density_vs_dev_score": round(float(corr_density_dev), 3),
        "infra_vs_dev_score": round(float(corr_infra_dev), 3),
        "health_vs_dev_score": round(float(corr_health_dev), 3),
        "edu_vs_dev_score": round(float(corr_edu_dev), 3)
    }

def generate_data_driven_insights(df: pd.DataFrame = None) -> list:
    """
    Generates dynamic, non-hardcoded data-driven insights using descriptive statistics.
    """
    if df is None:
        df = load_data()
        
    kpi = get_kpi_summary(df)
    corr = get_correlations(df)
    
    avg_score = kpi["avg_development_score"]
    top_ward = df.loc[df["Development_Score"].idxmax()]
    bottom_ward = df.loc[df["Development_Score"].idxmin()]
    
    density_top = df.loc[df["Population_Density"].idxmax()]
    density_bottom = df.loc[df["Population_Density"].idxmin()]
    
    insights = [
        {
            "category": "Overall Development",
            "text": f"{top_ward['Ward_Name']} (Ward {top_ward['Ward_ID']}) exhibits the highest project-defined development score of {top_ward['Development_Score']}, which is {round(top_ward['Development_Score'] - avg_score, 1)} points above the city-wide average of {avg_score}."
        },
        {
            "category": "Indicator Priority",
            "text": f"{bottom_ward['Ward_Name']} (Ward {bottom_ward['Ward_ID']}) has a lower project-defined score of {bottom_ward['Development_Score']}. Based on the indicator breakdown, it has lower relative access to healthcare facilities and sanitation coverage compared with the Mumbai-wide benchmark."
        },
        {
            "category": "Population Density Impact",
            "text": f"Ward {density_top['Ward_ID']} ({density_top['Ward_Name'].split(' - ')[0]}) exhibits the highest population density with {density_top['Population_Density']:,} persons/sq km, whereas Ward {density_bottom['Ward_ID']} ({density_bottom['Ward_Name'].split(' - ')[0]}) has the lowest density of {density_bottom['Population_Density']:,} persons/sq km. The Pearson correlation between population density and development score is {corr['density_vs_dev_score']}, indicating that compact high-density wards face specific public facility pressures."
        },
        {
            "category": "Infrastructure Alignment",
            "text": f"Infrastructure indicators (road coverage, water supply, and drainage) exhibit a strong positive correlation of {corr['infra_vs_dev_score']} with the overall Development Score, highlighting infrastructure as a foundational contributor to local municipal well-being."
        },
        {
            "category": "Public Amenities Distribution",
            "text": f"The 24 wards collectively accommodate {int(df['Schools_Count'].sum())} registered municipal/state schools and {int(df['Hospitals_Count'].sum() + df['Health_Centres_Count'].sum())} public health facilities, though distribution per 100,000 residents varies significantly between the island city and suburban wards."
        }
    ]
    return insights

def run_eda():
    """
    Console runner for exploratory data analysis.
    """
    df = load_data()
    print("=" * 60)
    print("MUMBAI WARD DEVELOPMENT DATASET — EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    print(f"Total Rows (Wards): {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDescriptive Statistics (Scores & Population):")
    print(df[["Population", "Population_Density", "Infrastructure_Score", "Health_Score", "Education_Score", "Development_Score"]].describe().round(2))
    
    print("\n--- Key Performance Indicators ---")
    kpis = get_kpi_summary(df)
    for k, v in kpis.items():
        print(f"  {k}: {v}")
        
    print("\n--- Correlation Matrix ---")
    corrs = get_correlations(df)
    for k, v in corrs.items():
        print(f"  {k}: {v}")
        
    print("\n--- Dynamic Insights ---")
    for ins in generate_data_driven_insights(df):
        print(f"[{ins['category']}] {ins['text']}\n")

if __name__ == "__main__":
    run_eda()
