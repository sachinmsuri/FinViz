from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from functools import reduce

##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('portfolios', external_stylesheets=external_stylesheets)

def read_ticker_symbols():
    try:
        df_tickers = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)
        df_tickerstats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)
        df = pd.merge(df_tickers, df_tickerstats, how='inner', on='Symbol')

        return df
    except Exception as e:
        print(str(e))

def get_symbols():
    dropdown_options = []
    df = read_ticker_symbols()
    for index, row in df.iterrows():
        dropdown_options.append({'label': row['Name'], 'value': row['Symbol']})
    return dropdown_options
##############################################################################################

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='portfolio_1',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 1",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_2',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 2",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_3',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 3",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_4',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 4",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_5',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 5",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_6',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 6",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_7',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 7",
                style={'backgroundColor': '#1E1E1E'}),
    dcc.Dropdown(id='portfolio_8',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Add Stocks to Portfolio 8",
                style={'backgroundColor': '#1E1E1E'}),
    

    html.Br(),

    html.Button('Create Portfolios', 
                n_clicks = 0,
                id='button', 
                style = {
                'display':'flex', 
                'justifyContent':'center',
                'align-items':'center',
                'margin': 'auto'
                }
    ),

    html.Br(),
    html.Br(),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),

    html.Br(),
])

#Callbacks
@app.callback(
    Output("time-series-chart", "figure"), 
    Input("button", 'n_clicks'),
    State("portfolio_1", "value"),
    State("portfolio_2", "value"),
    State("portfolio_3", "value"),
    State("portfolio_4", "value"),
    State("portfolio_5", "value"),
    State("portfolio_6", "value"),
    State("portfolio_7", "value"),
    State("portfolio_8", "value"),
    )

def time_series_stock(n_clicks, portfolio_1, portfolio_2, portfolio_3, 
                        portfolio_4, portfolio_5, portfolio_6,
                        portfolio_7, portfolio_8):
    #Flatten list
    graphs = []

    fig = {
            'data': graphs,
            'layout': go.Layout(
            paper_bgcolor='rgba(30, 30, 30, 30)',
            plot_bgcolor='rgba(30, 30, 30, 30)',
            autosize=True,
            height = 550,
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
            legend=dict(
                font=dict(
                    color="white"
                    ),
                )
                )
        } 

    #if n_clicks is None:
        #return fig
    #    raise PreventUpdate
    #else:
        #if any(isinstance(i, list) for i in portfolio_1):
        #    ticker_dropdown = [item for elem in portfolio_1 for item in elem]
    if n_clicks > 0:
        user_inputs = {
            'Portfolio 1': portfolio_1,
            'Portfolio 2': portfolio_2,
            'Portfolio 3': portfolio_3,
            'Portfolio 4': portfolio_4,
            'Portfolio 5': portfolio_5,
            'Portfolio 6': portfolio_6,
            'Portfolio 7': portfolio_7,
            'Portfolio 8': portfolio_8,
            }
        filled_user_inputs = {}
        #graphs = []

        for key, value in user_inputs.items():
            if value:
                filled_user_inputs[key] = value

        for key, value in filled_user_inputs.items():
            #Calculate average price of a portfolio
            portfolio_df_lst = []
            for ticker in value:
                share_price_df = obj_iexcloud.get_max_time_series_df(ticker)
                portfolio_df_lst.append(share_price_df)
            portfolio_df = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                    how='outer'), portfolio_df_lst)
            portfolio_df['Portfolio Name'] = key
            portfolio_df['Average Price'] = portfolio_df.mean(axis=1)
            portfolio_df = portfolio_df.sort_values(by="Date")
            print(portfolio_df)

            #Create time-series graph for portfolio
            graphs.append(go.Scatter(
            x = portfolio_df['Date'],
            y = portfolio_df['Average Price'],
            mode = 'lines',
            name = f"{key} - Average Price",
            textposition = 'bottom center',
            ))

            n_clicks = 0
        
    return fig

