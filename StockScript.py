import requests
import json
import matplotlib.pyplot as plt
import numpy as np
key='AQXSQPCS64BZ2LPP'
#Intraday, interval 15 minutes, length full
r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&outputsize=full&apikey='+'AQXSQPCS64BZ2LPP')

#status on request
if (r.status_code==200):
    data = r.json()
else:
    print ("Error")

endtime=data["Meta Data"]["3. Last Refreshed"]
interval=data["Meta Data"]["4. Interval"]
timeseries=data["Time Series (15min)"]
length=len(timeseries)

# plt
axes = plt.gca()
axes.set_xlim([0,300])
axes.set_ylim([90,100])

# ["2018-05-02 16:00:00"]["2. high"]
x = 0
high = "2. high"
for timestamp in timeseries:
    x = x+1
    y = timeseries[timestamp][high]
    print ('(' + str(x) + ',' + str(y) + ')')
    plt.scatter(x, y)

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