from django.core.management.base import BaseCommand
from db_ingestion.models import Tickerstats
from sqlalchemy import create_engine
import pandas as pd
from parameters import engine_string
from iexcloud.iexcloud import iexCloud
import random

class Command(BaseCommand):
    help = "A command to add data from iexcloud api to database"

    def handle(self, *args, **options):
        financials_df_rows = []
        stats_df_rows = []
        try:
            obj = iexCloud()
            tickers_df = pd.read_sql('SELECT Symbol FROM db_ingestion_tickers;', engine_string)
            tickers = tickers_df['Symbol'].to_list()
            tickers = random.choices(tickers, k=100)
            #For testing
            #tickers.extend(['NVDA', 'MSFT', 'AAPL'])
            tickers = list(dict.fromkeys(tickers))
            print(tickers)   

            for ticker in tickers:
                print(f"Fetching data for {ticker}")
                financials = obj.get_financials(ticker)
                stats = obj.get_stats(ticker)
                if financials:
                    financials_df_rows.append(financials)
                if stats:
                    stats_df_rows.append(stats)

            stats_df = pd.DataFrame(stats_df_rows)
            financials_df = pd.DataFrame(financials_df_rows)

            df = pd.merge(stats_df, financials_df, how='inner', on='Symbol')
            df = df.drop_duplicates()

            engine = create_engine(engine_string)   
            df.to_sql(Tickerstats._meta.db_table, con=engine, index=False, if_exists='replace')
            print(df)

        except Exception as e:
           print(str(e))