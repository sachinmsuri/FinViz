from django.core.management.base import BaseCommand
from db_ingestion.models import Tickers
from sqlalchemy import create_engine
import pandas as pd
from parameters import engine_string
import datapackage


class Command(BaseCommand):
    help = "A command to add data from csv file to database"

    # def handle(self, *args, **options):
    #     try:
    #         #Clean data
    #         df = pd.read_csv("db_ingestion/nasdaq_data/nasdaq_screener_1638944075113.csv")
    #         df = df[df['Sector'].notna()]
    #         df[~df['Symbol'].str.contains("^")]
    #         df = df[df['Country'] == 'United States']
    #         df = df[['Symbol', 'Name', 'Sector', 'Volume']]

    #         #Upload data
    #         #engine = create_engine('sqlite:///db.sqlite3')
    #         engine = create_engine(engine_string)
    #         df.to_sql(Tickers._meta.db_table, con=engine, index=False, if_exists='replace')
    #         print('Nasdaq company information uploaded to database')
    #     except Exception as e:
    #         print(str(e))

    def handle(self, *args, **options):
        data_url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

        # to load Data Package into storage
        package = datapackage.Package(data_url)

        # to load only tabular data
        resources = package.resources
        for resource in resources:
            if resource.tabular:
                data = pd.read_csv(resource.descriptor['path'])
                print (data)

        df = data[data['Sector'].notna()]
        df[~df['Symbol'].str.contains("^")]
        # df = df[df['Country'] == 'United States']
        df = df[['Symbol', 'Name', 'Sector']]

        #Upload data
        #engine = create_engine('sqlite:///db.sqlite3')
        engine = create_engine(engine_string)
        df.to_sql(Tickers._meta.db_table, con=engine, index=False, if_exists='replace')
        print('Nasdaq company information uploaded to database')
