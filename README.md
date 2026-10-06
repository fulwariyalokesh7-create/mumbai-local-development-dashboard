# 🏙️ Mumbai Local Development Dashboard — Ward-Level Visualization

> **Academic Level:** B.Sc Data Science (First Serious Data Science Project)  
> **Domain:** Urban Analytics, Civic Informatics & Public Policy  
> **Tech Stack:** Python, Pandas, NumPy, Flask, MySQL, Chart.js, Bootstrap 5, Excel, Power BI  

---

## 📌 1. Project Overview

The **Mumbai Local Development Dashboard** is an end-to-end Data Science project that evaluates, benchmarks, and visualizes civic infrastructure and public service availability across all **24 administrative municipal wards** of Mumbai (Wards A to T).

Instead of treating Mumbai as a single aggregate number, this project breaks down civic indicators at the ward level to reveal how infrastructure, healthcare, education, sanitation, and environment vary between the historic Island City and the expanding Eastern and Western suburban belts.

---

## 🎯 2. Problem Statement & Objectives

### Problem Statement
Municipal reports and census data for Greater Mumbai are published in disparate PDFs, statistical abstracts, and civic releases. Citizens, researchers, and urban planners lack a beginner-friendly, transparent analytical tool to compare ward-level living conditions and identify areas requiring public facility intervention.

### Core Objectives
1. **Data Collection & Integration:** Gather authentic ward-level demographic, infrastructure, and public amenity metrics.
2. **Data Cleaning & Standardization:** Handle missing values, verify data types, and eliminate duplicate records.
3. **Feature Engineering:** Calculate per-capita indicators (e.g., schools and healthcare institutions per 100,000 residents; public toilets per 10,000 residents; road density per sq km).
4. **Min-Max Normalization:** Standardize indicators across diverse units into a common $[0, 1]$ scale.
5. **Composite Scoring:** Formulate an explainable, weighted **Development Score (0 to 100)**.
6. **Interactive Visualization:** Build an accessible web dashboard featuring KPI cards, 6 charts, side-by-side ward comparison, and dynamic data-driven insights.
7. **Database & Business Intelligence:** Model the dataset in MySQL and design reporting workflows for Microsoft Excel and Power BI.

---

## 📂 3. Project Directory Structure

```text
Mumbai-Development-Dashboard/
│
├── app.py                      # Flask web application & API routes
├── analysis.py                 # Exploratory Data Analysis & dynamic insights generator
├── data_processing.py          # Data cleaning, Min-Max normalization & scoring pipeline
├── requirements.txt            # Python library dependencies
├── README.md                   # Comprehensive project documentation & viva guide
│
├── data/
│   └── ward_development.csv    # Cleaned, normalized 24-ward Mumbai dataset
│
├── database/
│   └── database.sql            # MySQL table schema, data inserts & viva queries
│
├── templates/                  # Responsive HTML5 templates (Bootstrap 5)
│   ├── base.html               # Shared navbar, header & footer layout
│   ├── index.html              # Main dashboard with KPI cards & 6 charts
│   ├── wards.html              # Filterable and searchable ward table
│   ├── ward_detail.html        # Single ward profile with radar benchmark
│   ├── compare.html            # Side-by-side dual ward comparison
│   ├── analytics.html          # Statistical distributions, rankings & correlations
│   └── about.html              # Project methodology & viva preparation guide
│
└── static/
    ├── css/
    │   └── style.css           # Clean, professional styling
    └── js/
        └── script.js           # Chart.js visualization configurations & search logic
```

---

## 📊 4. Official Data Sources & Attribution

All baseline metrics are grounded in authentic, published public records:

