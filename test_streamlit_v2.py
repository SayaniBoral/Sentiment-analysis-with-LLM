"""
A Streamlit app for analyzing Amazon product reviews.

How to use: Ensure the data files are in the same directory and pandas version 1.1.3 is installed.
Open a terminal to this directory, and then run the command: streamlit run test_streamlit_v2_PEP8_kill_warning.py
"""

import streamlit as st
import pandas as pd

# Define the file paths for the datasets
DATASET_PATHS = {
    'Gift Card': 'amazon_reviews_us_Gift_Card_v1_00.tsv',
    'Major Appliances': 'amazon_reviews_us_Major_Appliances_v1_00.tsv',
    'Shoes': 'amazon_reviews_us_Shoes_v1_00.tsv',
    'Electronics': 'amazon_reviews_us_Electronics_v1_00.tsv'
}

@st.experimental_memo
def read_dataset(dataset_path):
    """Reads a dataset from a given file path and returns a DataFrame."""
    try:
        df = pd.read_csv(dataset_path, sep='\t', on_bad_lines='skip')
        return df, ""
    except Exception as e:
        return pd.DataFrame(), str(e)

@st.experimental_memo
def merge_datasets(selected_category):
    """Merges datasets based on the selected category or all if 'all' is selected."""
    if selected_category in DATASET_PATHS:
        df, error = read_dataset(DATASET_PATHS[selected_category])
        return df, error
    elif selected_category == 'all':
        dfs = []
        for path in DATASET_PATHS.values():
            df, error = read_dataset(path)
            if error:
                return pd.DataFrame(), error
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True), ""

def remove_specific_columns(df):
    """Removes specific columns from the DataFrame."""
    return df.drop(columns=["customer_id", "review_id", "product_id"])

def modify_review_date_to_year(df):
    """Converts the review_date in DataFrame to only include the year."""
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

        try:
            df.loc[has_votes, category_col_name] = pd.qcut(votes_data, q=4,
                                                           labels=["Minimal Engagement", "Low Engagement",
                                                                   "Moderate Engagement", "High Engagement"],
                                                           duplicates='drop')
        except ValueError:
            # Fallback strategy if qcut fails due to non-unique bin edges
            bins = [votes_data.min(), votes_data.max()]
            labels = ["Engagement"]
            df.loc[has_votes, category_col_name] = pd.cut(votes_data, bins=bins, labels=labels, include_lowest=True)

    return df

# Streamlit UI components
def main():
    """Main function to render the Streamlit UI components."""
    st.title('Amazon Reviews Analysis')

    selected_category = st.selectbox(
        "Please select a product category:",
        ('Gift Card', 'Major Appliances', 'Shoes', 'Electronics', 'all')
    )

    df, error = merge_datasets(selected_category)
    if error:
        st.error(f"Failed to load dataset: {error}")
    else:
        st.write(f"Dataset for '{selected_category}' category loaded.")
        df = remove_specific_columns(df)
        st.write("Removed specific columns: customer_id, review_id, product_id")

        df = modify_review_date_to_year(df)
        st.write("Modified 'review_date' to retain the year only.")

        df = categorize_votes(df, ['helpful_votes', 'total_votes'])
        st.write("Categorized 'helpful_votes' and 'total_votes' into engagement levels.")

        selected_variables = st.multiselect(
            "Select variables to filter by:",
            options=df.columns,
            default=df.columns[0]
        )

        if selected_variables:
            filters = {var: st.selectbox(f"Values for {var}:", ['All'] + list(df[var].dropna().unique()))
                       for var in selected_variables}
            for var, value in filters.items():
                if value != 'All':
                    df = df[df[var] == value]
            st.write("Filtered dataset based on your selections:")
            st.dataframe(df.head())
        else:
            st.write("No variable selections made. Displaying first entries of the dataset.")
            st.dataframe(df.head())

if __name__ == "__main__":
    main()
