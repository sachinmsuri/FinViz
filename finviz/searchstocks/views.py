from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from iexcloud.iexcloud import iexCloud
from json import dumps


# Create your views here.

def search_stock(request):
    if request.method == 'POST':
        stock = request.POST['search_stock']
        obj = iexCloud()

        try:
            stock_name = obj.get_quote(stock)
            time_series = obj.get_max_time_series(stock)

            #format data for chartjs
            chartjs_data = []
            for i in time_series:
                chartjs_data.append({'x':i['date'], 'y':i['close']})

            dataJSON = dumps(chartjs_data)        
        except Exception as e:
            dataJSON = "Error"
        
        return render(request, 'search_stock.html', {'chartjs_data': dataJSON, 'stock_name': stock_name})
        
    else:
        return render(request, 'search_stock.html', {'search_stock': 'Enter a stock quote'})


def _search_stock(request):
    return render(request, 'search_stock.html', {})
