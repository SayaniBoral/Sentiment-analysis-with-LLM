import pytest
import pandas as pd
from review_app import rank_and_select_products  # Ensure this import matches the location of your function

@pytest.fixture
def sample_dataframe():
    # Load a smaller sample from the CSV for testing
    df = pd.read_csv('df_with_sentiment.csv').sample(n=50, random_state=1)  # Ensure reproducibility with random_state
    # Assuming the CSV already has 'verified_purchase', 'polarity', 'star_rating', 'helpful_votes', 'total_votes', and 'score' columns
    # If not, you would need to add or adjust these columns here similar to the previous example
    return df

def test_rank_and_select_products_functionality(sample_dataframe):
    top_products, bottom_products = rank_and_select_products(sample_dataframe)
    assert not top_products.empty and not bottom_products.empty, "Top or bottom products should not be empty."
    assert len(top_products) >= 5 and len(bottom_products) >= 5, "Should have at least 5 top and 5 bottom products."

def test_empty_dataframe():
    # Ensure the dataframe structure matches your function's expectations
    df = pd.DataFrame(columns=['verified_purchase', 'polarity', 'star_rating', 'helpful_votes', 'total_votes', 'score', 'product_parent', 'product_title'])
    top_products, bottom_products = rank_and_select_products(df)
    assert top_products.empty and bottom_products.empty, "Top and bottom products should be empty for an empty dataframe."

def test_less_than_ten_products(sample_dataframe):
    small_df = sample_dataframe.iloc[:9].copy()  # Take a smaller sample and use copy to avoid SettingWithCopyWarning
    top_products, bottom_products = rank_and_select_products(small_df)
    assert not top_products.empty or not bottom_products.empty, "Should return results even with less than ten products."

def test_boundary_scores_inclusion(sample_dataframe):
    df = sample_dataframe.iloc[:15].copy()  # Adjust to ensure controlled testing conditions
    # Set scores to create a clear boundary; adjust as necessary based on your scoring logic
    df.loc[:4, 'score'] = 5  # Top scores
    df.loc[10:, 'score'] = 1  # Bottom scores
    # You might need to adjust the 'score' calculations within your function for this test to be meaningful
    top_products, bottom_products = rank_and_select_products(df)
    assert len(top_products) >= 5, "Should include all products with top boundary scores."
    assert len(bottom_products) >= 5, "Should include all products with bottom boundary scores."

# Ensure you run these tests after adjusting them to match your data and logic
