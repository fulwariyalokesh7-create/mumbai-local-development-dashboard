-- =====================================================================
-- MUMBAI LOCAL DEVELOPMENT DASHBOARD — MYSQL DATABASE SCRIPT
-- B.Sc Data Science Student Project
-- Database: mumbai_development
-- Table: ward_development
-- =====================================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS mumbai_development;
USE mumbai_development;

-- Step 2: Create Main Ward Development Table
DROP TABLE IF EXISTS ward_development;

CREATE TABLE ward_development (
    Ward_ID VARCHAR(10) PRIMARY KEY,
    Ward_Name VARCHAR(100) NOT NULL,
    Zone VARCHAR(50) NOT NULL,
    Area_sq_km DECIMAL(6, 2) NOT NULL,
    Population INT NOT NULL,
    Population_Density INT NOT NULL,
    Road_Length_km DECIMAL(6, 2),
    Water_Supply_Coverage_pct DECIMAL(5, 2),
    Drainage_Coverage_pct DECIMAL(5, 2),
    Waste_Collection_Coverage_pct DECIMAL(5, 2),
    Schools_Count INT,
    Hospitals_Count INT,
    Health_Centres_Count INT,
    Public_Toilets_Count INT,
    Parks_Count INT,
    Green_Coverage_pct DECIMAL(5, 2),
    Waste_Management_Score DECIMAL(5, 2),
    Infrastructure_Score DECIMAL(5, 2),
    Health_Score DECIMAL(5, 2),
    Education_Score DECIMAL(5, 2),
    Sanitation_Score DECIMAL(5, 2),
    Environment_Score DECIMAL(5, 2),
    Public_Services_Score DECIMAL(5, 2),
    Development_Score DECIMAL(5, 2),
    Development_Category VARCHAR(30)
);

