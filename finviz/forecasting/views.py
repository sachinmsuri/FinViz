from iexcloud.iexcloud import iexCloud
import pandas as pd
import numpy as np
import nltk
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from prophet import Prophet

from django.shortcuts import render

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


# Create your views here.

def forecasting(request):
    return render(request, 'forecasting.html', {})

#Function to clean data before calculating sentiment score
def clean_data(df, test):
    #turn all letters to lowercase
    df['sentence'] = df['sentence'].str.lower()

    #normalise text data & remove numbers
    df["sentence"] = df['sentence'].str.replace(
            "(@\[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?",''
        )

    #Remove stop words
    df['sentence'] = df['sentence'].apply(
            lambda x: ' '.join([word for word in x.split() if word not in (stop_words)])
        )

    #df['sentence (format)'] = df['sentence'].str.split(" ")
    #df['sentence (stemmed)'] = df['sentence (format)'].apply(lambda x: [stemmer.stem(y) for y in x])
    #df = df.drop(['sentence (format)'], axis=1)

    #df['sentence stemmed'] = df['sentence'].apply(lambda x: ''.join([str(elem) for elem in x]))
    #df = df.drop(['sentence (stemmed)'], axis=1)

    if not test:
        sentiment_score = {
            'neutral': 0,
            'negative': -1,
            'positive': 1
        }

        df['sentiment'] = df['sentiment'].replace(sentiment_score)
        df.columns = df.columns.str.replace(" ", "")
    
        df = df.drop(['sentiment'], axis=1)
        
    return df

def fit_model(data):
    df = pd.read_csv(data, encoding='ISO-8859-1', names=['sentiment', 'sentence'])

    df = clean_data(df, True)
    print(df)

    tfidf = TfidfVectorizer(max_features = 5000)

    x = df['sentence']
    y = df['sentiment']

    x = tfidf.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        random_state=1,
        test_size =0.2,
        shuffle=True
    )

    clf = LinearSVC()
    clf.fit(x_train, y_train)

    return clf, x, tfidf

def predict_sentiment(ticker):
    clf, x, tfidf = fit_model(r'all-data.csv')

    iex = iexCloud()
    news_df = iex.get_news(ticker)
    news_df = news_df.rename(columns={'headline': 'sentence'})

    news_df = clean_data(news_df, True)

    x = tfidf.transform(news_df['sentence'])
    y_pred = clf.predict(x)

    sentiment_count = {
        0: 0,
        1: 0,
        2: 0
    }

    for sentiment in y_pred:
        if sentiment == 'neutral':
            sentiment_count[1] += 1
        if sentiment == 'positive':
            sentiment_count[2] += 1
        if sentiment == 'negative':
            sentiment_count[0] += 1 

    print(sentiment_count)
    weighted_average = (
        (sentiment_count[1] * 1 +
        sentiment_count[2] * 2 +
        sentiment_count[0] * 0) / 100
    )

    return weighted_average




