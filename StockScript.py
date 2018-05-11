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

# plt
#axes = plt.gca()
#axes.set_xlabel("Time")
#axes.set_ylabel("Price (Highs)")

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
    
fig, ax = plt.subplots()
ax.plot(xticks, SMAvalue)

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

# round to nearest years...
datemin = np.datetime64(xticks[1], 'Y')
datemax = np.datetime64(xticks[-1], 'Y') + np.timedelta64(1, 'Y')
print (datemin)
ax.set_xlim(str(datemin), str(datemax))


# format the coords message box
def price(x):
    return '$%1.2f' % x
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = price
#ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
#fig.autofmt_xdate()

plt.show()