import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt

# ==========================================
# STEP 1: FILE PATH
# ==========================================

file_path = Path(
    r"C:\Users\Bhavin Chauhan\Downloads\NCRB_Table_1A.1.csv"
)

output_folder = Path(
    routput_folder = Path(
    r"C:\Users\Bhavin Chauhan\OneDrive\Attachments\datascience baiccprojected\Week2_Data_Preprocessing"
)
)

output_folder.mkdir(parents=True, exist_ok=True)

# ==========================================
# STEP 2: LOAD DATASET
# ==========================================

data = pd.read_csv(file_path)

print("\nFIRST FIVE ROWS")
print(data.head())

print("\nDATASET SHAPE")
print(data.shape)

print("\nCOLUMN NAMES")
print(data.columns.tolist())

# ==========================================
# STEP 3: DATA CLEANING
# ==========================================

data.columns = data.columns.str.strip()

data = data.drop_duplicates()

data = data.dropna(how="all")

print("\nMISSING VALUES")
print(data.isnull().sum())

print("\nDUPLICATE ROWS")
print(data.duplicated().sum())

data.to_csv(
    output_folder / "Cleaned_NCRB_Data.csv",
    index=False
)

# ==========================================
# STEP 4: STATISTICAL ANALYSIS
# ==========================================

numeric_data = data.select_dtypes(include=np.number)

print("\nSTATISTICAL SUMMARY")

print(numeric_data.describe())

print("\nMEAN")
print(numeric_data.mean())

print("\nMEDIAN")
print(numeric_data.median())

print("\nSTANDARD DEVIATION")
print(numeric_data.std())

# ==========================================
# STEP 5: CORRELATION HEATMAP
# ==========================================

if numeric_data.shape[1] >= 2:

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        numeric_data.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title(
        "NCRB Statistical Correlation Heatmap"
    )

    plt.tight_layout()

    plt.savefig(
        output_folder / "Correlation_Heatmap.png",
        dpi=300
    )

    plt.show()

# ==========================================
# STEP 6: SELECT COLUMNS
# ==========================================

print("\nAVAILABLE COLUMNS:")

for column in data.columns:
    print(column)

state_col = input(
    "\nEnter State/UT column name: "
).strip()

crime_col = input(
    "Enter Crime Count column name: "
).strip()

if state_col not in data.columns:
    raise ValueError("Invalid State column name!")

if crime_col not in data.columns:
    raise ValueError("Invalid Crime column name!")

# ==========================================
# STEP 7: PREPARE DASHBOARD DATA
# ==========================================

dashboard_data = data[
    [state_col, crime_col]
].copy()

dashboard_data[crime_col] = pd.to_numeric(
    dashboard_data[crime_col],
    errors="coerce"
)

dashboard_data = dashboard_data.dropna()

# Remove common national aggregate rows
aggregate_names = [
    "ALL INDIA",
    "TOTAL (ALL INDIA)",
    "TOTAL ALL INDIA",
    "GRAND TOTAL"
]

dashboard_data = dashboard_data[
    ~dashboard_data[state_col]
    .astype(str)
    .str.upper()
    .str.strip()
    .isin(aggregate_names)
]

state_crimes = (
    dashboard_data
    .groupby(state_col)[crime_col]
    .sum()
    .sort_values(ascending=False)
)

if state_crimes.empty:
    raise ValueError("No valid data available for dashboard!")

# ==========================================
# STEP 8: DASHBOARD DESIGN
# ==========================================

sns.set_style("whitegrid")

fig, axes = plt.subplots(
    2,
    2,
    figsize=(16, 11)
)

fig.suptitle(
    "NCRB E-GOVERNANCE ANALYTICS DASHBOARD",
    fontsize=20,
    fontweight="bold",
    color="darkblue"
)

# ------------------------------------------
# CHART 1: TOP 10 STATES
# ------------------------------------------

top_states = state_crimes.head(10)

sns.barplot(
    x=top_states.values,
    y=top_states.index,
    ax=axes[0, 0],
    color="steelblue"
)

