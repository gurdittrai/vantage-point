import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import config
key=config.api_key
#Intraday, interval 15 minutes, length full
stock="GOOGL"
r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stock+'&interval=60min&outputsize=compact&apikey='+'AQXSQPCS64BZ2LPP')

#status on request
if (r.status_code==200):
    data = r.json()
else:
    print ("Error")

endtime=data["Meta Data"]["3. Last Refreshed"]
interval=data["Meta Data"]["4. Interval"]
timeseries=data["Time Series (60min)"]
length=len(timeseries)

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
plt.text(0.75, 0.9, 'matplotlib', transform=axes.transAxes)
axes.set_xlim(xmin=0,xmax=100)
axes.set_ylim(ymin=ylow,ymax=yhigh)
plt.show()

# error_config = {'ecolor': '0.3'}
# # starttime = timeseries.keys()[length-1]
# # print data
# # print endtime
# fig, ax = plt.subplots()
# bar_width=0.35
# opacity=0.4
# index=np.arange(length)
# rects1 = ax.bar(index, timeseries[timestamp]["2. high"], bar_width,alpha=opacity, color='b', error_kw=error_config,label='MFST')
# ax.set_xlabel('Date')
# ax.set_ylabel('Price')
# ax.set_title('Price by date')
# ax.set_xticks(index + bar_width / 2)
# ax.set_xticklabels(timeseries.keys())

# fig.tight_layout()
# plt.show()