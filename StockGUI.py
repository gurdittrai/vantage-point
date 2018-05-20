import tkinter as tk 
from tkinter import ttk
LARGE_FONT=("Verdana",12)
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
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Main Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #lambda function might have trouble if you pass a variable to it
        button1=ttk.Button(self,text="Plot Page",command=lambda: controller.show_frame(PlotPage))
        button1.pack()
#we can copy this (almost) exactly to create more pages
class PlotPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Plotting Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1=ttk.Button(self,text="Back to home",command=lambda: controller.show_frame(StartPage))
        button1.pack()
app=stockapp()
app.mainloop()