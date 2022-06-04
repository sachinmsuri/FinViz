from iexcloud.iexcloud import iexCloud
from parameters import engine_string
from db_ingestion.models import Tickers
import pandas as pd
#import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

##############################################################################################
#Parameters and instantiating classes
obj_iexcloud = iexCloud()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('searchstocks', external_stylesheets=external_stylesheets)

def read_ticker_symbols():
    try:
        df_tickers = pd.read_sql('SELECT * FROM db_ingestion_tickers;', engine_string)
        df_tickerstats = pd.read_sql('SELECT * FROM db_ingestion_tickerstats', engine_string)
        df = pd.merge(df_tickers, df_tickerstats, how='inner', on='Symbol')
        
        # #Format Market Capitalisation
        # df['Market Capitalization Ranges'] = 'Placeholder'
        # df.loc[(df['Market Capitalization'] <= 250000000), 'Market Capitalization Ranges'] = '$0 - $250Million'
        # df.loc[(df['Market Capitalization'] >= 250000000) & (df['Market Capitalization'] <= 500000000), 'Market Capitalization Ranges'] = '$250Million - $500Million'
        # df.loc[(df['Market Capitalization'] >= 500000000) & (df['Market Capitalization'] <= 1000000000), 'Market Capitalization Ranges'] = '$500Million - $1Billion'
        # df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 10000000000), 'Market Capitalization Ranges'] = '$1Billion - $10Billion'
        # df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 50000000000), 'Market Capitalization Ranges'] = '$10Billion - $50Billion'
        # df.loc[(df['Market Capitalization'] >= 5000000000) & (df['Market Capitalization'] <= 100000000000), 'Market Capitalization Ranges'] = '$50Billion - $100Billion'
        # df.loc[(df['Market Capitalization'] >= 100000000000) & (df['Market Capitalization'] <= 500000000000), 'Market Capitalization Ranges'] = '$100Billion - $500Billion'
        # df.loc[(df['Market Capitalization'] >= 500000000000), 'Market Capitalization Ranges'] = 'Greater than $500Billion'

        # #Format Dividend
        # df['Dividend Ranges'] = 'Placeholder'
        # df.loc[(df['Dividend'] <= 0), 'Dividend Ranges'] = '0%'
        # df.loc[(df['Dividend'] >= 0) & (df['Dividend'] <= 0.01), 'Dividend Ranges'] = '0% - 1%'
        # df.loc[(df['Dividend'] >= 0.01) & (df['Dividend'] <= 0.025), 'Dividend Ranges'] = '1% - 2.5%'
        # df.loc[(df['Dividend'] >= 0.025) & (df['Dividend'] <= 0.05), 'Dividend Ranges'] = '2.5% - 5%'
        # df.loc[(df['Dividend'] >= 0.05) & (df['Dividend'] <= 0.075), 'Dividend Ranges'] = '5% - 7.5%'
        # df.loc[(df['Dividend'] >= 0.075) & (df['Dividend'] <= 0.1), 'Dividend Ranges'] = '7.5% - 10%'
        # df.loc[(df['Dividend'] >= 0.1) & (df['Dividend'] <= 0.15), 'Dividend Ranges'] = '10% - 15%'
        # df.loc[(df['Dividend'] >= 0.15) & (df['Dividend'] <= 0.2), 'Dividend Ranges'] = '15% - 20%'
        # df.loc[(df['Dividend'] >= 2), 'Dividend Ranges'] = 'Greater than 20%'

        # #Format Dividend
        # df['PE Ratio Ranges'] = 'Placeholder'
        # df.loc[(df['PE Ratio'] <= -10), 'PE Ratio Ranges'] = 'Less than -10'
        # df.loc[(df['PE Ratio'] >= -10) & (df['PE Ratio'] <= 0), 'PE Ratio Ranges'] = '-10 - 0'
        # df.loc[(df['PE Ratio'] >= 0) & (df['PE Ratio'] <= 10), 'PE Ratio Ranges'] = '0 - 10'
        # df.loc[(df['PE Ratio'] >= 10) & (df['PE Ratio'] <= 20), 'PE Ratio Ranges'] = '10 - 20'
        # df.loc[(df['PE Ratio'] >= 20) & (df['PE Ratio'] <= 30), 'PE Ratio Ranges'] = '20 - 30'
        # df.loc[(df['PE Ratio'] >= 30) & (df['PE Ratio'] <= 40), 'PE Ratio Ranges'] = '30 - 40'
        # df.loc[(df['PE Ratio'] >= 40) & (df['PE Ratio'] <= 50), 'PE Ratio Ranges'] = '40 - 50'
        # df.loc[(df['PE Ratio'] >= 50) & (df['PE Ratio'] <= 75), 'PE Ratio Ranges'] = '50 - 75'
        # df.loc[(df['PE Ratio'] >= 75) & (df['PE Ratio'] <= 100), 'PE Ratio Ranges'] = '75 - 100'
        # df.loc[(df['PE Ratio'] >= 100), 'PE Ratio Ranges'] = 'Greater than 100'

        # #Format Revenue
        # df['Revenue Ranges'] = 'Placeholder'
        # df.loc[(df['Revenue'] <= 250000000), 'Revenue Ranges'] = '$0 - $250Million'
        # df.loc[(df['Revenue'] >= 250000000) & (df['Revenue'] <= 500000000), 'Revenue Ranges'] = '$250Million - $500Million'
        # df.loc[(df['Revenue'] >= 500000000) & (df['Revenue'] <= 1000000000), 'Revenue Ranges'] = '$500Millionn- $1Billion'
        # df.loc[(df['Revenue'] >= 1000000000) & (df['Revenue'] <= 10000000000), 'Revenue Ranges'] = '$1Billion - $10Billion'
        # df.loc[(df['Revenue'] >= 10000000000) & (df['Revenue'] <= 50000000000), 'Revenue Ranges'] = '$10Billion - $50Billion'
        # df.loc[(df['Revenue'] >= 50000000000) & (df['Revenue'] <= 100000000000), 'Revenue Ranges'] = '$50Billion - $100Billion'
        # df.loc[(df['Revenue'] >= 100000000000), 'Revenue Ranges'] = 'Greater than $100Billion'
        # #243,198,000

        # #Format EBITDA
        # df['EBITDA Ranges'] = 'Placeholder'
        # df.loc[(df['EBITDA'] < -100000000), 'EBITDA Ranges'] = 'Less than -$100Million'
        # df.loc[(df['EBITDA'] < -100000000) & (df['EBITDA'] <= -50000000), 'EBITDA Ranges'] = '-$100Million- -$50Million'
        # df.loc[(df['EBITDA'] >= -50000000) & (df['EBITDA'] <= 0), 'EBITDA Ranges'] = '-$50Million - $0'
        # df.loc[(df['EBITDA'] >= 0) & (df['EBITDA'] <= 250000000), 'EBITDA Ranges'] = '$0 - $250Million'
        # df.loc[(df['EBITDA'] >= 250000000) & (df['EBITDA'] <= 500000000), 'EBITDA Ranges'] = '$250Million - $500Million'
        # df.loc[(df['EBITDA'] >= 500000000) & (df['EBITDA'] <= 1000000000), 'EBITDA Ranges'] = '$500Million - $1Billion'
        # df.loc[(df['EBITDA'] >= 1000000000) & (df['EBITDA'] <= 10000000000), 'EBITDA Ranges'] = '$1Billion - $10Billion'
        # df.loc[(df['EBITDA'] >= 10000000000), 'EBITDA Ranges'] = 'Greater than $10Billion'

        return df
    except Exception as e:
        print(str(e))

