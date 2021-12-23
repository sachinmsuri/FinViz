from django.db import models
from pandas import DataFrame

class Tickers(models.Model):
    symbol = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    marketcap = models.IntegerField
    volume = models.IntegerField

    def ticker_dataframe(self) -> DataFrame:
        """
        Get all pricing data, as a Pandas DataFrame object, for a given Stock.
        Returns:
            Pandas DataFrame
        """
        return DataFrame.from_records(Tickers.objects.all().values())

class Tickerstats(models.Model):
    symbol = models.CharField(max_length=500)
