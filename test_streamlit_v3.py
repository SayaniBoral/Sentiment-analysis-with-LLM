import streamlit as st
import pandas as pd


def load_data(file_path):
    """Load and return the pre-processed sentiment analysis dataframe."""
    return pd.read_csv(file_path).iloc[:, 1:]


def apply_filters(dataframe):
    """Apply user-selected filters to the dataframe and return the filtered dataframe."""
    # Filtering UI
    st.sidebar.header('Filter Options')

    # Marketplace filter
    marketplace = st.sidebar.selectbox(
        'Marketplace:',
        ['All'] + list(dataframe['marketplace'].unique())
    )

    # Product category filter
    category = st.sidebar.selectbox(
        'Product Category:',
        ['All'] + list(dataframe['product_category'].unique())
    )

    # Star rating filter
    rating = st.sidebar.selectbox(
        'Star Rating:',
        ['All'] + sorted(dataframe['star_rating'].unique())
    )

    # Verified purchase filter
    verified = st.sidebar.selectbox(
        'Verified Purchase:',
        ['All'] + list(dataframe['verified_purchase'].unique())
    )

    # Review date filter
    review_year = st.sidebar.selectbox(
        'Review Year:',
        ['All'] + sorted(dataframe['review_date'].unique())
    )

    # Apply the filters
    if marketplace != 'All':
        dataframe = dataframe[dataframe['marketplace'] == marketplace]
    if category != 'All':
        dataframe = dataframe[dataframe['product_category'] == category]
    if rating != 'All':
        dataframe = dataframe[dataframe['star_rating'] == rating]
    if verified != 'All':
        dataframe = dataframe[dataframe['verified_purchase'] == verified]
    if review_year != 'All':
        dataframe = dataframe[dataframe['review_date'] == review_year]

    return dataframe


def display_dataframe(dataframe):
    """Display the dataframe in the Streamlit app."""
    st.write("Filtered Results:")
    st.dataframe(dataframe)


def main():
    """Main function to render the Streamlit UI components for sentiment analysis."""
    st.title('Amazon Reviews Analysis with Sentiment')

    # Load the dataframe
    df = load_data('df_with_sentiment.csv')
    # df = load_data('ddata/final/df_with_sentiment.csv')
    # Apply user-selected filters and display the results
    filtered_df = apply_filters(df)
    display_dataframe(filtered_df)


if __name__ == "__main__":
    main()
