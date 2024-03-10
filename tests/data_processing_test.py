# tests/data_processing_test.py

import unittest
from unittest.mock import patch
import pandas as pd
# Adjust the import path according to your project structure
from data.data_processing import read_dataset, merge_datasets, remove_specific_columns, modify_review_date_to_year, categorize_votes

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Setup mock data for tests
        self.mock_df = pd.DataFrame({
            'customer_id': [1, 2],
            'review_id': [3, 4],
            'product_id': [5, 6],
            'review_date': ['2020-01-01', '2021-02-02'],
            'helpful_votes': [1, 5],
            'total_votes': [2, 10]
        })

    @patch('sentiment_analysis_with_llm.data_processing.pd.read_csv')
    def test_read_dataset(self, mock_read_csv):
        mock_read_csv.return_value = self.mock_df
        df, error = read_dataset("dummy_path.tsv")
        mock_read_csv.assert_called_once()
        self.assertTrue(df.equals(self.mock_df))
        self.assertEqual(error, "")

    def test_merge_datasets(self):
        # This example assumes you've adapted the merge_datasets function to work with mock data
        pass  # Implement based on your project's specifics

    def test_remove_specific_columns(self):
        df = remove_specific_columns(self.mock_df.copy())
        self.assertNotIn('customer_id', df.columns)
        self.assertNotIn('review_id', df.columns)
        self.assertNotIn('product_id', df.columns)

    def test_modify_review_date_to_year(self):
        df = modify_review_date_to_year(self.mock_df.copy())
        self.assertTrue(all(df['review_date'] == [2020, 2021]))

    def test_categorize_votes(self):
        df = categorize_votes(self.mock_df.copy(), ['helpful_votes', 'total_votes'])
        self.assertIn('helpful_votes_category', df.columns)
        self.assertIn('total_votes_category', df.columns)
        # Add more assertions to check if categorization is correct

if __name__ == '__main__':
    unittest.main()
