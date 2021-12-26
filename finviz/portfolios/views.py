from django.shortcuts import render

# Create your views here.

def create_portfolio(request):
        return render(request, 'portfolios.html', {})
