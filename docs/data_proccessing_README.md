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