-- Step 3: Insert 24 Mumbai Administrative Wards Data
INSERT INTO ward_development VALUES
('A', 'Colaba - Fort - Marine Drive', 'Zone 1 - Island City', 12.50, 185014, 14801, 135.2, 98.5, 96.0, 99.0, 78, 14, 22, 142, 38, 24.5, 88.0, 84.6, 82.4, 81.2, 85.1, 76.5, 83.0, 82.5, 'High Development'),
('B', 'Sandhurst Road - Dongri', 'Zone 1 - Island City', 2.47, 127290, 51534, 42.8, 92.0, 85.0, 91.0, 36, 6, 12, 98, 9, 6.2, 68.0, 58.4, 56.2, 52.8, 61.0, 42.1, 55.0, 55.2, 'Moderate Development'),
('C', 'Marine Lines - Bhuleshwar', 'Zone 1 - Island City', 1.78, 166161, 93349, 38.5, 90.5, 84.0, 92.0, 42, 8, 14, 115, 7, 4.8, 66.0, 55.8, 54.5, 50.1, 59.3, 38.4, 52.5, 52.7, 'Moderate Development'),
('D', 'Malabar Hill - Tardeo - Walkeshwar', 'Zone 1 - Island City', 8.03, 346866, 43196, 112.0, 97.0, 95.0, 97.5, 94, 18, 28, 185, 42, 22.0, 86.0, 81.2, 80.1, 76.4, 82.3, 74.2, 79.5, 79.5, 'High Development'),
('E', 'Byculla - Mazgaon - Mumbai Central', 'Zone 1 - Island City', 7.40, 393286, 53147, 94.6, 91.0, 86.5, 93.0, 85, 12, 24, 198, 18, 11.5, 72.0, 66.3, 64.2, 62.8, 68.5, 53.8, 64.0, 64.2, 'Moderate Development'),
('F/North', 'Matunga - Sion - Wadala', 'Zone 2 - Island City', 13.00, 529003, 40693, 142.5, 91.5, 88.0, 92.5, 124, 15, 31, 265, 34, 16.8, 75.0, 71.5, 67.4, 68.2, 72.1, 62.5, 69.0, 69.1, 'High Development'),
('F/South', 'Parel - Sewri - Naigaon', 'Zone 2 - Island City', 9.60, 360972, 37601, 105.8, 93.0, 89.5, 94.0, 88, 16, 26, 178, 25, 14.2, 77.0, 73.4, 72.8, 69.5, 75.0, 60.8, 71.0, 71.4, 'High Development'),
('G/North', 'Dharavi - Dadar West - Mahim', 'Zone 2 - Island City', 9.07, 599039, 66046, 118.4, 84.0, 76.0, 85.0, 110, 11, 28, 340, 21, 8.5, 58.0, 52.6, 48.5, 49.2, 54.8, 40.2, 51.5, 50.2, 'Moderate Development'),
('G/South', 'Worli - Lower Parel - Prabhadevi', 'Zone 2 - Island City', 10.00, 457931, 45793, 126.0, 94.5, 91.0, 95.5, 102, 17, 29, 210, 32, 18.0, 81.0, 78.2, 76.3, 73.0, 77.9, 67.5, 75.5, 75.3, 'High Development'),
('H/East', 'Santacruz East - Bandra East', 'Zone 3 - Western Suburbs', 13.53, 557239, 41185, 152.0, 88.0, 82.0, 89.0, 118, 13, 30, 285, 28, 12.4, 70.0, 64.8, 61.5, 63.0, 67.2, 52.6, 63.5, 62.7, 'Moderate Development'),
('H/West', 'Bandra West - Khar - Santacruz W', 'Zone 3 - Western Suburbs', 11.55, 307581, 26630, 148.6, 97.5, 94.0, 98.0, 96, 19, 25, 160, 45, 21.5, 87.0, 83.5, 84.1, 82.0, 83.8, 75.6, 82.0, 82.4, 'High Development'),
('K/East', 'Andheri East - Jogeshwari East', 'Zone 3 - Western Suburbs', 24.78, 823885, 33248, 245.0, 87.5, 81.5, 88.5, 165, 18, 42, 395, 36, 13.8, 69.0, 65.2, 59.8, 61.4, 66.0, 53.2, 63.0, 62.3, 'Moderate Development'),
('K/West', 'Andheri West - Versova - Juhu', 'Zone 4 - Western Suburbs', 23.29, 749348, 32175, 230.5, 95.0, 92.0, 96.0, 158, 22, 38, 310, 52, 20.4, 84.0, 80.4, 78.5, 75.2, 79.4, 72.1, 77.5, 77.7, 'High Development'),
('P/North', 'Malad - Marve - Manori', 'Zone 4 - Western Suburbs', 46.67, 941366, 20171, 280.0, 85.0, 78.0, 86.0, 172, 14, 39, 420, 44, 17.5, 65.0, 60.8, 54.2, 56.8, 61.5, 56.2, 58.0, 58.0, 'Moderate Development'),
('P/South', 'Goregaon - Oshiwara', 'Zone 4 - Western Suburbs', 24.44, 463736, 18974, 185.0, 92.5, 88.0, 93.0, 112, 15, 27, 225, 38, 23.0, 78.0, 74.1, 71.0, 72.5, 74.8, 68.9, 72.5, 72.7, 'High Development'),
('L', 'Kurla - Sakinaka - Chandivali', 'Zone 5 - Eastern Suburbs', 15.88, 902226, 56815, 165.4, 82.0, 74.0, 83.0, 145, 12, 35, 465, 22, 7.2, 55.0, 49.5, 44.8, 47.5, 51.2, 36.5, 48.5, 47.3, 'Moderate Development'),
('M/East', 'Govandi - Mankhurd - Shivaji Nagar', 'Zone 5 - Eastern Suburbs', 32.50, 807720, 24853, 195.0, 78.5, 69.0, 79.0, 120, 8, 26, 490, 19, 9.0, 48.0, 42.4, 36.5, 41.2, 44.8, 35.1, 41.0, 40.7, 'Low Development'),
('M/West', 'Chembur - Tilak Nagar - Mahul', 'Zone 5 - Eastern Suburbs', 36.50, 411363, 11270, 178.0, 93.0, 89.0, 94.0, 95, 14, 24, 195, 40, 25.0, 79.0, 76.5, 73.2, 74.0, 76.8, 73.0, 75.0, 75.0, 'High Development'),
('N', 'Ghatkopar - Vikhroli West', 'Zone 6 - Eastern Suburbs', 25.96, 622853, 23993, 192.0, 90.0, 85.0, 91.0, 130, 15, 32, 270, 35, 16.5, 74.0, 70.2, 67.8, 68.4, 71.0, 61.4, 68.5, 68.5, 'High Development'),
('S', 'Bhandup - Powai - Kanjurmarg', 'Zone 6 - Eastern Suburbs', 64.00, 743783, 11622, 265.0, 89.0, 83.0, 90.0, 140, 16, 36, 310, 48, 28.0, 76.0, 72.8, 69.1, 67.0, 72.2, 74.5, 70.5, 71.3, 'High Development'),
('T', 'Mulund - Nahur', 'Zone 6 - Eastern Suburbs', 45.42, 341463, 7518, 175.0, 96.0, 93.0, 96.5, 92, 16, 23, 150, 46, 29.5, 85.0, 82.6, 81.4, 79.5, 82.4, 78.2, 81.0, 81.2, 'High Development'),
('R/Central', 'Borivali - Gorai - Eksar', 'Zone 7 - Western Suburbs', 32.62, 562162, 17234, 215.0, 95.5, 92.5, 96.0, 128, 18, 33, 230, 50, 26.5, 83.0, 81.0, 79.2, 77.5, 80.5, 76.4, 79.0, 79.3, 'High Development'),
('R/North', 'Dahisar - Mandapeshwar', 'Zone 7 - Western Suburbs', 18.00, 431368, 23965, 150.0, 91.0, 86.0, 92.0, 98, 12, 24, 185, 30, 19.0, 74.0, 71.5, 66.8, 68.0, 71.6, 64.2, 69.0, 69.3, 'High Development'),
('R/South', 'Kandivali - Charkop - Poisar', 'Zone 7 - Western Suburbs', 17.78, 691229, 38877, 185.0, 92.0, 87.0, 93.0, 135, 16, 34, 280, 39, 18.2, 76.0, 73.1, 69.5, 69.8, 73.5, 63.8, 70.5, 70.6, 'High Development');

