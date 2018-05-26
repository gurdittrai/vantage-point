import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import config
import matplotlib.gridspec as gridspec

def getData(interval,stock,key):
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

    #alpha error
    if "Information" in data:
        info = data["Information"]
        if "try again" in info:
            print(info)
            exit(1)
    
    return(data,SMAdata)

def getcurrentdata(interval,stock,key):
    r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+stock+'&interval=1min&apikey='+key)

    #status on request
    if (r.status_code==200):
        data = r.json()
    else:
        print ("Error retrieving stock data")

    #alpha error
    if "Information" in data:
        info = data["Information"]
        if "try again" in info:
            print(info)
            exit(1)

    #get the first timestamp
    timesseries=data["Time Series (1min)"]
    for timestamp in timesseries:
        curntvalue = timesseries[timestamp]

        stk_open    = curntvalue["1. open"]
        stk_high    = curntvalue["2. high"]
        stk_low     = curntvalue["3. low"]
        stk_close   = curntvalue["4. close"]
        return(stk_open, stk_high, stk_low, stk_close)
    
    return('0','0','0','0')

def plotData(data,SMAdata,stock,interval,fig):
    #now we parse through the data to get important information like timestamps
    timeseries=data["Time Series (Daily)"]
    #get the start and end times 
    endtime=data["Meta Data"]["3. Last Refreshed"]
    #starttime=sorted(timeseries.keys())[0]
    SMAtechnical=SMAdata["Technical Analysis: SMA"]
    SMAendtime=SMAdata["Meta Data"]["3: Last Refreshed"]
    #SMAstarttime=sorted(SMAtechnical.keys())[0]
    #startdate = datetime.date(int(starttime[0:4]),int(starttime[5:7]), int(starttime[8:10]) )
    enddate = datetime.date(int(endtime[0:4]),int(endtime[5:7]), int(endtime[8:10]) )
    #SMAstartdate = datetime.date(int(SMAstarttime[0:4]),int(SMAstarttime[5:7]), int(SMAstarttime[8:10]) )
    SMAenddate = datetime.date(int(SMAendtime[0:4]),int(SMAendtime[5:7]), int(SMAendtime[8:10]) )
    #delta calculates the number of days between two inputs output format: 5020 days, 0:00:00
    #we want to limit the amount of data we plot to avoid crashing the program 
    SMAintervaldate=SMAenddate + relativedelta(days=-interval)
    SMAbreakdate=SMAintervaldate.strftime('%Y-%m-%d')
    priceintervaldate=enddate + relativedelta(days=-interval)
    pricebreakdate=priceintervaldate.strftime('%Y-%m-%d')
    #length=len(SMAtechnical)
    xticks=[]
    SMAvalue=[]
    #fig=plt.figure(facecolor='white')
    ax=plt.axes()
    for date in SMAtechnical:
        xticks.append(date)
        SMAvalue.append(float(SMAtechnical[date]["SMA"]))
        #plt.scatter(limiter,float(SMAtechnical[date]["SMA"]))
        #stops reading the data once interval end is reached
        if date<=SMAbreakdate:
            break

    ax.set_xlabel("Time")
    ax.set_ylabel("Value (USD)")
    pricex=[]
    pricey=[]
    volume=[]
    for timestamp in timeseries:
        pricex.append(timestamp)
        pricey.append(float(timeseries[timestamp]["2. high"]))
        volume.append(float(timeseries[timestamp]["5. volume"]))
        if timestamp<=pricebreakdate:
            break
    font = {'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
            }
    #reversing the lists since they are read from most recent time to the interval end
    plotxticks=xticks[::-1]
    plotSMAvalue=SMAvalue[::-1]
    plotpricevalue=pricey[::-1]
    plotvolume=volume[::-1]
    #This is the actual plotting and formatting section
    # plt.subplot(211)
    # SMAline, = plt.plot(plotxticks,plotSMAvalue,lw=2.5,label='Simple Moving Average')
    # priceline, = plt.plot(plotxticks,plotpricevalue,lw=2.5,label='Stock Price')
    # plt.legend(handles=[SMAline,priceline])
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start, end, interval//10))
    # fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    # #plt.text(0.9, 0.9, stock, transform=ax.transAxes)
    # #ax.set_xlim(xmin=0,xmax=100)
    # #ax.set_ylim(ymin=ylow,ymax=yhigh)
    # plt.title("Tracking: "+stock+" Interval: "+str(interval)+" days")2
    # plt.subplot(212)
    # volume_line, = plt.plot(plotxticks,plotvolume,lw=2.5,label='Volume')
    # #plt.show()
    
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=4,rowspan=3)
    ax2 = plt.subplot2grid((4, 4), (3, 0), colspan=4,rowspan=1)
    start, end = ax2.get_xlim()
    ax1.plot(plotxticks,plotSMAvalue,lw=2.5,label='Simple Moving Average')
    ax1.plot(plotxticks,plotpricevalue,lw=2.5,label='Stock Price')
    ax2.plot(plotxticks,plotvolume,lw=2.5,label='Volume')
    ax2.legend(loc="upper right")
    ax1.legend(loc="upper right")
    ax2.xaxis.set_ticks(np.arange(start, end, interval//10))
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    ax1.set_xticks([])
    ax2.set_yticks([])
    ax1.set_title("Tracking: "+stock+" Interval: "+str(interval)+" days")
# def main():
#     key=config.api_key
#     #change this to get more/less data on plot
#     interval=365
#     stock="GOOGL"
#     data=getcurrentdata(interval,stock,key)
#     print(data)
#     # plotData(data,SMAdata,stock,interval)
    
# if __name__=='__main__' :
#     main()
