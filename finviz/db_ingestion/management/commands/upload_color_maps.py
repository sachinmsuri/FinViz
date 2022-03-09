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
            #UPLOAD MARKET CAP COLOR MAP DATA
            marketcap_data = [['$0 - $250Million', 'ffadad'], 
                            ['$250Million - $500Million', 'ffd6a5'], 
                            ['$500Million - $1Billion', 'fdffb6'],
                            ['$1Billion - $10Billion', 'caffbf'],
                            ['$10Billion - $50Billion', '9bf6ff'],
                            ['$50Billion - $100Billion', 'a0c4ff'],
                            ['$100Billion - $500Billion', 'bdb2ff'],
                            ['Greater than $500Billion', 'ffc6ff']]

            marketcap_df = pd.DataFrame(marketcap_data, columns = ['Metric', 'Color'])
            print(marketcap_df)

            engine = create_engine(engine_string)   
            marketcap_df.to_sql(Marketcap_colormaps._meta.db_table, con=engine, index=False, if_exists='replace')

            
            #UPLOAD DIVIDEND COLOR MAP DATA
            dividend_data = [['0%', 'ffadad'], 
                            ['0% - 1%', 'ffd6a5'], 
                            ['1% - 2.5%', 'fdffb6'],
                            ['2.5% - 5%', 'caffbf'],
                            ['5% - 7.5%', '9bf6ff'],
                            ['7.5% - 10%', 'a0c4ff'],
                            ['10% - 15%', 'bdb2ff'],
                            ['15% - 20%', 'ffc6ff'],
                            ['Greater than 20%', 'fffffc']]

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
            peratio_data = [['Less than -10', 'ffadad'], 
                            ['-10 - 0', 'ffd6a5'], 
                            ['0 - 10', 'fdffb6'],
                            ['10 - 20', 'caffbf'],
                            ['20 - 30', '9bf6ff'],
                            ['30 - 40', 'a0c4ff'],
                            ['40 - 50', 'bdb2ff'],
                            ['50 - 75', 'ffc6ff'],
                            ['75 - 100', 'fffffc'],
                            ['Greater than 100', 'fffffc']]

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
            revenue_data = [['$0 - $250Million', 'ffadad'], 
                            ['$250Million - $500Million', 'ffd6a5'], 
                            ['$500Million- $1Billion', 'fdffb6'],
                            ['$1Billion - $10Billion', 'caffbf'],
                            ['$10Billion - $50Billion', '9bf6ff'],
                            ['$50Billion - $100Billion', 'a0c4ff'],
                            ['Greater than $100Billion', 'bdb2ff']]

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
            ebitda_data = [['Less than -$100Million', 'ffadad'], 
                            ['-$100Million- -$50Million', 'ffd6a5'], 
                            ['-$50Million - $0', 'fdffb6'],
                            ['$0 - $250Million', 'caffbf'],
                            ['$250Million - $500Million', '9bf6ff'],
                            ['$500Million - $1Billion', 'a0c4ff'],
                            ['$1Billion - $10Billion', 'bdb2ff'],
                            ['Greater than $10Billion', 'ffc6ff']]

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