def get_symbols():
    dropdown_options = []
    df = read_ticker_symbols()
    for index, row in df.iterrows():
        dropdown_options.append({'label': row['Name'], 'value': row['Symbol']})
    return dropdown_options

def get_sectors():
    dropdown_options = []
    df = read_ticker_symbols()
    sector_lst = list(df['Sector'].unique())
    for i in sector_lst:
        dropdown_options.append({'label':i, 'value':i})
    return dropdown_options

def dropdown_values(column_name):
    dropdown_options = []
    df = read_ticker_symbols()
    lst = list(df[column_name].unique())
    for i in lst:
        dropdown_options.append({'label':i, 'value':i})
    return dropdown_options

def colormap_value(table_name, range):
    try:
        df_colormaps = pd.read_sql(f'SELECT * FROM db_ingestion_{table_name}_colormaps;', engine_string)
        df_colormaps = df_colormaps[df_colormaps['Metric'] == range]
        print(df_colormaps)

        color = df_colormaps['Color'].iloc[0]
        return color
    except Exception as e:
        print(str(e))

def stock_information(ticker, metric):
    df_tickerstats = pd.read_sql(f'SELECT * FROM db_ingestion_tickerstats', engine_string)
    df_tickerstats = df_tickerstats[df_tickerstats['Symbol'] == ticker]

    if metric == 'marketcap':
        updated_metric = 'Market Capitalization Ranges'
    if metric == 'dividend':
        updated_metric = 'Dividend Ranges'
    if metric == 'ebitda':
        updated_metric = 'EBITDA Ranges'
    if metric == 'peratio':
        updated_metric = 'PE Ratio Ranges'
    if metric == 'revenue':
        updated_metric = 'Revenue Ranges'


    range = df_tickerstats[updated_metric].iloc[0]

    return range


