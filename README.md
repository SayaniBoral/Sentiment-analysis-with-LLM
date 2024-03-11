# Sentiment-analysis-with-LLM

## Project Overview
This project aims to leverage the capabilities of Large Language Models (LLMs) to conduct sentiment analysis on customer reviews. Our primary objective is to understand the sentiment embedded in the feedback provided by customers on various platforms about our product/service. Through this analysis, we intend to gain insights into customer satisfaction, preferences, and expectations to improve our offerings and address any potential issues.

## Project Type
This initiative is an analytical project focused on exploring the sentiment analysis capabilities of LLMs. We will utilize advanced LLMs to interpret and classify the sentiments expressed in customer reviews, categorizing them into positive, negative, and neutral sentiments.


## Directory Struc
-- Need to ADD


## Project Goal
The goal of this project is to produce a comprehensive sentiment analysis report detailing the sentiments expressed in customer reviews. This report will include:

- Quantitative metrics summarizing the overall sentiment distribution.
- Qualitative insights into the themes and trends observed within the feedback.
- Understanding the top 5 positive and negative products per product category
- Recommendations for addressing areas of concern highlighted by negative sentiments.
- Additionally, we aim to develop a sentiment analysis model or tool that can automate the process of categorizing customer sentiments for ongoing analysis and monitoring.

## Data Sources
We utilized the Amazon reviews dataset as mentioned in Kaggle: https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset

There are product reviews for multiple product categories. We chose datasets of these 4 categories:
- Electronics
- Major Appliances
- Shoes 
- Gift Card

## Features
- **Data Processing**: The engine processes Amazon review datasets by merging them based on product categories, removing specific columns (customer ID, review ID, product ID), modifying the review date to only retain the year, and categorizing `helpful_votes` and `total_votes` into engagement levels for deeper analysis.

- **User Interaction**: Users interact with the engine through input prompts, allowing them to specify preferences for:
  - Product categories (Gift Card, Major Appliances, Shoes, Electronics, or All)
  - Variables of interest for analysis (`marketplace`, `product_title`, `product_category`, `star_rating`, `vine`, `verified_purchase`, `review_headline`, `review_body`, `review_date`, and engagement levels for `helpful_votes` and `total_votes`)
  - Engagement levels for reviews based on `helpful_votes` and `total_votes` (Minimal Engagement, Low Engagement, Moderate Engagement, High Engagement, or No Votes for reviews without votes)

- **Engagement Level Categorization**: `helpful_votes` and `total_votes` are categorized into four engagement levels: Minimal Engagement, Low Engagement, Moderate Engagement, High Engagement. A special category, 'No Votes', is introduced for reviews without votes, allowing for nuanced analysis of user engagement with products.

## How to Use

1. **Select a Product Category**: At the start, users are prompted to select a product category. They can choose from specific categories like Gift Card, Major Appliances, Shoes, Electronics, or opt for analyzing all categories combined.

2. **Variable Selection**: Users are then prompted to select variables they're interested in analyzing. This step allows users to tailor the analysis to specific aspects of the review data, such as focusing on products with a certain star rating or within a particular category.

3. **Engagement Level Selection**: Users can also choose to filter reviews based on engagement levels derived from `helpful_votes` and `total_votes`. This feature enables users to focus on reviews with varying degrees of perceived helpfulness or engagement from the Amazon customer base.

4. **Review and Analyze**: After making their selections, the script filters the dataset accordingly and displays the filtered dataset. This allows users to review and analyze the data based on their specific criteria, facilitating informed decision-making or further data exploration.

# How to use this project?

1. Download the necessary raw files from this URL:
2. Run the data_processing.py file to merge 4 raw data files, perform data manipulation and sampling to reduce dataset size
3. Upload the reduced dataset and Sentiment_Analysis_using_llama2.ipynb to Google Colab Enterprise to run the LLM and generate sentiment polarity and scores. Once processed, download the csv: df_with_sentiments.csv
4. To view the final application, run the following code from your terminal: 
streamlit run test_streamlit_v5.py