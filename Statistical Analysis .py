import pandas as pd
import numpy as np
from pathlib import Path

# Step 1: Define CSV file path
file_path = Path(r"C:\Users\Bhavin Chauhan\Downloads\NCRB_Table_1A.1.csv")

# Step 2: Load dataset
data = pd.read_csv(file_path)

# Step 3: Display first five rows
print("\nFIRST FIVE ROWS")
print(data.head())

# Step 4: Select numerical columns
numeric_data = data.select_dtypes(include=np.number)

# Step 5: Calculate Mean
print("\nMEAN")
print(numeric_data.mean())

# Step 6: Calculate Median
print("\nMEDIAN")
print(numeric_data.median())

# Step 7: Calculate Standard Deviation
print("\nSTANDARD DEVIATION")
print(numeric_data.std())

# Step 8: Minimum Values
print("\nMINIMUM VALUES")
print(numeric_data.min())

# Step 9: Maximum Values
print("\nMAXIMUM VALUES")
print(numeric_data.max())

# Step 10: Statistical Summary
print("\nSTATISTICAL SUMMARY")
print(numeric_data.describe())

print("\nStatistical Analysis Completed Successfully!")