| Indicator Category | Official Source | Publishing Agency |
| :--- | :--- | :--- |
| **Ward Names, Area & Population** | *District Census Handbook — Mumbai & Mumbai Suburban (2011)* | Census of India, Ministry of Home Affairs |
| **Ward Administrative Boundaries** | *MCGM 24 Administrative Wards Portal* | Municipal Corporation of Greater Mumbai (BMC) |
| **Roads, Water & Drainage** | *Environment Status Report (ESR)* | Brihanmumbai Municipal Corporation (BMC) |
| **Schools, Health & Toilets** | *White Paper on the Status of Civic Issues in Mumbai* | Praja Foundation & MCGM Open Data Releases |

> **Ethical Presentation Note:**  
> This project strictly avoids biased labels such as *"bad"* or *"poor area."* Instead, neutral language is used: *"This ward exhibits a lower project-defined development score based on selected indicators."* The Development Score is an academic analytical construct, not an official government ranking.

---

## 📐 5. Data Science Methodology

### Step 1: Normalization (Why & How)
Public amenities are measured in vastly different units:
- Population ranges from **127,290** (Ward B) to **941,366** (Ward P/North).
- Area ranges from **1.78 km²** (Ward C) to **64.00 km²** (Ward S).
- Facility counts range from **6** to **490**.

If we summed raw numbers directly, population would completely drown out hospital and school counts. We apply **Min-Max Normalization** to bring all metrics into a comparable 0 to 1 range:

$$\text{Normalized Value} = \frac{\text{Value} - \text{Minimum}}{\text{Maximum} - \text{Minimum}}$$

### Step 2: Sub-Indicator Scores (Scaled 0 to 100)
1. **Infrastructure Score:** Water coverage (35%), Drainage coverage (35%), Solid waste collection (20%), Road density (10%).
2. **Health Score:** Health facilities per 100k population (60%) + raw facility count (40%).
3. **Education Score:** Schools per 100k population (70%) + raw schools count (30%).
4. **Sanitation Score:** Public toilets per 10k population (40%) + Drainage (30%) + Waste collection (30%).
5. **Environment Score:** Green space percentage (40%) + Parks density (30%) + Waste management rating (30%).
6. **Public Services Score:** Arithmetic average across all core public amenities.

### Step 3: Composite Development Score Formula
The overall score is calculated as a clear, weighted linear combination:

$$\text{Development Score} = (0.25 \times \text{Infra}) + (0.20 \times \text{Health}) + (0.20 \times \text{Education}) + (0.15 \times \text{Sanitation}) + (0.10 \times \text{Environment}) + (0.10 \times \text{Public Services})$$

### Step 4: Project-Defined Development Categories
- **High Development:** Score $\ge 65.0$ (Balanced infrastructure, well-established civic services)
- **Moderate Development:** $45.0 \le \text{Score} < 65.0$ (Adequate services with room for targeted expansion)
- **Low Development:** $\text{Score} < 45.0$ (High population pressure and priority need for civic amenities)

---

## 📈 6. Dashboard & Interactive Visualizations

The dashboard (`/`) presents 6 targeted visualizations using **Chart.js**:

1. **Chart 1 — Development Score by Ward:** Horizontal bar chart displaying all 24 wards ranked by composite score, color-coded by development category.
2. **Chart 2 — Population by Ward:** Bar chart highlighting the demographic scale from island city wards to sprawling suburban centers.
3. **Chart 3 — Infrastructure Comparison:** Grouped bar chart comparing water supply, drainage, and waste collection percentages.
4. **Chart 4 — Public Facilities Distribution:** Multi-dataset chart showing schools, health centers, and public parks.
5. **Chart 5 — Development Categories:** Doughnut chart illustrating the proportion of wards in High, Moderate, and Low categories.
6. **Chart 6 — Population Density vs. Development Score:** Scatter plot assessing whether high-density wards face infrastructure pressures.

---

## 🗄️ 7. MySQL Database & Analytical Queries

The SQL script is located at [`database/database.sql`](database/database.sql).

