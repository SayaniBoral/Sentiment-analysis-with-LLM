import unittest
from unittest.mock import patch
import pandas as pd
from test_streamlit_v2 import read_dataset, merge_datasets, remove_specific_columns, modify_review_date_to_year, categorize_votes, main

class TestStreamlitApp(unittest.TestCase):

    def test_read_dataset_success(self):
        """Test successful dataset read."""
        with patch('pandas.read_csv', return_value=pd.DataFrame({'test': [1, 2, 3]})):
            df, error = read_dataset('dummy_path.tsv')
            self.assertFalse(df.empty)
            self.assertEqual(error, "")

    def test_read_dataset_failure(self):
        """Test failure in reading dataset."""
        with patch('pandas.read_csv', side_effect=Exception("File not found")):
            df, error = read_dataset('nonexistent_path.tsv')
            self.assertTrue(df.empty)
            self.assertIn("File not found", error)

    def test_merge_datasets_all(self):
        """Test merging all datasets."""
        with patch('test_streamlit_v2.read_dataset', side_effect=[
            (pd.DataFrame({'test': [1]}), ""),
            (pd.DataFrame({'test': [2]}), ""),
            (pd.DataFrame({'test': [3]}), ""),
            (pd.DataFrame({'test': [4]}), "")
        ]):
            df, error = merge_datasets('all')
            self.assertEqual(len(df), 4)
            self.assertEqual(error, "")

    def test_merge_datasets_specific(self):
        """Test merging specific dataset."""
        with patch('test_streamlit_v2.read_dataset', return_value=(pd.DataFrame({'test': [1]}), "")):
            df, error = merge_datasets('Gift Card')
            self.assertEqual(len(df), 1)
            self.assertEqual(error, "")

    def test_remove_specific_columns(self):
        """Test removal of specific columns."""
        df = pd.DataFrame({'customer_id': [1], 'review_id': [2], 'product_id': [3], 'data': [4]})
        df = remove_specific_columns(df)
        self.assertNotIn('customer_id', df.columns)
        self.assertNotIn('review_id', df.columns)
        self.assertNotIn('product_id', df.columns)
        self.assertIn('data', df.columns)

    def test_modify_review_date_to_year(self):
        """Test modification of review_date to year."""
        df = pd.DataFrame({'review_date': ['2021-01-01', '2022-02-02']})
        df = modify_review_date_to_year(df)
        self.assertTrue(all(df['review_date'] == [2021, 2022]))

    def test_categorize_votes_no_votes(self):
        """Test categorization of no votes."""
        df = pd.DataFrame({'helpful_votes': [0, 0]})
        df = categorize_votes(df, ['helpful_votes'])
        self.assertTrue(all(df['helpful_votes_category'] == 'No Votes'))

    def test_categorize_votes_engagement(self):
        """Test categorization into engagement levels."""
        df = pd.DataFrame({'helpful_votes': [1, 100]})
        df = categorize_votes(df, ['helpful_votes'])
        self.assertIn('Engagement', df['helpful_votes_category'].unique())

    def test_main_load_data_error(self):
        """Test main function's error handling on data load."""
        with patch('test_streamlit_v2.st.selectbox', return_value='all'), \
             patch('test_streamlit_v2.merge_datasets', return_value=(pd.DataFrame(), "Error")), \
             patch('test_streamlit_v2.st.error') as mock_error:
            main()
            mock_error.assert_called_with("Failed to load dataset: Error")

    def test_main_success(self):
        """Test main function's successful data load and display."""
        with patch('test_streamlit_v2.st.selectbox', return_value='all'), \
             patch('test_streamlit_v2.merge_datasets', return_value=(pd.DataFrame({'data': [1]}), "")), \
             patch('test_streamlit_v2.st.write') as mock_write:
            main()
            mock_write.assert_called()

if __name__ == '__main__':
    unittest.main()
