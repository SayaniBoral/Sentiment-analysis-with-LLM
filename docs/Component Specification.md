
# COMPONENT SPECFICATION for SENTIMENT ANALYSIS USING LLMs

## Software components. 
High level description of the software components such as: data manager, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and visualization manager, which displays data frames as a plot. Describe at least 3 components specifying: what it does, inputs it requires, and outputs it provides. If you have more significant components in your system, we highly suggest documenting those as well.

The below diagram describes the architecture components of our project
[embed]/Sentiment Analysis using Llama2.pdf/[embed]

__Input Datasets__ - We have 3 input data files in .tsv format. They will be merged to create a single dataframe containing raw data. Further processing will be done to keep only the required features.

__Llama2-7b-chat model__ - This is the LLM from Meta which we will be using for sentiment analysis task. It will add 2 more columns to our dataset: sentiment and polarity score.

__Streamlit app__ - This will be the user interface of our application. The user will be able to search for a product category and get back top 10 and bottom 10 products based on the review sentiments.

## Interaction Diagram (User Experience flow)
Interactions to accomplish use cases. Describe how the above software components interact to accomplish your use cases. Include at least one interaction diagram.