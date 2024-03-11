# tests/data_processing_test.py

import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os

# Ensure the script can find the data_processing module by adjusting sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))

from data_processing import (
    read_dataset,
    merge_datasets,
    remove_specific_columns,
    modify_review_date_to_year,
    categorize_votes,
)

class TestDataProcessing(unittest.TestCase):
    """
    This class contains unit tests for the data_processing.py module.
    It tests the functionality of data reading, merging, cleaning,
    and processing to ensure they work as expected.
    """

    def setUp(self):
        """
        Set up method to run before each test case.
        Initializes a mock DataFrame to use in the tests.
        """
        self.mock_df = pd.DataFrame({
            'customer_id': [1, 2],
            'review_id': [3, 4],
            'product_id': [5, 6],
            'review_date': ['2020-01-01', '2021-02-02'],
            'helpful_votes': [1, 5],
            'total_votes': [2, 10],
        })

    @patch('data_processing.pd.read_csv')
    def test_read_dataset(self, mock_read_csv):
        """
        Test the read_dataset function to verify it properly reads data from
        a file path and handles exceptions correctly.
        """
        # Setup the mock to return the mock DataFrame
        mock_read_csv.return_value = self.mock_df
        # Call the function with a dummy file path
        df, error = read_dataset("dummy_path.tsv")
        # Assertions to verify function behavior
        mock_read_csv.assert_called_once_with("dummy_path.tsv", sep='\t', error_bad_lines=False, warn_bad_lines=False)
        self.assertTrue(df.equals(self.mock_df))
        self.assertEqual(error, "")

    @patch('data_processing.read_dataset')
    def test_merge_datasets_all(self, mock_read_dataset):
        """
        Test the merge_datasets function to ensure it correctly merges multiple
        datasets when 'all' is specified as the category.
        """
        mock_dfs = [pd.DataFrame([{'id': i}]) for i in range(4)]
        mock_read_dataset.side_effect = [(df, "") for df in mock_dfs]
        # Call the function with 'all' to merge all datasets
        df, error = merge_datasets('all')
        self.assertEqual(len(df), len(mock_dfs))
        self.assertEqual(error, "")

    def test_remove_specific_columns(self):
        """
        Test the remove_specific_columns function to ensure it correctly removes
        specified columns from the DataFrame.
        """
        df = remove_specific_columns(self.mock_df.copy())
        self.assertNotIn('customer_id', df.columns)
        self.assertNotIn('review_id', df.columns)
        self.assertNotIn('product_id', df.columns)

    def test_modify_review_date_to_year(self):
        """
        Test the modify_review_date_to_year function to verify that it correctly
        modifies the 'review_date' column to retain only the year.
        """
        df = modify_review_date_to_year(self.mock_df.copy())
        self.assertTrue(all(df['review_date'] == [2020, 2021]))

    def test_categorize_votes(self):
        """
        Test the categorize_votes function to check if votes are correctly
        categorized into engagement levels.
        """
        df = categorize_votes(self.mock_df.copy(), ['helpful_votes', 'total_votes'])
        self.assertIn('helpful_votes_category', df.columns)
        self.assertIn('total_votes_category', df.columns)
        # Additional assertions could be added to check the correctness of the categories

if __name__ == '__main__':
    unittest.main()