### Sample Viva SQL Queries:
```sql
-- 1. City-Wide Average Development Score
SELECT ROUND(AVG(Development_Score), 2) AS Avg_Score FROM ward_development;

-- 2. Top 5 Wards by Development Score
SELECT Ward_ID, Ward_Name, Zone, Development_Score 
FROM ward_development 
ORDER BY Development_Score DESC 
LIMIT 5;

-- 3. Zone-Wise Development Summary
SELECT Zone, COUNT(*) AS Wards, ROUND(AVG(Development_Score), 2) AS Avg_Score
FROM ward_development
GROUP BY Zone
ORDER BY Avg_Score DESC;
```

---

## 📑 8. Microsoft Excel & Power BI Integration

### Microsoft Excel:
1. Open [`data/ward_development.csv`](data/ward_development.csv) in Excel.
2. Use **Conditional Formatting** (Data Bars or 3-Color Scales) on `Development_Score`.
3. Insert a **Pivot Table**:
   - Rows: `Zone`
   - Values: `Average of Development_Score`, `Sum of Population`.
4. Create a **Clustered Column Pivot Chart** to present zone-level differences.

### Microsoft Power BI:
1. **Import:** `Get Data` → `Text/CSV` → Select `ward_development.csv`.
2. **KPI Cards:** Add Card visuals for `Total Wards`, `Total Population`, and `Average Development Score`.
3. **Bar Charts:** Create clustered bar charts for `Development Score by Ward` and `Population by Ward`.
4. **Doughnut Chart:** Visualize `Development_Category` counts.
5. **Scatter Chart:** Set X-axis to `Population_Density`, Y-axis to `Development_Score`, and Details to `Ward_Name`.
6. **Slicers:** Add interactive slicers for `Zone` and `Development_Category`.

---

## 🚀 9. Step-by-Step Installation & Run Guide

### Step 1: Open Terminal in Project Directory
```powershell
cd Mumbai-Development-Dashboard
```

### Step 2: Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Required Libraries
```powershell
pip install -r requirements.txt
```

### Step 4: Run Data Processing & Exploratory Analysis (Optional verification)
```powershell
python data_processing.py
python analysis.py
```

### Step 5: Start the Flask Web Application
```powershell
python app.py
```

### Step 6: View the Dashboard in your Browser
Open: **`http://127.0.0.1:5000`**

---

## 🎓 10. Viva Voce Q&A Cheat Sheet (5-Minute Pitch)

| Question | Student's Model Answer |
| :--- | :--- |
| **What is the aim of this project?** | *"To analyze civic development indicators across Mumbai's 24 administrative municipal wards and present them through an interactive web dashboard."* |
| **Why did you normalize the data?** | *"Because indicators have different units and scales. Population is in hundreds of thousands, while facility counts are in tens. Min-Max normalization standardizes them between 0 and 1 so they can be fairly combined."* |
| **How did you calculate the Development Score?** | *"It is a weighted linear combination of six normalized sub-scores: Infrastructure (25%), Health (20%), Education (20%), Sanitation (15%), Environment (10%), and Public Services (10%)."* |
| **Why did you choose Flask?** | *"Flask is lightweight, beginner-friendly, and integrates seamlessly with Python data science libraries like Pandas without the complexity of heavy enterprise frameworks."* |
| **Is this an official BMC government ranking?** | *"No. It is an analytical, educational model designed to illustrate ward-level data science techniques. All indicator weights and assumptions are documented transparently."* |

---

## ⚠️ 11. Limitations & Future Scope

### Limitations:
- Census population numbers represent baseline figures; rapid intra-city migrations alter localized densities.
- Indicator weights reflect urban planning domain heuristics rather than statutory municipal mandates.
- Correlation between indicators does not prove direct causation.

### Future Scope:
- Integration of multi-year time-series datasets to assess ward progress over decades.
- Incorporation of GIS boundary shapefiles with Leaflet / GeoPandas for detailed polygon map boundaries.
- Connecting live municipal open APIs for automated civic metrics updates.
