import requests
import json
import matplotlib.pyplot as plt
import numpy as np
key='AQXSQPCS64BZ2LPP'
#Intraday, interval 15 minutes, length full
r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=15min&outputsize=full&apikey='+'AQXSQPCS64BZ2LPP')

if (r.status_code==200):
    data = r.json()
else:
    print "Error"
endtime=data["Meta Data"]["3. Last Refreshed"]
interval=data["Meta Data"]["4. Interval"]
timeseries=data['Time Series (15min)']
length=len(timeseries)
error_config = {'ecolor': '0.3'}
# starttime = timeseries.keys()[length-1]
# print data
# print endtime
fig, ax =plt.subplots()
bar_width=0.35
opacity=0.4
index=np.arange(length)
rects1 = ax.bar(index, timeseries["2. high"], bar_width,alpha=opacity, color='b',yerr=std_men, error_kw=error_config,label='MFST')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Price by date')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(timeseries.keys())
fig.tight_layout()
plt.show()