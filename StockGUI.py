import tkinter as tk 
LARGE_FONT=("Verdana",12)
class stockapp(tk.Tk):
    #all code in __init__ method is run when app starts (creates startpage etc.) 
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        #container should be the main window object
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        #frame should represent different windows in the app
        frame=StartPage(container,self)
        self.frames[StartPage]=frame
        frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, cont):
        #selecting the right window to display and displaying it
        frame=self.frames[cont]
        frame.tkraise()
def qf(teststring):
        print (teststring)
#creates a window "StartPage"
class StartPage(tk.Frame):
    def __init__(self,parent, controler):
            tk.Frame.__init__(self,parent)
            label=tk.Label(self,text="Main Page",font=LARGE_FONT)
            label.pack(pady=10,padx=10)
            #qf is a temporary function to test functionality
            #this will not work if u pass variables to qf
            button1=tk.Button(self,text="Plot",command=lambda: qf("hi"))
            button1.pack()
app=stockapp()
app.mainloop()