axes[0, 0].set_title(
    "Top 10 States by Reported Crime Cases"
)

axes[0, 0].set_xlabel("Reported Crime Cases")

axes[0, 0].set_ylabel("State/UT")

# ------------------------------------------
# CHART 2: PIE CHART
# ------------------------------------------

top_five = state_crimes.head(5)

other_total = state_crimes.iloc[5:].sum()

pie_values = top_five.tolist()

pie_labels = top_five.index.tolist()

if other_total > 0:

    pie_values.append(other_total)

    pie_labels.append("Other")

axes[0, 1].pie(
    pie_values,
    labels=pie_labels,
    autopct="%1.1f%%",
    startangle=90
)

axes[0, 1].set_title(
    "Crime Distribution by State"
)

# ------------------------------------------
# CHART 3: BOTTOM 10 STATES
# ------------------------------------------

bottom_states = (
    state_crimes.tail(10).sort_values()
)

sns.barplot(
    x=bottom_states.values,
    y=bottom_states.index,
    ax=axes[1, 0],
    color="seagreen"
)

axes[1, 0].set_title(
    "Bottom 10 States by Reported Crime Cases"
)

axes[1, 0].set_xlabel("Reported Crime Cases")

axes[1, 0].set_ylabel("State/UT")

# ------------------------------------------
# CHART 4: KPI SUMMARY
# ------------------------------------------

axes[1, 1].axis("off")

total_crimes = state_crimes.sum()

total_states = len(state_crimes)

highest_state = state_crimes.index[0]

highest_crimes = state_crimes.iloc[0]

summary_text = (
    "KEY PERFORMANCE INDICATORS\n\n"
    f"Total Reported Cases: {total_crimes:,.0f}\n\n"
    f"States/UTs Covered: {total_states}\n\n"
    f"Highest Count State: {highest_state}\n\n"
    f"Highest Reported Count: {highest_crimes:,.0f}"
)

axes[1, 1].text(
    0.05,
    0.85,
    summary_text,
    fontsize=15,
    verticalalignment="top",
    bbox=dict(
        facecolor="lightblue",
        alpha=0.4,
        boxstyle="round,pad=1"
    )
)

plt.tight_layout(
    rect=[0, 0, 1, 0.95]
)

dashboard_path = (
    output_folder / "Week5_NCRB_Dashboard.png"
)

