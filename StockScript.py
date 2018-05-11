import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import config
import matplotlib.dates as mdates
key=config.api_key

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

stock="GOOGL"
r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock+'&outputsize=full&apikey='+key)
#SMA is the simple moving average. The average of the 50 points surrounding the point of interest
SMA=requests.get('https://www.alphavantage.co/query?function=SMA&symbol='+stock+'&interval=daily&time_period=50&series_type=close&apikey='+key)

#status on request
if (r.status_code==200):
    data = r.json()
else:
    print ("Error retrieving stock data")

if (r.status_code==200):
    SMAdata = SMA.json()
else:
    print ("Error retreiving SMA")

endtime=data["Meta Data"]["3. Last Refreshed"]
#interval=data["Meta Data"]["4. Interval"]
timeseries=data["Time Series (Daily)"]
SMAtechnical=SMAdata["Technical Analysis: SMA"]
#length=len(SMAtechnical)
xticks=[]
SMAvalue=[]
limiter=0
for date in SMAtechnical:
    xticks.append(date)
    SMAvalue.append(SMAtechnical[date]["SMA"])
    limiter=limiter+1
    plt.scatter(limiter,SMAtechnical[date]["SMA"])
    if limiter>100:
        break
# plt
axes = plt.gca()
axes.set_xlabel("Time")
axes.set_ylabel("Price (Highs)")

# ["2018-05-02 16:00:00"]["2. high"]
yhigh, ylow = -1, -1
x = 0
high = "2. high"
for timestamp in timeseries:
    # get values
    x = x+1
    y = float(timeseries[timestamp][high])

    # limit output
    if (x > 100):
        break

    # get range
    if (yhigh == -1):
        yhigh = y
        ylow = y
    elif (y > yhigh):
        yhigh = y
    elif (y < ylow):
        ylow = y

    # print values to terminal
    #print ('(' + str(x) + ',' + str(y) + ')')
    plt.scatter(x, y)
    
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
plt.text(0.75, 0.9, 'SMA/Daily High', transform=axes.transAxes)
axes.set_xlim(xmin=0,xmax=100)
axes.set_ylim(ymin=ylow,ymax=yhigh)

plt.show()