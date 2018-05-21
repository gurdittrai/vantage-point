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
        for F in (StartPage,PlotPage):
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
        
        fields = ('Stock Symbol', 'Interval (days)')

        stock_symbol_entry=Entry(self)
        user_input=tk.Label(self, text="Stock Symbol",font=small_font)
        
        interval_entry=Entry(self)
        interval_input=tk.Label(self, text="Interval (days)",font=small_font)

        stock_symbol_entry.insert(10,'GOOGL')
        interval_entry.insert(10,7)
        
        button1=ttk.Button(self,text="Plot Page",command=lambda: controller.show_frame(PlotPage))
        #button2=ttk.Button(self,text="Enter1",command=get_interval())
        button3=ttk.Button(self,text="Enter2",command=lambda: print("Symbol: %s\nInterval: %s" % (stock_symbol_entry.get(), interval_entry.get())))
        
        #grid
        label.grid(row=0,column=0)

        user_input.grid(row=1,column=0)
        stock_symbol_entry.grid(row=1,column=1)

        interval_input.grid(row=2,column=0)
        interval_entry.grid(row=2,column=1)

        button1.grid(row=3,column=0)
        #button2.grid(row=1,column=3)
        button3.grid(row=2,column=3)

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
def get_interval():
    print("hello")
    #interval=tk.IntVar()
    #print ("Test: "+str(interval.get()))
app=stockapp()
app.mainloop()