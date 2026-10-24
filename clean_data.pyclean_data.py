import pandas as pd
from pathlib import Path

# Step 1: Define CSV file path
file_path = Path("C:/Users/Bhavin Chauhan/Downloads/NCRB_Table_1A.1.csv")

# Step 2: Load dataset
data = pd.read_csv(file_path)

# Step 3: Display first five rows
print("\nFIRST FIVE ROWS")
print(data.head())

# Step 4: Dataset size
print("\nDATASET SIZE")
print(data.shape)

# Step 5: Missing values
print("\nMISSING VALUES")
print(data.isnull().sum())

# Step 6: Duplicate rows
print("\nDUPLICATE ROWS")
print(data.duplicated().sum())