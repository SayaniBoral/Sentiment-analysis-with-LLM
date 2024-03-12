"""
This module contains the script for processing the raw data files. 
It contains functions to read, merge data files. 
Additionally there are functions to transform columns

Example usage:

    import numpy as np
    from data_processing import merge_datasets

    # Load training data and query sample
    data=merge_datasets('all')
    display(data)
    
"""

import os
import pandas as pd

# Constants are capitalized (PEP 8)
DATA_DIR = "amazon_raw_data"
DATASET_PATHS = {
    'Gift Card': os.path.join(DATA_DIR, 'amazon_reviews_us_Gift_Card_v1_00.tsv'),
    'Major Appliances': os.path.join(DATA_DIR, 'amazon_reviews_us_Major_Appliances_v1_00.tsv'),
    'Shoes': os.path.join(DATA_DIR, 'amazon_reviews_us_Shoes_v1_00.tsv'),
    'Electronics': os.path.join(DATA_DIR, 'amazon_reviews_us_Electronics_v1_00.tsv')
}

def read_dataset(dataset_path):
    """
    Reads a dataset from a specified file path using pandas.

    Parameters:
    - dataset_path (str): The path to the dataset file.

    Returns:
    - DataFrame: Loaded data as pandas DataFrame.
    - str: An empty string on success, or an error message on failure.
    """
    try:
        df = pd.read_csv(dataset_path, sep='\t', error_bad_lines=False, warn_bad_lines=False)
        return df, ""
    except ValueError as e:
        return pd.DataFrame(), str(e)

def merge_datasets(selected_category):
    """
    Merges datasets based on the selected category or merges all if 'all' is selected.

    Parameters:
    - selected_category (str): The category of datasets to merge or 'all'.

    Returns:
    - DataFrame: Merged dataset(s) as pandas DataFrame.
    - str: An empty string on success, or an error message on failure.
    """
    if selected_category in DATASET_PATHS:
        return read_dataset(DATASET_PATHS[selected_category])
    if selected_category == 'all':
        dfs = [read_dataset(path)[0] for path in DATASET_PATHS.values()]
        return pd.concat(dfs, ignore_index=True), ""
    return pd.DataFrame(), "Invalid category specified."

def remove_specific_columns(df):
    """
    Removes specific columns from a DataFrame.

    Parameters:
    - df (DataFrame): The pandas DataFrame to process.

    Returns:
    - DataFrame: The DataFrame with specific columns removed.
    """
    return df.drop(columns=["customer_id", "review_id", "product_id"])

def modify_review_date_to_year(df):
    """
    Modifies the review_date column of a DataFrame to only include the year.

    Parameters:
    - df (DataFrame): The pandas DataFrame to process.

    Returns:
    - DataFrame: The DataFrame with modified review_date column.
    """
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce').dt.year
    df.dropna(subset=['review_date'], inplace=True)
    df['review_date'] = df['review_date'].astype(int)
    return df

def categorize_votes(df, column_names):
    """
    Categorizes votes into engagement levels based on provided column names.

    Parameters:
    - df (DataFrame): The pandas DataFrame to process.
    - column_names (list): List of column names to categorize.

    Returns:
    - DataFrame: The DataFrame with vote categories added.
    """
    for column in column_names:
        category_col_name = f'{column}_category'
        df[category_col_name] = 'No Votes'  # Default category for 0 votes
        has_votes = df[column] > 0
        votes_data = df.loc[has_votes, column]
        # Dynamically categorize based on unique values in votes_data
        try:
            df.loc[has_votes, category_col_name] = pd.qcut(
                votes_data, q=4, labels=["Minimal", "Low", "Moderate", "High"])
        except ValueError:
            # Fallback for when qcut fails due to identical values
            df.loc[has_votes, category_col_name] = "Minimal"
    return df
