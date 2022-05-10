from django.core.management.base import BaseCommand
from db_ingestion.models import Marketcap_colormaps
from db_ingestion.models import Dividend_colormaps
from db_ingestion.models import Peratio_colormaps
from db_ingestion.models import Revenue_colormaps
from db_ingestion.models import Ebitda_colormaps
from sqlalchemy import create_engine
import pandas as pd
from parameters import engine_string
from iexcloud.iexcloud import iexCloud
import random

class Command(BaseCommand):
    help = "A command to add color maps to the database"

    def handle(self, *args, **options):
        try:
            #color_lst = ["#41bbc5", "#d10f55", "#66de78", "#d06440", "#a6c363", "#5756a0", "#c8b0d4", "#3e727b", "#f8ba7c", "#428621"]
            color_lst = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
            color_1 = "636EFA"
            color_2 = "EF553B"
            color_3 = "00CC96"
            color_4 = "AB63FA"
            color_5 = "FFA15A"
            color_6 = "19D3F3"
            color_7 = "FF6692"
            color_8 = "B6E880"
            color_9 = "FF97FF"
            color_10 = "FECB52"


            #UPLOAD MARKET CAP COLOR MAP DATA
            marketcap_data = [['$0 - $250Million', color_1], 
                            ['$250Million - $500Million', color_2], 
                            ['$500Million - $1Billion', color_3],
                            ['$1Billion - $10Billion', color_4],
                            ['$10Billion - $50Billion', color_5],
                            ['$50Billion - $100Billion', color_6],
                            ['$100Billion - $500Billion', color_7],
                            ['Greater than $500Billion', color_8]]

            marketcap_df = pd.DataFrame(marketcap_data, columns = ['Metric', 'Color'])
            print(marketcap_df)

            engine = create_engine(engine_string)   
            marketcap_df.to_sql(Marketcap_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

            
            #UPLOAD DIVIDEND COLOR MAP DATA
            dividend_data = [['0%', color_1], 
                            ['0% - 1%', color_2], 
                            ['1% - 2.5%', color_3],
                            ['2.5% - 5%', color_4],
                            ['5% - 7.5%', color_5],
                            ['7.5% - 10%', color_6],
                            ['10% - 15%', color_7],
                            ['15% - 20%', color_8],
                            ['Greater than 20%', color_9]]

            dividend_df = pd.DataFrame(dividend_data, columns = ['Metric', 'Color'])
            print(dividend_df)

            engine = create_engine(engine_string)   
            dividend_df.to_sql(Dividend_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

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

            
            #UPLOAD PE RATIO COLOR MAP DATA
            peratio_data = [['Less than -10', color_1], 
                            ['-10 - 0', color_2], 
                            ['0 - 10', color_3],
                            ['10 - 20', color_4],
                            ['20 - 30', color_5],
                            ['30 - 40', color_6],
                            ['40 - 50', color_7],
                            ['50 - 75', color_8],
                            ['75 - 100', color_9],
                            ['Greater than 100', color_10]]

            peratio_df = pd.DataFrame(peratio_data, columns = ['Metric', 'Color'])
            print(peratio_df)

            engine = create_engine(engine_string)   
            peratio_df.to_sql(Peratio_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

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
            
            #UPLOAD REVENUE COLOR MAP DATA
            revenue_data = [['$0 - $250Million', color_1], 
                            ['$250Million - $500Million', color_2], 
                            ['$500Million- $1Billion', color_3],
                            ['$1Billion - $10Billion', color_4],
                            ['$10Billion - $50Billion', color_5],
                            ['$50Billion - $100Billion', color_6],
                            ['Greater than $100Billion', color_7]]

            revenue_df = pd.DataFrame(revenue_data, columns = ['Metric', 'Color'])
            print(revenue_df)

            engine = create_engine(engine_string)   
            revenue_df.to_sql(Revenue_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

            # #Format Revenue
            # df['Revenue Ranges'] = 'Placeholder'
            # df.loc[(df['Revenue'] <= 250000000), 'Revenue Ranges'] = '$0 - $250Million'
            # df.loc[(df['Revenue'] >= 250000000) & (df['Revenue'] <= 500000000), 'Revenue Ranges'] = '$250Million - $500Million'
            # df.loc[(df['Revenue'] >= 500000000) & (df['Revenue'] <= 1000000000), 'Revenue Ranges'] = '$500Million- $1Billion'
            # df.loc[(df['Revenue'] >= 1000000000) & (df['Revenue'] <= 10000000000), 'Revenue Ranges'] = '$1Billion - $10Billion'
            # df.loc[(df['Revenue'] >= 10000000000) & (df['Revenue'] <= 50000000000), 'Revenue Ranges'] = '$10Billion - $50Billion'
            # df.loc[(df['Revenue'] >= 50000000000) & (df['Revenue'] <= 100000000000), 'Revenue Ranges'] = '$50Billion - $100Billion'
            # df.loc[(df['Revenue'] >= 100000000000), 'Revenue Ranges'] = 'Greater than $100Billion'

            #UPLOAD EBIDTA COLOR MAP DATA
            ebitda_data = [['Less than -$100Million', color_1], 
                            ['-$100Million- -$50Million', color_2], 
                            ['-$50Million - $0', color_3],
                            ['$0 - $250Million', color_4],
                            ['$250Million - $500Million', color_5],
                            ['$500Million - $1Billion', color_6],
                            ['$1Billion - $10Billion', color_7],
                            ['Greater than $10Billion', color_8]]

            ebidta_df = pd.DataFrame(ebitda_data, columns = ['Metric', 'Color'])
            print(ebidta_df)

            engine = create_engine(engine_string)   
            ebidta_df.to_sql(Ebitda_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

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

        except Exception as e:
           print(str(e))