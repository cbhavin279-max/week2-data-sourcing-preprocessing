

import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. FILE PATHS AND OUTPUT FOLDER
# ------------------------------------------------------------

DATA_FILE = "NCRB_Table_1A.1.csv"
OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ------------------------------------------------------------
# 2. LOAD THE ACTUAL DATASET
# ------------------------------------------------------------

try:
    df = pd.read_csv(DATA_FILE)
    print("Dataset loaded successfully!")

except FileNotFoundError:
    print("ERROR: CSV file not found.")
    print("Keep visualize.py and the CSV file in the same folder.")
    raise SystemExit

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Clean State/UT names
df["State/UT"] = df["State/UT"].astype(str).str.strip()

print("\nDataset size:", df.shape)
print("\nFirst five rows:")
print(df.head())

# ------------------------------------------------------------
# 3. PREPARE THE DATA
# ------------------------------------------------------------

# Identify summary rows such as Total State, Total UT,
# and Total All India.
# Exclude these rows from state-level comparisons.

state_df = df[
    ~df["State/UT"].str.lower().str.startswith("total")
].copy()

# Convert numerical columns into numeric format
numeric_columns = [
    "2020",
    "2021",
    "2022",
    "Mid-Year Projected Population (in Lakhs) (2022)",
    "Rate of Cognizable Crimes (IPC) (2022)",
    "Chargesheeting Rate (2022)"
]

for column in numeric_columns:
    state_df[column] = pd.to_numeric(
        state_df[column], errors="coerce"
    )

# Remove rows without the main numerical data
state_df = state_df.dropna(
    subset=[
        "2020",
        "2021",
        "2022",
        "Rate of Cognizable Crimes (IPC) (2022)",
        "Chargesheeting Rate (2022)"
    ]
)

print("\nNumber of state/UT records:", len(state_df))

# ------------------------------------------------------------
# 4. CHART 1: ALL-INDIA CRIME TREND, 2020–2022
# ------------------------------------------------------------

# Prefer the official Total All India row supplied
# in the dataset rather than calculating a total.

all_india = df[
    df["State/UT"].str.lower() == "total all india"
]

if not all_india.empty:

    totals = all_india.iloc[0]

    years = ["2020", "2021", "2022"]

    crime_counts = [
        pd.to_numeric(totals[year], errors="coerce")
        for year in years
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        years,
        crime_counts,
        marker="o",
        linewidth=2
    )

    plt.title("All-India Recorded Crimes (2020–2022)")
    plt.xlabel("Year")
    plt.ylabel("Number of Recorded Crimes")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_FOLDER, "chart1_india_trend.png"),
        dpi=300
    )

    plt.show()

else:
    print("Total All India row not found. Chart 1 skipped.")

# ------------------------------------------------------------
# 5. CHART 2: TOP 10 STATES/UTs BY CRIME COUNT IN 2022
# ------------------------------------------------------------

top_10 = state_df.sort_values(
    by="2022",
    ascending=False
).head(10)

plt.figure(figsize=(11, 6))

plt.bar(
    top_10["State/UT"],
    top_10["2022"]
)

plt.title("Top 10 States/UTs by Recorded Crime Count (2022)")
plt.xlabel("State/Union Territory")
plt.ylabel("Recorded Crime Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "chart2_top10_crimes.png"),
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# 6. CHART 3: CRIME RATE BY STATE/UT IN 2022
# ------------------------------------------------------------

highest_crime_rate = state_df.sort_values(
    by="Rate of Cognizable Crimes (IPC) (2022)",
    ascending=False
).head(10)

plt.figure(figsize=(11, 6))

plt.barh(
    highest_crime_rate["State/UT"],
    highest_crime_rate["Rate of Cognizable Crimes (IPC) (2022)"]
)

plt.title("Top 10 States/UTs by IPC Crime Rate (2022)")
plt.xlabel("Crime Rate (as reported in the dataset)")
plt.ylabel("State/Union Territory")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "chart3_crime_rate.png"),
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# 7. CHART 4: CHARGESHEETING RATE BY STATE/UT
# ------------------------------------------------------------

highest_chargesheeting = state_df.sort_values(
    by="Chargesheeting Rate (2022)",
    ascending=False
).head(10)

plt.figure(figsize=(11, 6))

plt.barh(
    highest_chargesheeting["State/UT"],
    highest_chargesheeting["Chargesheeting Rate (2022)"]
)

plt.title("Top 10 States/UTs by Chargesheeting Rate (2022)")
plt.xlabel("Chargesheeting Rate (%)")
plt.ylabel("State/Union Territory")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "chart4_chargesheeting_rate.png"),
    dpi=300
)

plt.show()

# ------------------------------------------------------------
# 8. PRINT SUMMARY AND BASIC ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("NCRB DATA VISUALIZATION PROJECT SUMMARY")
print("=" * 55)

print("\n1. Number of state/UT records:", len(state_df))

print("\n2. All-India recorded crime counts:")
if not all_india.empty:
    print("2020:", int(all_india.iloc[0]["2020"]))
    print("2021:", int(all_india.iloc[0]["2021"]))
    print("2022:", int(all_india.iloc[0]["2022"]))

print("\n3. Five highest recorded crime counts in 2022:")
print(
    state_df[
        ["State/UT", "2022"]
    ].sort_values(
        by="2022", ascending=False
    ).head(5).to_string(index=False)
)

print("\n4. Five highest IPC crime rates in 2022:")
print(
    state_df[
        ["State/UT", "Rate of Cognizable Crimes (IPC) (2022)"]
    ].sort_values(
        by="Rate of Cognizable Crimes (IPC) (2022)",
        ascending=False
    ).head(5).to_string(index=False)
)

print("\n5. Five highest chargesheeting rates in 2022:")
print(
    state_df[
        ["State/UT", "Chargesheeting Rate (2022)"]
    ].sort_values(
        by="Chargesheeting Rate (2022)",
        ascending=False
    ).head(5).to_string(index=False)
)

print("\nAll charts have been saved in the outputs folder.")
print("Project completed successfully!")