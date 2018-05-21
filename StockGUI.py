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
        for F in (StartPage,PlotPage,TestPage):
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

    def __init__(self,parent, controller):
        root = tk.Frame.__init__(self,parent)
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
        btn_test = ttk.Button(self,text="Test Page",command=lambda: controller.show_frame(TestPage))
        btn_exit = ttk.Button(self,text="Exit",command=lambda: exit(1))

        #grid
        label.grid(row=0,column=0)

        user_input.grid(row=1,column=0)
        stock_symbol_entry.grid(row=1,column=1)

        interval_input.grid(row=2,column=0)
        interval_entry.grid(row=2,column=1)

        btn_stock.grid(row=1,column=3)
        btn_interval.grid(row=2,column=3)
        btn_plot.grid(row=3,column=0)
        btn_test.grid(row=3,column=1)
        btn_exit.grid(row=4,column=0)

#we can copy this (almost) exactly to create more pages
class PlotPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Plotting Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to home",command=lambda: controller.show_frame(StartPage))
        button1.pack()
        fig=plt.figure(facecolor='white')
        data, SMAdata=StockScript.getData(interval,stock,key)
        StockScript.plotData(data,SMAdata,stock,interval,fig)
        canvas=FigureCanvasTkAgg(fig,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        toolbar=NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

class TestPage(tk.Frame):
    #print values of fields
    def fetch(entries):
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            print('%s: %s' % (field, text))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label=tk.Label(self,text="Test Page",font=LARGE_FONT)
        btn_home = ttk.Button(self,text="Home Page",command=lambda: controller.show_frame(StartPage))

        #create input fields
        fields = 'Stock Symbol', 'Interval (days)'
        field_defaults = 'GOOGL', '7'
        entries = []
        for field, fdefault in zip(fields, field_defaults):
            #three columns
            rowlabel = tk.Label(self, text=field, font=small_font)
            entry = Entry(self)
            entry.insert(10,fdefault)
            btn = ttk.Button(self,text="Enter",command=lambda: print('%s: %s' % (field, entry.get())))
            #add to list
            entries.append((rowlabel, entry, btn, field))

        #grid
        rowCount = 0

        #adding start and end rows
        label.grid(row=rowCount,column=0)
        rowCount += 1
        
        #adding entries to the grid
        for r, entry in enumerate(entries, start=rowCount):
            for c in range(0,3):
                entry[c].grid(row=r,column=c)
            rowCount += 1

        btn_home.grid(row=rowCount,column=0)

#btn function
    def showValue(field, entry):
        print('%s: %s' % (field, entry.get()))

app=stockapp()
app.mainloop()