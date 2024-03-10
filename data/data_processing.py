# data_processing.py
import os
import pandas as pd

# Constants should be capitalized
DATA_DIR = "amazon_raw_data"
DATASET_PATHS = {
    'Gift Card': os.path.join(DATA_DIR, 'amazon_reviews_us_Gift_Card_v1_00.tsv'),
    'Major Appliances': os.path.join(DATA_DIR, 'amazon_reviews_us_Major_Appliances_v1_00.tsv'),
    'Shoes': os.path.join(DATA_DIR, 'amazon_reviews_us_Shoes_v1_00.tsv'),
    'Electronics': os.path.join(DATA_DIR, 'amazon_reviews_us_Electronics_v1_00.tsv')
}

def read_dataset(dataset_path):
    """Reads a dataset from a given file path and returns a DataFrame."""
    try:
        df = pd.read_csv(dataset_path, sep='\t', error_bad_lines=False, warn_bad_lines=False)
        return df, ""
    except Exception as e:
        return pd.DataFrame(), str(e)

def merge_datasets(selected_category):
    """Merges datasets based on the selected category or 'all'."""
    if selected_category in DATASET_PATHS:
        return read_dataset(DATASET_PATHS[selected_category])
    elif selected_category == 'all':
        dfs = [read_dataset(path) for path in DATASET_PATHS.values()]
        return pd.concat(dfs, ignore_index=True), ""

def remove_specific_columns(df):
    """Removes specific columns from the DataFrame."""
    return df.drop(columns=["customer_id", "review_id", "product_id"])

def modify_review_date_to_year(df):
    """Converts the review date to retain only the year."""
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce').dt.year
    df.dropna(subset=['review_date'], inplace=True)
    df['review_date'] = df['review_date'].astype(int)
    return df

def categorize_votes(df, column_names):
    """Categorizes votes into engagement levels."""
    for column in column_names:
        category_col_name = f'{column}_category'
        df[category_col_name] = 'No Votes'  # Default category for 0 votes
        has_votes = df[column] > 0
        votes_data = df.loc[has_votes, column]
        
        unique_values = votes_data.unique()
        if len(unique_values) > 4:
            try:
                df.loc[has_votes, category_col_name] = pd.qcut(
                    votes_data, q=4,
                    labels=["Minimal Engagement", "Low Engagement",
                            "Moderate Engagement", "High Engagement"])
            except ValueError:
                df.loc[has_votes, category_col_name] = pd.cut(
                    votes_data, bins=4,
                    labels=["Minimal Engagement", "Low Engagement",
                            "Moderate Engagement", "High Engagement"])
        else:
            df.loc[has_votes, category_col_name] = pd.cut(
                votes_data, bins=4,
                labels=["Minimal Engagement", "Low Engagement",
                        "Moderate Engagement", "High Engagement"])
    return df

if __name__ == "__main__":
    # Test functionality when running this script directly
    category = 'Electronics'  # Example category
    df, error = merge_datasets(category)
    if not error:
        print(f"Dataset for '{category}' loaded successfully.")
        df = remove_specific_columns(df)
        print("Specific columns removed.")
        df = modify_review_date_to_year(df)
        print("Review dates modified to retain only the year.")
        df = categorize_votes(df, ['helpful_votes', 'total_votes'])
        print("Votes categorized into engagement levels.")
    else:
        print(f"Failed to load dataset for '{category}': {error}")
