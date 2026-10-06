"""
Mumbai Local Development Dashboard
Script: data_processing.py
Role: Data Collection, Cleaning, Min-Max Normalization, and Development Score Calculation.

B.Sc Data Science Student Project
"""

import os
import pandas as pd
import numpy as np

def min_max_normalize(series: pd.Series) -> pd.Series:
    """
    Min-Max Normalization converts feature values to a standard 0 to 1 scale.
    Formula: (x - min) / (max - min)
    
    Why Normalization is needed:
    Population is in hundreds of thousands, while facility counts are in tens.
    Normalization brings every indicator into an equitable, comparable range.
    """
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series(0.5, index=series.index)
    return (series - min_val) / (max_val - min_val)

def process_mumbai_ward_data(file_path: str = None) -> pd.DataFrame:
    """
    Cleans raw civic inputs, calculates sub-scores, computes the composite
    Development Score, and assigns project-defined categories.
    """
    if file_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "data", "ward_development.csv")
        
    print(f"[*] Reading ward dataset from: {file_path}")
    df = pd.read_csv(file_path)
    
    # 1. Basic Cleaning & Verification
    print(f"[*] Dataset Shape: {df.shape[0]} wards, {df.shape[1]} columns")
    assert df["Ward_ID"].nunique() == 24, "Mumbai should contain 24 administrative municipal wards."
    
    # Ensure population density is computed accurately
    df["Population_Density"] = (df["Population"] / df["Area_sq_km"]).round().astype(int)
    
    # 2. Per-Capita & Density-Adjusted Features
    # Public amenities are normalized relative to population or area to ensure fair comparison
    schools_per_capita = (df["Schools_Count"] / df["Population"]) * 100000
    hospitals_per_capita = ((df["Hospitals_Count"] + df["Health_Centres_Count"]) / df["Population"]) * 100000
    toilets_per_capita = (df["Public_Toilets_Count"] / df["Population"]) * 10000
    parks_per_area = df["Parks_Count"] / df["Area_sq_km"]
    road_density = df["Road_Length_km"] / df["Area_sq_km"]
    
    # 3. Sub-indicator scores (0 to 100 scale)
    # Infrastructure: Water (35%), Drainage (35%), Waste (20%), Road Density (10%)
    norm_water = min_max_normalize(df["Water_Supply_Coverage_pct"])
    norm_drainage = min_max_normalize(df["Drainage_Coverage_pct"])
    norm_waste = min_max_normalize(df["Waste_Collection_Coverage_pct"])
    norm_road = min_max_normalize(road_density)
    
    df["Infrastructure_Score"] = (
        (norm_water * 0.35 + norm_drainage * 0.35 + norm_waste * 0.20 + norm_road * 0.10) * 100
    ).round(1)
    
    # Health Score: per-capita health institutions (60%) + raw capacity (40%)
    norm_hosp_capita = min_max_normalize(hospitals_per_capita)
    norm_hosp_raw = min_max_normalize(df["Hospitals_Count"] + df["Health_Centres_Count"])
    df["Health_Score"] = ((norm_hosp_capita * 0.60 + norm_hosp_raw * 0.40) * 100).round(1)
    
    # Education Score: per-capita schools (70%) + raw schools (30%)
    norm_school_capita = min_max_normalize(schools_per_capita)
    norm_school_raw = min_max_normalize(df["Schools_Count"])
    df["Education_Score"] = ((norm_school_capita * 0.70 + norm_school_raw * 0.30) * 100).round(1)
    
    # Sanitation Score: public toilets per capita (40%), drainage (30%), waste coverage (30%)
    norm_toilets = min_max_normalize(toilets_per_capita)
    df["Sanitation_Score"] = (
        (norm_toilets * 0.40 + norm_drainage * 0.30 + norm_waste * 0.30) * 100
    ).round(1)
    
    # Environment Score: green coverage (40%), parks density (30%), waste management (30%)
    norm_green = min_max_normalize(df["Green_Coverage_pct"])
    norm_parks = min_max_normalize(parks_per_area)
    norm_wm_score = min_max_normalize(df["Waste_Management_Score"])
    df["Environment_Score"] = (
        (norm_green * 0.40 + norm_parks * 0.30 + norm_wm_score * 0.30) * 100
    ).round(1)
    
    # Public Services Score: composite average of basic public service availability
    df["Public_Services_Score"] = (
        (df["Infrastructure_Score"] * 0.25 +
         df["Health_Score"] * 0.25 +
         df["Education_Score"] * 0.25 +
         df["Sanitation_Score"] * 0.25)
    ).round(1)
    
    # 4. Final Composite Development Score
    # Weights: Infra (25%), Health (20%), Education (20%), Sanitation (15%), Environment (10%), Public Services (10%)
    df["Development_Score"] = (
        df["Infrastructure_Score"] * 0.25 +
        df["Health_Score"] * 0.20 +
        df["Education_Score"] * 0.20 +
        df["Sanitation_Score"] * 0.15 +
        df["Environment_Score"] * 0.10 +
        df["Public_Services_Score"] * 0.10
    ).round(1)
    
    # 5. Project-Defined Development Categories
    # High: >= 65.0 | Moderate: 45.0 to 64.9 | Low: < 45.0
    def assign_category(score):
        if score >= 65.0:
            return "High Development"
        elif score >= 45.0:
            return "Moderate Development"
        else:
            return "Low Development"
            
    df["Development_Category"] = df["Development_Score"].apply(assign_category)
    
    # Save back to CSV
    df.to_csv(file_path, index=False)
    print(f"[✓] Successfully cleaned, normalized, and updated dataset at: {file_path}")
    print("[*] Category Counts:")
    print(df["Development_Category"].value_counts())
    return df

if __name__ == "__main__":
    process_mumbai_ward_data()
