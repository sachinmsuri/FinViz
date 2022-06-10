
# FinViz

This is a repository containing the code for FinViz.

FinViz is an analytics web application developed in Django to help retail investors visualise financial markets, allowing investors to build a variety of investment stategies and test these strategies against each other.


# How to Run Code

1. Install all requirements from the requirements.txt file into a virtual environment.

2. You will need an IEX Cloud account to generate the API credentials. After you have generated the credentials save the credentials in a file called iexcloud_keys.json within the iexcloud directory.

3. Download the file called all-data.csv from the <a href=https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news > this Kaggle link</a> and save the CSV file in the forcasting directory.


4. Move into the finviz directory and in the terminal type:

```
Python manage.py runserver

```

N.B Python 3.8 was used for the development of this project.



