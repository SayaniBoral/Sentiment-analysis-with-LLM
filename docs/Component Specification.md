
# COMPONENT SPECFICATION for SENTIMENT ANALYSIS USING LLMs

## Software components

The below diagram describes the architecture components of our project

![Component Diagram ](<Sentiment Analysis using Llama2.png>)

__Input Datasets__ - We have 3 input data files in .tsv format. They will be merged to create a single dataframe containing raw data. Further processing will be done to keep only the required features. We will be using python packages like pandas and numpy to do the basic cleaning and transformation.

__Llama2-7b-chat model__ - This is the LLM from Meta which we will be using for sentiment analysis task. It will add 2 more columns to our dataset: sentiment and polarity score. This model is gated model and can be accessed here : https://huggingface.co/meta-llama/Llama-2-7b-chat 

__Streamlit app__ - This will be the user interface of our application. The user will be able to search for a product category and get back top 5 and bottom 5 products based on the review sentiments. We are planning to show a visualization of the top 5 products and we can build it using matplotlib.

## Interaction Diagram (User Experience flow)

We can see the interaction diagram/ user experience flow below:
![Interaction Flow](<Interaction flow.png>)

