from django.core.management.base import BaseCommand
from db_ingestion.models import Tickerstats
from sqlalchemy import create_engine
import pandas as pd
from parameters import engine_string
from iexcloud.iexcloud import iexCloud
import random
import time

class Command(BaseCommand):
    help = "A command to add data from iexcloud api to database"

    def handle(self, *args, **options):
        financials_df_rows = []
        stats_df_rows = []
        try:
            obj = iexCloud()
            tickers_df = pd.read_sql('SELECT Symbol FROM db_ingestion_tickers;', engine_string)
            tickers = tickers_df['Symbol'].to_list()
            #For testing
            #tickers = random.choices(tickers, k=10)
            #tickers.extend(['NVDA', 'MSFT', 'AAPL'])
            tickers = list(dict.fromkeys(tickers))
            print(tickers)

            count = 0

            for ticker in tickers:
                count += 1
                if count == 50:
                    count = 0
                    time.sleep(30)
                    print('Pausing connnection ....')
                print(f"Fetching data for {ticker}")
                financials = obj.get_financials(ticker)
                stats = obj.get_stats(ticker)
                if financials:
                    financials_df_rows.append(financials)
                if stats:
                    stats_df_rows.append(stats)

            stats_df = pd.DataFrame(stats_df_rows)
            financials_df = pd.DataFrame(financials_df_rows)

            print(stats_df)
            print(financials_df)

            df = pd.merge(stats_df, financials_df, how='inner', on='Symbol')
            df = df.drop_duplicates()

            #Format Market Capitalisation
            df['Market Capitalization Ranges'] = 'Placeholder'
            df.loc[(df['Market Capitalization'] <= 250000000), 'Market Capitalization Ranges'] = '$0 - $250Million'
            df.loc[(df['Market Capitalization'] >= 250000000) & (df['Market Capitalization'] <= 500000000), 'Market Capitalization Ranges'] = '$250Million - $500Million'
            df.loc[(df['Market Capitalization'] >= 500000000) & (df['Market Capitalization'] <= 1000000000), 'Market Capitalization Ranges'] = '$500Million - $1Billion'
            df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 10000000000), 'Market Capitalization Ranges'] = '$1Billion - $10Billion'
            df.loc[(df['Market Capitalization'] >= 1000000000) & (df['Market Capitalization'] <= 50000000000), 'Market Capitalization Ranges'] = '$10Billion - $50Billion'
            df.loc[(df['Market Capitalization'] >= 5000000000) & (df['Market Capitalization'] <= 100000000000), 'Market Capitalization Ranges'] = '$50Billion - $100Billion'
            df.loc[(df['Market Capitalization'] >= 100000000000) & (df['Market Capitalization'] <= 500000000000), 'Market Capitalization Ranges'] = '$100Billion - $500Billion'
            df.loc[(df['Market Capitalization'] >= 500000000000), 'Market Capitalization Ranges'] = 'Greater than $500Billion'

            #Format Dividend
            df['Dividend Ranges'] = 'Placeholder'
            df.loc[(df['Dividend'] <= 0), 'Dividend Ranges'] = '0%'
            df.loc[(df['Dividend'] >= 0) & (df['Dividend'] <= 0.01), 'Dividend Ranges'] = '0% - 1%'
            df.loc[(df['Dividend'] >= 0.01) & (df['Dividend'] <= 0.025), 'Dividend Ranges'] = '1% - 2.5%'
            df.loc[(df['Dividend'] >= 0.025) & (df['Dividend'] <= 0.05), 'Dividend Ranges'] = '2.5% - 5%'
            df.loc[(df['Dividend'] >= 0.05) & (df['Dividend'] <= 0.075), 'Dividend Ranges'] = '5% - 7.5%'
            df.loc[(df['Dividend'] >= 0.075) & (df['Dividend'] <= 0.1), 'Dividend Ranges'] = '7.5% - 10%'
            df.loc[(df['Dividend'] >= 0.1) & (df['Dividend'] <= 0.15), 'Dividend Ranges'] = '10% - 15%'
            df.loc[(df['Dividend'] >= 0.15) & (df['Dividend'] <= 0.2), 'Dividend Ranges'] = '15% - 20%'
            df.loc[(df['Dividend'] >= 2), 'Dividend Ranges'] = 'Greater than 20%'

            #Format Dividend
            df['PE Ratio Ranges'] = 'Placeholder'
            df.loc[(df['PE Ratio'] <= -10), 'PE Ratio Ranges'] = 'Less than -10'
            df.loc[(df['PE Ratio'] >= -10) & (df['PE Ratio'] <= 0), 'PE Ratio Ranges'] = '-10 - 0'
            df.loc[(df['PE Ratio'] >= 0) & (df['PE Ratio'] <= 10), 'PE Ratio Ranges'] = '0 - 10'
            df.loc[(df['PE Ratio'] >= 10) & (df['PE Ratio'] <= 20), 'PE Ratio Ranges'] = '10 - 20'
            df.loc[(df['PE Ratio'] >= 20) & (df['PE Ratio'] <= 30), 'PE Ratio Ranges'] = '20 - 30'
            df.loc[(df['PE Ratio'] >= 30) & (df['PE Ratio'] <= 40), 'PE Ratio Ranges'] = '30 - 40'
            df.loc[(df['PE Ratio'] >= 40) & (df['PE Ratio'] <= 50), 'PE Ratio Ranges'] = '40 - 50'
            df.loc[(df['PE Ratio'] >= 50) & (df['PE Ratio'] <= 75), 'PE Ratio Ranges'] = '50 - 75'
            df.loc[(df['PE Ratio'] >= 75) & (df['PE Ratio'] <= 100), 'PE Ratio Ranges'] = '75 - 100'
            df.loc[(df['PE Ratio'] >= 100), 'PE Ratio Ranges'] = 'Greater than 100'

            #Format Revenue
            df['Revenue Ranges'] = 'Placeholder'
            df.loc[(df['Revenue'] <= 250000000), 'Revenue Ranges'] = '$0 - $250Million'
            df.loc[(df['Revenue'] >= 250000000) & (df['Revenue'] <= 500000000), 'Revenue Ranges'] = '$250Million - $500Million'
            df.loc[(df['Revenue'] >= 500000000) & (df['Revenue'] <= 1000000000), 'Revenue Ranges'] = '$500Million- $1Billion'
            df.loc[(df['Revenue'] >= 1000000000) & (df['Revenue'] <= 10000000000), 'Revenue Ranges'] = '$1Billion - $10Billion'
            df.loc[(df['Revenue'] >= 10000000000) & (df['Revenue'] <= 50000000000), 'Revenue Ranges'] = '$10Billion - $50Billion'
            df.loc[(df['Revenue'] >= 50000000000) & (df['Revenue'] <= 100000000000), 'Revenue Ranges'] = '$50Billion - $100Billion'
            df.loc[(df['Revenue'] >= 100000000000), 'Revenue Ranges'] = 'Greater than $100Billion'

            #Format EBITDA
            df['EBITDA Ranges'] = 'Placeholder'
            df.loc[(df['EBITDA'] < -100000000), 'EBITDA Ranges'] = 'Less than -$100Million'
            df.loc[(df['EBITDA'] < -100000000) & (df['EBITDA'] <= -50000000), 'EBITDA Ranges'] = '-$100Million- -$50Million'
            df.loc[(df['EBITDA'] >= -50000000) & (df['EBITDA'] <= 0), 'EBITDA Ranges'] = '-$50Million - $0'
            df.loc[(df['EBITDA'] >= 0) & (df['EBITDA'] <= 250000000), 'EBITDA Ranges'] = '$0 - $250Million'
            df.loc[(df['EBITDA'] >= 250000000) & (df['EBITDA'] <= 500000000), 'EBITDA Ranges'] = '$250Million - $500Million'
            df.loc[(df['EBITDA'] >= 500000000) & (df['EBITDA'] <= 1000000000), 'EBITDA Ranges'] = '$500Million - $1Billion'
            df.loc[(df['EBITDA'] >= 1000000000) & (df['EBITDA'] <= 10000000000), 'EBITDA Ranges'] = '$1Billion - $10Billion'
            df.loc[(df['EBITDA'] >= 10000000000), 'EBITDA Ranges'] = 'Greater than $10Billion'

            engine = create_engine(engine_string)   
            df.to_sql(Tickerstats._meta.db_table, con=engine, index=False, if_exists='replace')
            print(df)

        except Exception as e:
           print(str(e))