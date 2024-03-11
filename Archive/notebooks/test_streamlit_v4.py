import streamlit as st
import pandas as pd

def load_data(file_path):
    """Load and return the pre-processed sentiment analysis dataframe."""
    return pd.read_csv(file_path)

def apply_filters(dataframe):
    """Apply user-selected filters to the dataframe and return the filtered dataframe."""
    # Filtering UI
    st.sidebar.header('Filter Options')

    # Ensure 'review_date' is a string for .str operations
    dataframe['review_date'] = dataframe['review_date'].astype(str)

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
        ['All'] + sorted(dataframe['review_date'].str[:4].unique())
    )

    # Apply the filters
    if marketplace != 'All':
        dataframe = dataframe[dataframe['marketplace'] == marketplace]
    if category != 'All':
        dataframe = dataframe[dataframe['product_category'] == category]
    if rating != 'All':
        dataframe = dataframe[dataframe['star_rating'] == int(rating)]
    if verified != 'All':
        dataframe = dataframe[dataframe['verified_purchase'] == verified]
    if review_year != 'All':
        dataframe = dataframe[dataframe['review_date'].str.contains(review_year)]

    return dataframe

def rank_and_select_products(dataframe):
    """Rank products based on criteria and select top and bottom products."""
    # Adjustments for ranking logic
    dataframe['verified_purchase_numeric'] = dataframe['verified_purchase'].apply(lambda x: 1 if x == 'Y' else 0)
    dataframe['polarity_numeric'] = dataframe['polarity'].apply(lambda x: 1 if x == 'positive' else -1)
    # Assuming mappings for 'total_votes_category' and 'helpful_votes_category'
    dataframe['total_votes_category_numeric'] = dataframe['total_votes_category'].apply(lambda x: 1) # Placeholder
    dataframe['helpful_votes_category_numeric'] = dataframe['helpful_votes_category'].apply(lambda x: 1) # Placeholder
    # Composite score calculation
    dataframe['composite_score'] = (dataframe['polarity_numeric'] + dataframe['score'] + dataframe['star_rating']) / 3
    dataframe['verification_score'] = (dataframe['verified_purchase_numeric'] + dataframe['total_votes_category_numeric'] + dataframe['helpful_votes_category_numeric']) / 3
    dataframe['final_ranking_score'] = (dataframe['composite_score'] + dataframe['verification_score']) / 2
    # Sorting based on final ranking score
    dataframe_sorted = dataframe.sort_values(by='final_ranking_score', ascending=False)
    top_products = dataframe_sorted.head(5)
    bottom_products = dataframe_sorted.tail(5)
    return top_products, bottom_products

def display_top_and_bottom_products(top_products, bottom_products):
    """Display the top and bottom products in the Streamlit app."""
    st.write("Top Products:")
    st.dataframe(top_products[['product_title', 'final_ranking_score']])
    st.write("Bottom Products:")
    st.dataframe(bottom_products[['product_title', 'final_ranking_score']])

def main():
    """Main function to render the Streamlit UI components for sentiment analysis."""
    st.title('Amazon Reviews Analysis with Sentiment')

    # Load the dataframe
    df = load_data('df_with_sentiment.csv')

    # Apply user-selected filters and display the results
    filtered_df = apply_filters(df)
    top_products, bottom_products = rank_and_select_products(filtered_df)
    display_top_and_bottom_products(top_products, bottom_products)

if __name__ == "__main__":
    main()