plt.savefig(
    dashboard_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nDashboard created successfully!")

# ==========================================
# STEP 9: POLICY RECOMMENDATIONS
# ==========================================

recommendations = [
    "Improve digital crime reporting systems to make "
    "complaint registration easier for citizens.",

    "Develop government dashboards to monitor "
    "reported crime statistics regularly.",

    "Use population-adjusted crime rates and local "
    "context when planning public safety resources.",

    "Improve the quality and consistency of "
    "government crime data.",

    "Use predictive analytics carefully to support "
    "future planning and resource management.",

    "Increase public awareness about cybercrime "
    "prevention and online complaint services."
]

print("\nPOLICY RECOMMENDATIONS")

for index, recommendation in enumerate(
    recommendations,
    start=1
):

    print(index, recommendation)

# ==========================================
# STEP 10: CREATE WORD REPORT
# ==========================================

doc = Document()

# Document title
doc.add_heading(
    "WEEK 5 INTERNSHIP REPORT",
    0
)

doc.add_heading(
    "Reporting, Recommendations, and Dashboard "
    "Design for E-Governance Insights",
    level=1
)

doc.add_paragraph(
    "Project: NCRB Crime Data Analytics for E-Governance"
)

doc.add_paragraph(
    "Student Name: Bhavin Chauhan"
)

doc.add_paragraph(
    "Domain: Data Analytics and E-Governance"
)

doc.add_page_break()

# Executive Summary
doc.add_heading(
    "1. Executive Summary",
    level=1
)

doc.add_paragraph(
    "This report presents an overview of crime data "
    "analysis using NCRB statistics. The project "
    "focuses on statistical analysis, data visualization, "
    "dashboard design, and policy recommendations "
    "to support e-governance decision-making."
)

# Introduction
doc.add_heading(
    "2. Introduction",
    level=1
)

doc.add_paragraph(
    "E-governance uses digital technologies to improve "
    "government services and public administration. "
    "Data analytics helps government departments "
    "understand public information and support "
    "evidence-based decisions."
)

# Dataset
doc.add_heading(
    "3. Dataset Description",
    level=1
)

doc.add_paragraph(
    "The dataset used in this project is "
    "NCRB_Table_1A.1.csv from the National Crime "
    "Records Bureau. It provides crime-related "
    "statistics that may support public safety analysis."
)

doc.add_paragraph(
    f"Dataset Rows: {data.shape[0]}"
)

doc.add_paragraph(
    f"Dataset Columns: {data.shape[1]}"
)

# Data Analysis
doc.add_heading(
    "4. Data Analysis Recap",
    level=1
)

doc.add_paragraph(
    "The dataset was examined using Python and Pandas. "
    "Data preparation included checking missing values, "
    "removing exact duplicate rows, and inspecting "
    "numerical information."
)

doc.add_paragraph(
    "Statistical analysis included mean, median, "
    "standard deviation, and descriptive statistics."
)

# Dashboard
doc.add_heading(
    "5. Dashboard Design",
    level=1
)

doc.add_paragraph(
    "A dashboard was developed to display selected "
    "NCRB crime statistics using bar charts, "
    "a pie chart, and key performance indicators."
)

doc.add_picture(
    str(dashboard_path),
    width=Inches(6)
)

# KPI Section
doc.add_heading(
    "6. Key Performance Indicators",
    level=1
)

doc.add_paragraph(
    f"Total Reported Cases: {total_crimes:,.0f}"
)

doc.add_paragraph(
    f"States/UTs Covered: {total_states}"
)

doc.add_paragraph(
    f"Highest Reported Count State: {highest_state}"
)

# Policy Recommendations
doc.add_heading(
    "7. Policy Recommendations",
    level=1
)

for recommendation in recommendations:

    doc.add_paragraph(
        recommendation,
        style="List Bullet"
    )

# Interpretation
doc.add_heading(
    "8. Interpretation of Results",
    level=1
)

doc.add_paragraph(
    "The dashboard provides a visual comparison "
    "of reported crime counts across geographical "
    "regions. Such visualizations can help government "
    "officials identify areas requiring further analysis."
)

# Challenges
doc.add_heading(
    "9. Challenges and Limitations",
    level=1
)

doc.add_paragraph(
    "The analysis may be affected by missing data, "
    "differences in crime reporting practices, "
    "and incomplete historical information. "
    "Reported crime counts should not be interpreted "
    "as direct measures of crime risk without "
    "considering population and reporting differences."
)

# Conclusion
doc.add_heading(
    "10. Conclusion",
    level=1
)

doc.add_paragraph(
    "This project demonstrates how data analysis "
    "and dashboard visualization can support "
    "e-governance decision-making. The proposed "
    "recommendations focus on improving digital "
    "reporting systems, public safety monitoring, "
    "and responsible data-driven planning."
)

# References
doc.add_heading(
    "11. References",
    level=1
)

references = [
    "National Crime Records Bureau (NCRB), Government of India.",
    "Python Documentation: https://www.python.org/",
    "Pandas Documentation: https://pandas.pydata.org/",
    "Matplotlib Documentation: https://matplotlib.org/",
    "Seaborn Documentation: https://seaborn.pydata.org/"
]

for reference in references:

    doc.add_paragraph(
        reference,
        style="List Bullet"
    )

# Save Word report
report_path = (
    output_folder / "Week5_E_Governance_Report.docx"
)

doc.save(report_path)

print("\nWORD REPORT CREATED SUCCESSFULLY!")

print("\nReport Location:")
print(report_path)

print("\nPROJECT COMPLETED!")