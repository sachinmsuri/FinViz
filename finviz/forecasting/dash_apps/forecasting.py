from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from forecasting.views import forecast_stock
from forecasting.views import predict_sentiment
from forecasting.views import read_ticker_symbols
from forecasting.views import get_symbols



##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('forecasting', external_stylesheets=external_stylesheets)

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                value = [],
                placeholder="Companies listed on S&P500",
                style={'backgroundColor': '#1E1E1E', 'color': 'black'}),
    
    html.Br(),
        
    html.Div(id="sentiment-score", style={'color': 'white', 'textAlign': 'center'}),

    html.Div([
            html.Div(id="sentiment-score"),
            html.Br(),
            html.Div('0:Negative | 1: Neutral | 2: Positive'),  
            ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between',
                        'color':'white'}
        ),

    html.Br(),

    dcc.Graph(id="forecasting-chart", config={'displayModeBar': False}),

    html.Br(),

    html.Div(id="news-articles"),

    
])

#Callbacks

    
@app.callback(
    Output("forecasting-chart", "figure"), 
    [Input("stockselector", "value")])

def time_series_stock(ticker):
    graphs = []

    if ticker:
        count = 0
        forecasted_df = forecast_stock(ticker)
        for df in forecasted_df:
            forecasted_df = df.rename(columns={'ds': 'Date', 'trend':ticker})

            count += 1
            if count > 1:
                name = f"{ticker} Forecasted"
            else:
                name = f"{ticker}"

            graphs.append(go.Scatter(
                x = forecasted_df['Date'],
                y = forecasted_df[ticker],
                mode = 'lines',
                #name = f"{ticker} Forecasted" ,
                name = name,
                textposition = 'bottom center',
            ))

        #if any(isinstance(i, list) for i in graphs):
        #    graphs = [item for elem in graphs for item in elem]


    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
            autosize=True,
            xaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                'rangeselector': {
                    'buttons':list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=5, label="5y", step="year", stepmode="backward"),
                            dict(step="all")
                            ])
                        }
                    },
            yaxis = {'showgrid':True, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                    },
            yaxis2 = {'showgrid':False, 
                'gridwidth':1, 
                'gridcolor':'Grey',
                'color': 'White',
                'overlaying': 'y',
                'side': 'right'
                    },
            legend=dict(
                font=dict(
                    color="white"
                    ),
                )
            )
        }

    return fig

@app.callback(
    Output("news-articles", "children"), 
    [Input("stockselector", "value")])

def news_articles(ticker):

    news_df = obj_iexcloud.get_news(ticker)

    return dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        style_header={
        'backgroundColor': 'black',
        'color': 'white',
        'textAlign': 'center'
        },
        style_cell={
        'backgroundColor': 'black',
        'color': 'white',
        'textAlign': 'left'
        },
        data=news_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in news_df.columns],
        #columns=[{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'url' else {'id': x, 'name': x} for x in news_df.columns],
    )



@app.callback(
    Output("sentiment-score", "children"), 
    [Input("stockselector", "value")])

def sentiment_score(ticker):
    if ticker:
        sentiment_score = predict_sentiment(ticker)
        string = f'{ticker} Sentiment Score: {sentiment_score}'

    return string
