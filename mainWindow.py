import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from dataProcessing import ShowData 
import time
import threading

class MainWindow:

    _instance = None
    current_index = ""
    url = ""
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.sMainStyle = ttk.Style()
        self.sMainStyle.theme_use("clam")
        self.sMainStyle.configure("MainColor.TFrame",background ="#536878", foreground ="#FFFFFF")
        self.sMainStyle.configure("LabelColor.TLabel", background = "#536878",foreground ="#FFFFFF")
        self.sMainStyle.configure("ButtonColor.TButton", background = "#536878",foreground ="#FFFFFF")
        self.sMainStyle.configure("CustomColor1.TFrame",background = "#A1FA57")
        self.sMainStyle.configure("CustomColor2.TFrame",background = "#FA3636")
        self.sMainStyle.configure("CustomColor3.TFrame",background = "#277DE6")
        self.fMainFrame = ttk.Frame(self.root,padding=2,style="MainColor.TFrame")
        self.fMainFrame.pack(fill="both", expand=True)
        self.mMenuBar = tk.Menu(background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mPortofolioBar= tk.Menu(self.mMenuBar,tearoff=False,background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mNewsBar = tk.Menu(self.mMenuBar, tearoff=False,background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mSearchBar = tk.Menu(self.mMenuBar,tearoff=False)
        self.mMenuBar.add_cascade(label="My Portofolio", menu=self.mPortofolioBar, font=("Aptos",14))
        self.mMenuBar.add_cascade(label="News", menu=self.mNewsBar, font=("Aptos", 14))
        self.mMenuBar.add_cascade(label="Search Financial Instruments", menu=self.mSearchBar, font=("Aptos",14))
        self.root.config(menu =self.mMenuBar)
        self.root.configure(bg="#536878")
        self.fTitleFrame = ttk.Frame(self.fMainFrame, padding=10, style="MainColor.TFrame")
        self.fTitleFrame.pack(fill="both")
        self.lTitleLabel = ttk.Label(self.fTitleFrame, text="StockView", font=("Aptos", 20, "bold"),style="LabelColor.TLabel")
        self.lTitleLabel.pack(pady=5)
        self.lTimeLabel = ttk.Label(self.fTitleFrame, text=f"{self.getTime()}", font=("Aptos",12,"italic"),style="LabelColor.TLabel")
        self.lTimeLabel.pack(pady=5)
        self.pwResizingFrame = ttk.PanedWindow(self.fMainFrame,orient='horizontal')
        self.pwResizingFrame.pack(fill="both",expand=True)
        self.root.protocol("WM_DELETE_WINDOW",self._onClose)

        #Main Contents Window        
        self.fContentFrame = ttk.Frame(self.pwResizingFrame, padding=5,style="MainColor.TFrame")
        self.pwResizingFrame.add(self.fContentFrame)
        self.fCenterRowFrame = ttk.Frame(self.fContentFrame,style="MainColor.TFrame")
        self.fCenterRowFrame.pack(side="top",fill="both",expand=True)

        #Visualization Compact Window
        self.fGraphInfoFrame = ttk.Frame(self.fCenterRowFrame,padding=2, style="MainColor.TFrame")
        self.fGraphInfoFrame.pack(side="left")
        self.lGraphTitleLabel = ttk.Label(self.fGraphInfoFrame, text="Indices", font=("Aptos", 18,"bold"),style="LabelColor.TLabel")
        self.lGraphTitleLabel.pack(side = "top",pady= 5, padx= 20)
        self.lGraphIndexName = ttk.Label(self.fGraphInfoFrame ,font=("Aptos", 18),style="LabelColor.TLabel")
        self.lGraphIndexName.pack(side="top",pady=2,padx=5, expand=True, anchor="w")
        self.lGraphChart = ttk.Label(self.fGraphInfoFrame, text="Chart", font=("Aptos",16,"italic"),style="LabelColor.TLabel")
        self.lGraphChart.pack(side="top" ,expand=True,padx=5, pady=20,anchor="w")
        self.fVisualizationGraphs = ttk.Frame(self.fGraphInfoFrame, padding=2, style="MainColor.TFrame")
        self.fVisualizationGraphs.pack(side="bottom", padx=10, pady=20)
        self.cGraphsFrame = tk.Canvas(self.fVisualizationGraphs,bg="white",height=300,width=400)
        self.cGraphsFrame.pack(side="left",padx = 5, pady=20)

        #Visualization Choices
        self.fVisualizationChoicesFrame = ttk.Frame(self.fVisualizationGraphs, padding=2, style="MainColor.TFrame")        
        self.fVisualizationChoicesFrame.pack(side="right")
        self.bSMPIndex = ttk.Button(self.fVisualizationChoicesFrame, style="ButtonColor.TButton", text="GSPC", )
        self.bSMPIndex.configure(command=lambda: self.activeTicker("GSPC"))
        self.bSMPIndex.grid(row=0,column=0, padx=1, pady=10,sticky="nsew")
        self.bDJIIndex = ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="DJI")
        self.bDJIIndex.configure(command=lambda: self.activeTicker("DJI"))
        self.bDJIIndex.grid(row=1, column=0,padx=5,pady=10,sticky="nsew")
        self.bIXICIndex = ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton", text="IXIC")
        self.bIXICIndex.configure(command=lambda: self.activeTicker("IXIC"))
        self.bIXICIndex.grid(row=2, column=0,padx=5,pady=10,sticky="nsew")
        self.bNYAIndex= ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="NYA")
        self.bNYAIndex.configure(command=lambda: self.activeTicker("NYA")) 
        self.bNYAIndex.grid(row=3, column=0,padx=5,pady=10,sticky="nsew")
        self.bBUK100PIndex= ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="BUK100P")
        self.bBUK100PIndex.configure(command=lambda : self.activeTicker("BUK100P"))
        self.bBUK100PIndex.grid(row=4, column=0,padx=5,pady=10,sticky="nsew")




        #My Portofolio Compact Window
        self.fPortofolioFrame = ttk.Frame(self.fCenterRowFrame, padding=5, style="CustomColor1.TFrame")
        self.fPortofolioFrame.pack(side="left", expand=True)
        self.lMyPortofolioTextLable = ttk.Label(self.fPortofolioFrame, text="My Portofolio", font=("Aptoos", 18, "bold"))
        self.lMyPortofolioTextLable.pack(side="top", pady=10,  padx=20)
        self.fPortofolioData = ttk.Frame(self.fPortofolioFrame)
        self.fPortofolioData.pack(side="bottom",padx=10, expand=True)
        self.lStockLabel1 = ttk.Label(self.fPortofolioData, text="Stock 1", font=("Aptos",14))
        self.lStockLabel1.grid(row =0, column=0, padx=5, pady=5,sticky="nsew")
        self.lStockLabel2 = ttk.Label(self.fPortofolioData, text="Stock 1", font=("Aptos",14))
        self.lStockLabel2.grid(row =1, column=0, padx=5, pady=5,sticky="nsew")

        #News Compact Window
        self.fNewsFrame = ttk.Frame(self.fCenterRowFrame, padding=5, style="CustomColor2.TFrame")
        self.fNewsFrame.pack(side="right", padx=20)
        self.lNewsInfoLabel = ttk.Label(self.fNewsFrame, text="Daily News", font=("Aptos", 18,"bold"))
        self.lNewsInfoLabel.pack(side ="top",padx=10, pady=20)
        self.fDailyNewsFrame = ttk.Frame(self.fNewsFrame)
        self.fDailyNewsFrame.pack(side="bottom", padx=10, expand=True)
        self.lDailyNews1 = ttk.Label(self.fDailyNewsFrame,text="Daily News 1",font=("Aptos",14)) 
        self.lDailyNews1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.lDailyNews2 = ttk.Label(self.fDailyNewsFrame,text="Daily News 2",font=("Aptos",14)) 
        self.lDailyNews2.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.driver = ShowData.initializeWebdriver()
        self.updateTickerAndPrice()


    def updateTickerAndPrice(self):
        if self.current_index:
            # price = ShowData.getIndexPrice(url=self.url,driver=self.driver)
            # self.lGraphIndexName.configure(text=f"{self.current_index} : {price}")
            # self.driver.refresh()
            t = threading.Thread(target=self.getTickerAndPRice)
            t.start()
        self.root.after(5000,self.updateTickerAndPrice) 
     
    def getTickerAndPRice(self):
            price = ShowData.getIndexPrice(url=self.url,driver=self.driver)
            self.lGraphIndexName.configure(text=f"{self.current_index} : {price}")
            self.driver.refresh()    


    def activeTicker(self,ticker):
        self.current_index = ticker
        self.url = f"https://finance.yahoo.com/quote/%5E{self.current_index}/"
        messagebox.showinfo("URL",self.url)

    def getTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _onClose(self):
        MainWindow._instance = None
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance =cls() 
        return cls._instance
    

if __name__ == "__main__":
    window = MainWindow.getInstance()
    window.run()
    
    