def get_company_stats():
    try:
        df = pd.read_sql(f'SELECT * FROM db_ingestion_tickerstats', engine_string)
    except Exception as e:
        print(str(e))

    return df



##############################################################################################

#App layout
app.layout = html.Div([
    dcc.Dropdown(id='stockselector',
                options=get_symbols(),
                multi=True,
                value = [],
                clearable = True,
                placeholder="Companies listed on S&P500",
                style={'backgroundColor': '#1E1E1E'}),
    
    dcc.Dropdown(id='sectorselector',
                options=get_sectors(),
                multi=True,
                clearable = True,
                value = [],
                placeholder="Sectors listed on S&P500",
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),

    dcc.RadioItems(
        id='colormap',
        options=[
            {'label': 'Market Capitalization Ranges', 'value': 'marketcap'},
            {'label': 'Dividend Ranges', 'value': 'dividend'},
            {'label': 'PE Ratio Ranges', 'value': 'peratio'},
            {'label': 'Revenue Ranges', 'value': 'revenue'},
            {'label': 'EBITDA Ranges', 'value': 'ebitda'},
            {'label': 'None', 'value': 'none'}
        ],
        inline=True,
        value='none',
        style={"color": "white"},
    ),

    dcc.Graph(id="time-series-chart", config={'displayModeBar': False}),

    html.Br(),


    html.Button('Update Graphh', 
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

    dcc.Dropdown(id='marketcap_selector',
                options=[
                    {'label': "0 - $250Millon", 'value': "0 - $250Million"},
                    {'label': "$250Million - $500Million", 'value': "$250Million - $500Million"},
                    {'label': "$500Million - $1Billion", 'value': "$500Million - $1Billion"},
                    {'label': '$1Billion - $10Billion', 'value': '$1Billion - $10Billion'},
                    {'label': '$10Billion - $50Billion', 'value': '$10Billion - $50Billion'},
                    {'label': '$50Billion - $100Billion', 'value': '$50Billion - $100Billion'},
                    {'label': '$100Billion - $500Billion', 'value': '$100Billion - $500Billion'},        
                    {'label': 'Over $500Billion ', 'value': 'Over $500Billion'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Market Capitalization",
                searchable=True,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='dividend_selector',
                options=[
                    {'label': '0% - 1%', 'value': '0% - 1%'},
                    {'label': '1% - 2.5%', 'value': '1% - 2.5%'},
                    {'label': '2.5% - 5%', 'value': '2.5% - 5%'},
                    {'label': '5% - 7.5%', 'value': '5% - 7.5%'},
                    {'label': '7.5% - 10%', 'value': '7.5% - 10%'},
                    {'label': '10% - 15%', 'value': '10% - 15%'},
                    {'label': '15% - 20%', 'value': '15% - 20%'},
                    {'label': 'Greater than 20%', 'value': 'Greater than 20%'},

                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Dividend Yield",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),
    
    dcc.Dropdown(id='pe_selector',
                options=[
                    {'label': 'Less than -10', 'value': 'Less than -10'},
                    {'label': '-10 - 0', 'value': '-10 - 0'},
                    {'label': '0 - 10', 'value': '0 - 10'},
                    {'label': '10 - 20', 'value': '10 - 20'},
                    {'label': '20 - 30', 'value': '20 - 30'},
                    {'label': '30 - 40', 'value': '30 - 40'},
                    {'label': '40 - 50', 'value': '40 - 50'},
                    {'label': '50 - 75', 'value': '50 - 75'},
                    {'label': '75 - 100', 'value': '75 - 100'},
                    {'label': 'Greater than 100', 'value': 'Greater than 100'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by PE Ratio Scores",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='revenue_selector',
                options=[
                    {'label': '$0 - $250Million', 'value': '$0 - $250Million'},
                    {'label': '$250Million - $500Million', 'value': '$250Million - $500Million'},
                    {'label': '$500Million - $1Billion', 'value': '$500Million - $1Billion'},
                    {'label': '$1Billion - $10Billion', 'value': '$1Billion - $10Billion'},
                    {'label': '$10BBillion - $50Billion', 'value': '$10Billion - $50Billion'},
                    {'label': '$50Billion - $100Billion', 'value': '$50Billion - $100Billion'},
                    {'label': 'Greater than $100Billion', 'value': 'Greater than $100Billion'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Revenue",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),

    html.Br(),

    dcc.Dropdown(id='ebitda_selector',
                options=[
                    {'label': 'Less than -$100Million', 'value': 'Less than -$100Million'},
                    {'label': '-$100Million - -$50Million', 'value': '-$100Million - -$50Million'},
                    {'label': '-$50Million - $0', 'value': '-$50Million - $0'},
                    {'label': '$0 - $250Million', 'value': '$0 - $250Million'},
                    {'label': '$250Million - $500Million', 'value': '$250Million - $500Million'},
                    {'label': '$500Million - $1Billion', 'value': '$500Million - $1Billion'},
                    {'label': '$1Billion - $10Billion', 'value': '$1Billion - $10Billion'},
                    {'label': 'Greater than $10Billion', 'value': 'Greater than $10Billion'},
                ],
                multi=True,
                clearable = True,
                value = [],
                placeholder="Filter Sectors by Earnings (EBITDA)",
                searchable=False,
                style={'backgroundColor': '#1E1E1E'}),
    
    html.Br(),

    dcc.Graph(id="value-finder", config={'displayModeBar': False}),

])

#Callbacks
@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("button", 'n_clicks'),
    Input("stockselector", "value"),
    Input("sectorselector", "value"),
    Input("marketcap_selector", "value"),
    Input("dividend_selector", "value"),
    Input("pe_selector", "value"),
    Input("revenue_selector", "value"),
    Input("ebitda_selector", "value"),
    Input("colormap", "value")]
    )

def time_series_stock(n_clicks, ticker_dropdown, sector_dropdown, marketcap_selector, 
                        dividend_selector, pe_selector, revenue_selector,
                        ebitda_selector, colormap):

    graphs = []


    if n_clicks > 0:


        #Flatten list
        if any(isinstance(i, list) for i in ticker_dropdown):
            ticker_dropdown = [item for elem in ticker_dropdown for item in elem]

        #graphs = []

        #Draw time series of a single stock
        for ticker in ticker_dropdown:
            stock_df = obj_iexcloud.get_max_time_series_df(ticker)
            graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df[ticker],
                mode = 'lines',
                name = ticker,
                textposition = 'bottom center',
            ))

        parameters = {
            'Market Capitalization Ranges': marketcap_selector,
            'Dividend Ranges': dividend_selector,
            'PE Ratio Ranges': pe_selector,
            'Revenue Ranges': revenue_selector,
            'EBITDA Ranges': ebitda_selector
        }
        filled_parameters = {}
        for key, value in parameters.items():
            if value:
                filled_parameters[key] = value

        #Draw time series of sectors and filter
        sector_df = read_ticker_symbols()
        sector_df = sector_df[sector_df['Sector'].isin(sector_dropdown)]
        print(sector_df)
        #if marketcap_dropdown:
        for key in  filled_parameters:
            #sector_df = sector_df.loc[(sector_df['Market Capitalization Ranges'].isin(marketcap_dropdown))]
            sector_df = sector_df.loc[(sector_df[key].isin(filled_parameters[key]))]
        stock_list = list(sector_df['Symbol'])
        for stock in stock_list:
            stock_df = obj_iexcloud.get_max_time_series_df(stock)
            #Choose color based on metric
            if colormap == 'none':
                graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df[stock],
                mode = 'lines',
                name = stock,
                textposition = 'bottom center',
                ))
            else:
                metric = colormap
                range = stock_information(stock, metric)
                color = colormap_value(metric, range)

                graphs.append(go.Scatter(
                x = stock_df['Date'],
                y = stock_df[stock],
                mode = 'lines',
                name = stock,
                textposition = 'bottom center',
                line=dict(color=f'#{color}'),
                ))

        if any(isinstance(i, list) for i in graphs):
            graphs = [item for elem in graphs for item in elem]
        
        n_clicks = 0

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

    return fig



@app.callback(
    Output("value-finder", "figure"), 
    [Input("stockselector", "value"),
    Input("sectorselector", "value")]
    #Input("marketcap_selector", "value"),
    #Input("dividend_selector", "value"),
    #Input("pe_selector", "value"),
    #Input("revenue_selector", "value"),
    #Input("ebitda_selector", "value")]
    )

def value_finder(ticker_dropdown, sector_dropdown):

    #Flatten list
    if any(isinstance(i, list) for i in ticker_dropdown):
        ticker_dropdown = [item for elem in ticker_dropdown for item in elem]

    value_finder_df = read_ticker_symbols()
    value_finder_df['value'] = ((value_finder_df['Share Price'] -
                                value_finder_df['200 Day MA']) / value_finder_df['Share Price']) * 100
    
    value_finder_df = value_finder_df[value_finder_df['Symbol'].isin(ticker_dropdown)]

    fig = px.bar(value_finder_df, x="Symbol", y="value", 
                color="Symbol")

    if sector_dropdown:
        if any(isinstance(i, list) for i in sector_dropdown):
            sector_dropdown = [item for elem in sector_dropdown for item in elem]

        value_finder_df = read_ticker_symbols()
        value_finder_df['value'] = ((value_finder_df['Share Price'] -
                                    value_finder_df['200 Day MA']) / value_finder_df['Share Price']) * 100
        
        value_finder_df = value_finder_df[value_finder_df['Sector'].isin(sector_dropdown)]

        
        #df_metrics = get_company_stats()

        #value_finder_df = pd.merge(value_finder_df, df_metrics[['Symbol', 'PE Ratio Ranges']], how='left', on='Symbol')

        fig = px.bar(value_finder_df, 
                    x="Symbol", 
                    y="value", 
                    #color="PE Ratio Ranges",
                    color="Symbol",

                    )
    
    if not sector_dropdown and not ticker_dropdown:
        value_finder_df = read_ticker_symbols()
        value_finder_df['value'] = ((value_finder_df['Share Price'] -
                                    value_finder_df['200 Day MA']) / value_finder_df['Share Price']) * 100

        value_finder_df = value_finder_df.sort_values(by=['value'])
        value_finder_df = value_finder_df.head(15)

        fig = px.bar(value_finder_df, 
                    x="Symbol", 
                    y="value", 
                    #color="PE Ratio Ranges",
                    color="Sector",
                    )

        
    fig.update_layout(autosize=True, 
                    height=450, 
                    paper_bgcolor='rgba(30, 30, 30, 30)',
                    plot_bgcolor='rgba(30, 30, 30, 30)',
                    xaxis = {'showgrid':True, 
                            'gridwidth':1, 
                            'gridcolor':'Grey',
                            'color': 'White'},
                    yaxis = {'showgrid':True, 
                            'gridwidth':1, 
                            'gridcolor':'Grey',
                            'color': 'White'},
                    legend=dict(
                    font=dict(
                        color="white"
                    ),
                )
            )
    
    return fig
    