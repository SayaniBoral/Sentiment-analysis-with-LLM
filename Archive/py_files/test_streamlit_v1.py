# How to use: make sure that the data files are in the same directory, make sure you have pandas version 1.1.3 installed
# Open terminal to this directory, and then run the command: streamlit run test_streamlit_v1.py





import streamlit as st
import pandas as pd

# Define the file paths for the datasets
gift_card_path = 'amazon_reviews_us_Gift_Card_v1_00.tsv'
major_appliances_path = 'amazon_reviews_us_Major_Appliances_v1_00.tsv'
shoes_path = 'amazon_reviews_us_Shoes_v1_00.tsv'
electronics_path = 'amazon_reviews_us_Electronics_v1_00.tsv'


def read_dataset(dataset_path):
    return pd.read_csv(dataset_path, sep='\t', error_bad_lines=False, warn_bad_lines=False)


def merge_datasets(selected_category):
    paths = {
        'Gift Card': gift_card_path,
        'Major Appliances': major_appliances_path,
        'Shoes': shoes_path,
        'Electronics': electronics_path
    }
    if selected_category in paths:
        return read_dataset(paths[selected_category])
    elif selected_category == 'all':
        dfs = [read_dataset(path) for path in paths.values()]
        return pd.concat(dfs, ignore_index=True)


def remove_specific_columns(df):
    df.drop(columns=["customer_id", "review_id", "product_id"], inplace=True)
    return df


def modify_review_date_to_year(df):
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce').dt.year
    df.dropna(subset=['review_date'], inplace=True)
    df['review_date'] = df['review_date'].astype(int)
    return df


def categorize_votes(df, column_names):
    for column in column_names:
        category_col_name = f'{column}_category'
        df[category_col_name] = 'No Votes'  # Default category for 0 votes
        has_votes = df[column] > 0
        votes_data = df.loc[has_votes, column]

        unique_values = votes_data.unique()
        if len(unique_values) > 4:
            try:
                df.loc[has_votes, category_col_name] = pd.qcut(votes_data, q=4,
                                                               labels=["Minimal Engagement", "Low Engagement",
                                                                       "Moderate Engagement", "High Engagement"])
            except ValueError:
                df.loc[has_votes, category_col_name] = pd.cut(votes_data, bins=4,
                                                              labels=["Minimal Engagement", "Low Engagement",
                                                                      "Moderate Engagement", "High Engagement"])
        else:
            df.loc[has_votes, category_col_name] = pd.cut(votes_data, bins=4,
                                                          labels=["Minimal Engagement", "Low Engagement",
                                                                  "Moderate Engagement", "High Engagement"])
    return df


# Streamlit UI
st.title('Amazon Reviews Analysis')

selected_category = st.selectbox(
    "Please select a product category:",
    ('Gift Card', 'Major Appliances', 'Shoes', 'Electronics', 'all')
)

df = merge_datasets(selected_category)
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
    unique_values = {var: df[var].dropna().unique() for var in selected_variables}
    filters = {}
    for variable in selected_variables:
        selected_value = st.selectbox(f"Values for {variable}:", ['All'] + list(unique_values[variable]))
        if selected_value != 'All':
            filters[variable] = selected_value
    if filters:
        for variable, selected_value in filters.items():
            df = df[df[variable] == selected_value]
    st.write("Filtered dataset based on your selections:")
    st.dataframe(df.head())
else:
    st.write("No variable selections made. Displaying first entries of the dataset.")
    st.dataframe(df.head())
