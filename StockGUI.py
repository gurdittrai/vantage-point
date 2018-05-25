import matplotlib
#these will allow us to embed matplotlib into tkinter windows
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import StockScript 
import tkinter as tk 
from tkinter import ttk
from tkinter import Entry
import config
key=config.api_key
interval=200
stock="ABX"
LARGE_FONT=("Verdana",12)
small_font=("Verdana",8)
class stocks():
    #track amount of stock being handled
    stocklist = []

    #list methods
    def addtolist(stock):
        stocks.stocklist.append(stock)

    def rmvfromlist(stock):
        stocks.stocklist.remove(stock)

    #print list
    def liststocks():
        print('Stock List:\n')
        for stock in stocks.stocklist:
            print('%s: %s' % (stockinfo.fields[0], stock.symbol))
            print('%s: %s\n' % (stockinfo.fields[1], stock.interval))


class stockinfo():
    #stock info fields
    fields = 'Stock Symbol', 'Interval (days)'

    #instance variables
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval

    #update instance variables
    def update_interval(self, new_intv):
        self.interval = new_intv


class stockapp(tk.Tk):
    #all code in __init__ method is run when app starts (creates startpage etc.) 
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.iconbitmap(self,default="icon_stocks.ico")
        tk.Tk.wm_title(self,"Stock Tracking")

        #container should be the main window object
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        #add the pages in this list everytime you make a new page
        for F in (StartPage,PlotPage,OldPage):
            #frame should represent different windows in the app
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self, cont):
        #selecting the right window to display and displaying it
        frame=self.frames[cont]
        frame.tkraise()

#creates a window "StartPage"
class StartPage(tk.Frame):
    #print values of fields
    def addstock(self, entries):
        symbol = '_ERROR_'
        interval = '_ERROR_'

        for entry in entries:
            field = entry[2]
            text = entry[1].get()

            if (field == stockinfo.fields[0]):
                symbol = text
            elif (field == stockinfo.fields[1]):
                interval = text
            else:
                print("warning: unidef field detected")

        #init stock
        stocks.addtolist(stockinfo(symbol, interval))
        self.create_widget(symbol, interval)
        
        

    def create_window(self, parent, controller, fields, field_defaults):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="Test Page",font=LARGE_FONT)
        btn_old = ttk.Button(self,text="Old Page",command=lambda: controller.show_frame(OldPage))
        btn_plot = ttk.Button(self,text="Plot",command=lambda: controller.show_frame(PlotPage))
        btn_exit = ttk.Button(self,text="Exit",command=lambda: exit(1))

        #create input fields
        entries = []
        for field, fdefault in zip(fields, field_defaults):
            #three columns
            rowlabel = tk.Label(self, text=field, font=small_font)

            entry = Entry(self)
            entry.insert(10,fdefault)

            #add to list
            entries.append((rowlabel, entry, field))

        btn_addstock = ttk.Button(self,text="Enter",command=lambda: self.addstock(entries))
        btn_showstocks = ttk.Button(self,text="Show List",command=lambda: stocks.liststocks())

        #grid
        rowCount = 0

        #adding heading
        label.grid(row=rowCount,column=0)
        rowCount += 1
        
        #adding entries to the grid
        for r, entry in enumerate(entries, start=rowCount):
            for c in range(0,2):
                entry[c].grid(row=r,column=c)
            rowCount += 1

        #button
        btn_addstock.grid(row=rowCount,column=1)
        btn_showstocks.grid(row=rowCount,column=2)
        rowCount += 1

        #other pages
        btn_old.grid(row=rowCount,column=0)
        btn_plot.grid(row=rowCount,column=1)
        #exit
        btn_exit.grid(row=rowCount,column=2)

    def create_widget(self, symbol, interval):
        tstock = tk.Toplevel(self)
        tstock.wm_title('%s' % symbol)
        tstock.geometry("400x175")
        tstock.resizable(width=False, height=False)

        data = StockScript.getcurrentdata(interval, symbol, key)
        print(data)

        stk_close = tk.Label(tstock, text="%s" % data[3], font=LARGE_FONT)
        stk_close.grid(row=0, column=0)

        stk_open = tk.Label(tstock, text="open %s" % data[0], font=small_font)
        stk_open.grid(row=0, column=1)

        stk_high = tk.Label(tstock, text="high %s" % data[1], font=small_font)
        stk_high.grid(row=1, column=0)

        stk_low = tk.Label(tstock, text="low %s" % data[2], font=small_font)
        stk_low.grid(row=2, column=0)

        btn_exit = tk.Button(tstock, text="X", command=tstock.destroy)
        btn_exit.grid(row=0, column=2)

    def __init__(self, parent, controller):
        #input fields
        field_defaults = 'GOOGL', '7'

        #make window
        self.create_window(parent, controller, stockinfo.fields, field_defaults)


class OldPage(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Main Page",font=LARGE_FONT)

        #create field
        stock_symbol_entry = Entry(self)
        user_input = tk.Label(self, text="Stock Symbol",font=small_font)
        
        interval_entry = Entry(self)
        interval_input = tk.Label(self, text="Interval (days)",font=small_font)

        #set default values on the field
        stock_symbol_entry.insert(10,'GOOGL')
        interval_entry.insert(10,7)
        
        btn_stock = ttk.Button(self,text="Enter1")
        btn_interval = ttk.Button(self,text="Enter2",command=lambda: print("Symbol: %s\nInterval: %s" % (stock_symbol_entry.get(), interval_entry.get())))
        btn_plot = ttk.Button(self,text="Plot Page",command=lambda: controller.show_frame(PlotPage))
        btn_test = ttk.Button(self,text="Home Page",command=lambda: controller.show_frame(StartPage))
        btn_exit = ttk.Button(self,text="Exit",command=lambda: exit(1))

        #grid
        label.grid(row=0,column=0)

        user_input.grid(row=1,column=0)
        stock_symbol_entry.grid(row=1,column=1)

        interval_input.grid(row=2,column=0)
        interval_entry.grid(row=2,column=1)

        btn_stock.grid(row=1,column=3)
        btn_interval.grid(row=2,column=3)
        btn_plot.grid(row=3,column=1)
        btn_test.grid(row=3,column=0)
        btn_exit.grid(row=4,column=0)

#we can copy this (almost) exactly to create more pages
class PlotPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Plotting Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1=ttk.Button(self,text="Back to home",command=lambda: controller.show_frame(StartPage))
        button1.pack()
        btn_fetch = ttk.Button(self,text="Fetch Data",command=lambda: self.getData())
        btn_fetch.pack()
        btn_plot = ttk.Button(self,text="Plot Data",command=lambda: self.plotData())
        btn_plot.pack()

        self.fig=plt.figure(facecolor='white')
        # data, SMAdata=StockScript.getData(interval,stock,key)
        # StockScript.plotData(data,SMAdata,stock,interval,fig)

        canvas=FigureCanvasTkAgg(self.fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        toolbar=NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()

        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    def getData(self):
        self.data,self.SMAdata=StockScript.getData(interval,stock,key)
    def plotData(self):
        StockScript.plotData(self.data,self.SMAdata,stock,interval,self.fig)

app=stockapp()
app.mainloop()