from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests
import pandas as pd
import json
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.ticker as ticker
import plotly.graph_objects as go
import pytz
import mplfinance as mpf
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.io import output_notebook
from math import pi
import random
from urllib.request import urlopen
from IPython.display import display, HTML




# Create your views here.
def home(request):
    return render(request, 'app1/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app1/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() # save the user in db
                login(request, user) #log them in following creation of indexauth_permission_content_type_id_codename_01ab375a_uniqauth_permission
                return redirect('userhome')                 # what the user will be taken to at login
            except IntegrityError:
                return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: That username is already registered. Please choose a different username"})

        else:
            # Tell user passwords didn't match
            return render(request, 'app1/signupuser.html', {'form':UserCreationForm(), "Error":"ERROR: Passwords did NOT match"})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'app1/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'app1/loginuser.html', {'form': AuthenticationForm(), 'Error':'ERROR: Username and Password did not match'})
        else:
            login(request, user) #log them in following creation of indexauth_permission_content_type_id_codename_01ab375a_uniqauth_permission
            return redirect('userhome')                 # what the user will be taken to at login


@login_required
def userhome(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'app1/userhome.html', {'todos': todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'app1/completedtodos.html', {'todos': todos})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def addTodo(request):
    if request.method == 'GET':
        return render(request, 'app1/addTodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False) #creating a new to do object when someone creates a new one
            newTodo.user = request.user
            newTodo.save()
            return redirect('userhome')
        except ValueError:
            return render(request, 'app1/addtodo.html', {'Form': TodoForm(), 'error': 'Please Try Again'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'app1/viewtodo.html', {'todo': todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('userhome')
        except ValueError:
            return render(request, 'app1/viewtodo.html', {'todo': todo, 'form':form, 'Error':'Bad info. Please Retry.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('userhome')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('userhome')

@login_required
def sofie(request):
    symbolInput = input("Enter a symbol: ")
    timeInt = input("Select a time interval - 1m|2m|5m|15m|60m|1d: ")
    rangeInput = input("Select a range - 1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max: ")

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

    querystring = {"region": "US","symbol": symbolInput, "interval": timeInt, "range": rangeInput}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "e1608636d9msh8918cbfa46ffe42p118d48jsn816a911904ed"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).text
    a = json.loads(response)

    return (a)


@login_required
def stockhome(request):
    stock_list=["TSLA","AAPL","FB","AMZN","TWTR","BAC","GOOG","MSFT","NKLA"]
    example = random.choice(stock_list)
    return render(request, "app1/stockhome.html",{"eg":example})

@login_required
def stocksummtab(request):
    symbolInput = request.GET['symbol']
    ticker = str(symbolInput.upper())
    url = ("https://financialmodelingprep.com/api/v3/quote/"+
        ticker
        +"?apikey=1cea72b42ffe5bc30567da0ada037c2b")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    loaded_data = json.loads(data)[0]
    dayLow = str(loaded_data['dayLow'])
    dayHigh = str(loaded_data['dayHigh'])
    current = str(loaded_data['price'])
    date = str(datetime.fromtimestamp(
        int(loaded_data['timestamp']),
        pytz.timezone('America/Los_Angeles')).strftime('%a %m/%d/%y'))
    time = str(datetime.fromtimestamp(
        int(loaded_data['timestamp']),
        pytz.timezone('America/Los_Angeles')).strftime('%I:%M:%S'))
    yearLow =  str(round(loaded_data['yearLow'],2))
    yearHigh = str(round(loaded_data['yearHigh'],2))
    mrktCap = str(f"{loaded_data['marketCap']:,}")
    avg50 = str(round(loaded_data['priceAvg50'],2))
    avg200 = str(round(loaded_data['priceAvg200'],2))
    volume = str(f"{loaded_data['volume']:,}")
    avgVolume = str(f"{loaded_data['avgVolume']:,}")
    stockopen = str(loaded_data['open'])
    previousClose = str(loaded_data['previousClose'])
    pe = str(loaded_data['pe'])
    eps = str(loaded_data['eps'])
    #earnAnnounce = str(datetime.datetime(loaded_data['earningsAnnouncement']), pytz.timezone('America/Los_Angeles'))
    outstandingShares = str(f"{loaded_data['sharesOutstanding']:,}")#str(f"{loaded_data['sharesOutstanding']:,}")

    dict1={"Ticker Symbol":ticker,
    "Current Price":current,
    "Opening Price":stockopen,
    "Prevous Close": previousClose,
    "Volume":volume,
    "Average Volume":avgVolume,
    "Day Low":dayLow,
    "Day High":dayHigh,
    "Year Low":yearLow,
    "Year High":yearHigh,
    "50 Day Moving Average":avg50,
    "200 Day Moving Average":avg200,
    "Market Cap":mrktCap,
    "PE Ratio": pe,
    "EPS":eps,
    "Outstanding Shares":outstandingShares}

    df = pd.DataFrame.from_dict(dict1, orient="index")#, index=range(1,18))
    df.columns = [f"as of {time} on {date}"]
    df_html = df.to_html()
    return HttpResponse(df_html)

@login_required
def stocksumm(request):
    symbolInput = request.GET['symbol']
    ticker = str(symbolInput.upper())
    url = ("https://financialmodelingprep.com/api/v3/quote/"+
        ticker
        +"?apikey=1cea72b42ffe5bc30567da0ada037c2b")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    loaded_data = json.loads(data)[0]
    dayLow = str(loaded_data['dayLow'])
    dayHigh = str(loaded_data['dayHigh'])
    current = str(loaded_data['price'])
    date = str(datetime.fromtimestamp(
        int(loaded_data['timestamp']),
        pytz.timezone('America/Los_Angeles')).strftime('%a %m/%d/%y'))
    time = str(datetime.fromtimestamp(
        int(loaded_data['timestamp']),
        pytz.timezone('America/Los_Angeles')).strftime('%I:%M:%S'))
    yearLow =  str(round(loaded_data['yearLow'],2))
    yearHigh = str(round(loaded_data['yearHigh'],2))
    mrktCap = str(f"{loaded_data['marketCap']:,}")
    avg50 = str(round(loaded_data['priceAvg50'],2))
    avg200 = str(round(loaded_data['priceAvg200'],2))
    volume = str(f"{loaded_data['volume']:,}")
    avgVolume = str(f"{loaded_data['avgVolume']:,}")
    stockopen = str(loaded_data['open'])
    previousClose = str(loaded_data['previousClose'])
    pe = str(loaded_data['pe'])
    eps = str(loaded_data['eps'])
    #earnAnnounce = str(datetime.datetime(loaded_data['earningsAnnouncement']), pytz.timezone('America/Los_Angeles'))
    outstandingShares = str(f"{loaded_data['sharesOutstanding']:,}")#str(f"{loaded_data['sharesOutstanding']:,}")

    dict1={"Ticker Symbol":ticker,
    "Current Price":current,
    "Opening Price":stockopen,
    "Prevous Close": previousClose,
    "Volume":volume,
    "Average Volume":avgVolume,
    "Day Low":dayLow,
    "Day High":dayHigh,
    "Year Low":yearLow,
    "Year High":yearHigh,
    "50 Day Moving Average":avg50,
    "200 Day Moving Average":avg200,
    "Market Cap":mrktCap,
    "PE Ratio": pe,
    "EPS":eps,
    "Outstanding Shares":outstandingShares}

    df = pd.DataFrame.from_dict(dict1, orient="index")#, index=range(1,18))
    df.columns = [f"as of {time} on {date}"]
    df_html = df.to_html()
    return render(request, "app1/stocksumm.html", {"df":df_html})


    # return render(request,"app1/stocksumm.html",{
    #     "ticker":ticker,
    #     "dateTime":dateTime,
    #     "stockopen":stockopen,
    #     "current":current,
    #     "prevClose": previousClose,
    #     "vol":volume,
    #     "avgVol":avgVolume,
    #     "dl":dayLow,
    #     "dh":dayHigh,
    #     "yl":yearLow,
    #     "yh":yearHigh,
    #     "50da":avg50,
    #     "200da":avg200,
    #     "mkcp":mrktCap,
    #     "pe": pe,
    #     "eps":eps,
    #     "shares":outstandingShares,
    #     "df":df
    #             })
