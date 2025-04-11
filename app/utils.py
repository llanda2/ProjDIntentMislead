# utils.py
# Utility functions for data loading and cleaning
# Dataset: data/leadingCauseDeathUSA.csv

import pandas as pd


def load_and_clean_data(filepath):
    """
    Loads the raw cause of death data and performs cleaning steps:
    - Remove commas from 'Deaths' column and convert to integer
    - Rename columns for convenience
    - Filter out any unnecessary columns (optional)
    - Handle any missing values
    - Return cleaned DataFrame
    """
    # Load the data
    df = pd.read_csv(filepath)

    # Display initial data info for verification
    print("Initial data shape:", df.shape)
    print("Initial columns:", df.columns.tolist())

    # Rename columns for easier reference
    df = df.rename(columns={
        '113 Cause Name': 'ICD_Code_Description',
        'Cause Name': 'Cause',
        'State': 'State',
        'Deaths': 'Deaths',
        'Age-adjusted Death Rate': 'Age_Adjusted_Death_Rate'
    })

    # Clean the 'Deaths' column (remove commas and convert to integer)
    df['Deaths'] = df['Deaths'].astype(str).str.replace(',', '', regex=False).astype(int)

    # Ensure 'Year' column is integer
    df['Year'] = df['Year'].astype(int)

    # Optional: Clean 'Age_Adjusted_Death_Rate' to numeric
    df['Age_Adjusted_Death_Rate'] = pd.to_numeric(df['Age_Adjusted_Death_Rate'], errors='coerce')

    # Handle missing values, if any (basic forward fill as a safe default)
    df = df.fillna(method='ffill')

    # Print cleaned data sample for verification
    print("Cleaned data preview:")
    print(df.head())

    return df


# Test the function (you can run this script directly to check)
if __name__ == "__main__":
    filepath = '/Users/laurenlanda/PycharmProjects/ProjDIntentMislead/data/leadingCauseDeathUSA.csv'
    cleaned_df = load_and_clean_data(filepath)

    # Optional: Export cleaned data to CSV for inspection
    cleaned_df.to_csv('../data/leadingCauseDeath_cleaned.csv', index=False)

    print("Cleaned data saved to 'data/leadingCauseDeath_cleaned.csv'")
