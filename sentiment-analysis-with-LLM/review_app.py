"""
This module contains the script for visualizing the amazon product review app
"""
import streamlit as st
import pandas as pd


def apply_custom_css():
    """
    Function to apply the css style to streamlit web app
    """
    st.markdown("""
        <style>
        /* Set the overall background color */
        body, .stApp, .stSidebar > div:first-child {
            background-color: #FFA500;  /* Orange background for both main area and sidebar */
        }
        /* Adjust sidebar text color */
        .css-1d391kg, .stSidebar .css-10trblm, .stSidebar .css-1v3fvcr, .stSidebar .css-1kyxreq, .stSidebar .css-hi6a2p {
            color: #000000;  /* Black text for better readability */
        }
        /* Adjustments for dataframe display */
        .stDataFrame {
            background-color: #CCCCCC;  /* Attempt to set a grey background for tables */
        }
        </style>
        """, unsafe_allow_html=True)


def load_data(file_path):
    """Load and return the pre-processed sentiment analysis dataframe."""
    return pd.read_csv(file_path)


def apply_filters(dataframe):
    """Apply user-selected filters to the dataframe and return the filtered dataframe."""
    st.sidebar.header('Filter Options')
    dataframe['review_date'] = dataframe['review_date'].astype(str)

    marketplace = st.sidebar.selectbox('Marketplace:', ['All']
                                       + list(dataframe['marketplace'].unique()))
    category = st.sidebar.selectbox('Product Category:', ['All']
                                    + list(dataframe['product_category'].unique()))
    min_rating, max_rating = int(dataframe['star_rating'].min()), \
    int(dataframe['star_rating'].max())
    rating = st.sidebar.slider('Star Rating:', min_value=min_rating, max_value=max_rating,
                               value=(min_rating, max_rating))
    verified = st.sidebar.selectbox('Verified Purchase:', ['All']
                                    + list(dataframe['verified_purchase'].unique()))
    review_year = st.sidebar.selectbox('Review Year:', ['All']
                                       + sorted(dataframe['review_date'].str[:4].unique()))

    display_scores = st.sidebar.checkbox('Display Scores', value=False)

    if marketplace != 'All':
        dataframe = dataframe[dataframe['marketplace'] == marketplace]
    if category != 'All':
        dataframe = dataframe[dataframe['product_category'] == category]
    dataframe = dataframe[(dataframe['star_rating'] >= rating[0])
                          & (dataframe['star_rating'] <= rating[1])]
    if verified != 'All':
        dataframe = dataframe[dataframe['verified_purchase'] == verified]
    if review_year != 'All':
        dataframe = dataframe[dataframe['review_date'].str.contains(review_year)]

    return dataframe, display_scores


def rank_and_select_products(dataframe):
    """
    This function is used to rank products based on composite sentiment score.
    It returns the top and bottom products
    """
    dataframe['verified_purchase_numeric'] = dataframe['verified_purchase']\
    .apply(lambda x: 1 if x == 'Y' else 0)
    dataframe['polarity_numeric'] = dataframe['polarity']\
    .apply(lambda x: 1 if x == 'positive' else -1)

    dataframe['score'] = (
                                 dataframe['polarity_numeric'] * 2 +
                                 dataframe['score'] * 2 +
                                 dataframe['star_rating'] +
                                 dataframe['helpful_votes'] * 0.5 +
                                 dataframe['total_votes'] * 0.5 +
                                 dataframe['verified_purchase_numeric']
                         ) / 6.0

    grouped_df = dataframe.groupby('product_parent').agg({
        'score': 'mean',
        'product_title': lambda x: x.iloc[0]
    }).reset_index()

    grouped_df_sorted = grouped_df.sort_values(by='score', ascending=False)

    # Adjust the logic to include all products with the same boundary score
    top_cutoff_score = grouped_df_sorted.iloc[4]['score']
    bottom_cutoff_score = grouped_df_sorted.iloc[-5]['score']

    top_products = grouped_df_sorted[grouped_df_sorted['score'] >= top_cutoff_score]
    bottom_products = grouped_df_sorted[grouped_df_sorted['score'] <= bottom_cutoff_score]

    return top_products, bottom_products


def display_products_table(products, display_score, title):
    """Display the products in a table format."""
    st.markdown(f"### {title}")
    if display_score:
        st.dataframe(products[['product_title', 'score']])
    else:
        st.dataframe(products[['product_title']])


def main():
    """
    Main function to call all functions in a pipeline
    """
    apply_custom_css()
    st.title('Amazon Reviews Analysis with Sentiment')

    df = load_data('df_with_sentiment.csv')  # Make sure this path is correct
    filtered_df, display_scores = apply_filters(df)
    top_products, bottom_products = rank_and_select_products(filtered_df)
    display_products_table(top_products, display_scores, "Top Products")
    display_products_table(bottom_products, display_scores, "Bottom Products")

    st.markdown("""
        Note: If more than 5 products share the same score, all of those products will be displayed. 
                Double click to see the entire row.
                """)


if __name__ == "__main__":
    main()