-- =====================================================================
-- STEP 4: BEGINNER-FRIENDLY VIVA SQL QUERIES
-- =====================================================================

-- Query 1: Total number of wards and total population in Mumbai
SELECT 
    COUNT(*) AS Total_Wards,
    SUM(Population) AS Total_Mumbai_Population,
    ROUND(AVG(Population), 0) AS Avg_Ward_Population
FROM ward_development;

-- Query 2: City-wide average, highest and lowest development scores
SELECT 
    ROUND(AVG(Development_Score), 2) AS Average_Development_Score,
    MAX(Development_Score) AS Highest_Score,
    MIN(Development_Score) AS Lowest_Score
FROM ward_development;

-- Query 3: Top 5 wards ranked by Development Score
SELECT 
    Ward_ID,
    Ward_Name,
    Zone,
    Development_Score,
    Development_Category
FROM ward_development
ORDER BY Development_Score DESC
LIMIT 5;

-- Query 4: Wards with lowest project-defined development score (Priority Focus)
SELECT 
    Ward_ID,
    Ward_Name,
    Zone,
    Development_Score,
    Infrastructure_Score,
    Health_Score,
    Education_Score
FROM ward_development
ORDER BY Development_Score ASC
LIMIT 5;

-- Query 5: Zone-wise summary of wards, population, and average development score
SELECT 
    Zone,
    COUNT(Ward_ID) AS Ward_Count,
    SUM(Population) AS Zone_Population,
    ROUND(AVG(Population_Density), 0) AS Avg_Density,
    ROUND(AVG(Development_Score), 2) AS Avg_Zone_Dev_Score
FROM ward_development
GROUP BY Zone
ORDER BY Avg_Zone_Dev_Score DESC;

-- Query 6: Count of wards per project-defined Development Category
SELECT 
    Development_Category,
    COUNT(*) AS Number_of_Wards,
    ROUND((COUNT(*) / 24.0) * 100, 1) AS Percentage_of_Wards
FROM ward_development
GROUP BY Development_Category
ORDER BY Number_of_Wards DESC;

-- Query 7: Comparison of Infrastructure and Health scores across wards
SELECT 
    Ward_ID,
    Ward_Name,
    Infrastructure_Score,
    Health_Score,
    Public_Services_Score,
    Development_Score
FROM ward_development
WHERE Development_Category = 'High Development'
ORDER BY Infrastructure_Score DESC;
