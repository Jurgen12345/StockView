import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from dataProcessing import ShowData 
import threading
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataBase import DataBase
import matplotlib.dates as mdates

class MainWindow:

    _instance = None
    current_index = ""
    current_indexID= 0
    global_price = 0.0
    current_ticker = ""
    url = ""
    def __init__(self):
        self.db = DataBase.getInstance()
        self.root = tk.Tk()
        self.root.geometry("1920x1080")
        self.root.title("StockView Home")
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
        self.lTimeLabel = ttk.Label(self.fTitleFrame, font=("Aptos",12,"italic"),style="LabelColor.TLabel")
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
        # self.cGraphsFrame = tk.Canvas(self.fVisualizationGraphs,bg="white",height=400,width=500)
        # self.cGraphsFrame.pack(side="left",padx = 5, pady=20)
        self.fig = Figure(figsize=(6,3),dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([],[])
        self.cGraphsFrame = FigureCanvasTkAgg(figure=self.fig,master=self.fVisualizationGraphs)
        self.cGraphsFrame.draw()
        self.cGraphsFrame.get_tk_widget().pack(side="left", padx=5, pady=20)
        

        #Visualization Choices
        self.fVisualizationChoicesFrame = ttk.Frame(self.fVisualizationGraphs, padding=2, style="MainColor.TFrame")        
        self.fVisualizationChoicesFrame.pack(side="right")
        self.bSMPIndex = ttk.Button(self.fVisualizationChoicesFrame, style="ButtonColor.TButton", text="^GSPC", )
        self.bSMPIndex.configure(command=lambda: (self.activeTicker("GSPC",0), self.updateChartWithCurrentIndex()))
        self.bSMPIndex.grid(row=0,column=0, padx=1, pady=10,sticky="nsew")
        self.bDJIIndex = ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="DJI")
        self.bDJIIndex.configure(command=lambda: (self.activeTicker("DJI",1),self.updateChartWithCurrentIndex()))
        self.bDJIIndex.grid(row=1, column=0,padx=5,pady=10,sticky="nsew")
        self.bIXICIndex = ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton", text="IXIC")
        self.bIXICIndex.configure(command=lambda: (self.activeTicker("IXIC",2), self.updateChartWithCurrentIndex()))
        self.bIXICIndex.grid(row=2, column=0,padx=5,pady=10,sticky="nsew")
        self.bNYAIndex= ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="NYA")
        self.bNYAIndex.configure(command=lambda: (self.activeTicker("NYA",3), self.updateChartWithCurrentIndex())) 
        self.bNYAIndex.grid(row=3, column=0,padx=5,pady=10,sticky="nsew")
        self.bBUK100PIndex= ttk.Button(self.fVisualizationChoicesFrame,style="ButtonColor.TButton",  text="BUK100P")
        self.bBUK100PIndex.configure(command=lambda : (self.activeTicker("BUK100P",4), self.updateChartWithCurrentIndex()))
        self.bBUK100PIndex.grid(row=4, column=0,padx=5,pady=10,sticky="nsew")




        #My Portofolio Compact Window
        self.fPortofolioFrame = ttk.Frame(self.fCenterRowFrame, padding=5, style="CustomColor1.TFrame")
        self.fPortofolioFrame.pack(side="left", expand=True)
        self.lMyPortofolioTextLable = ttk.Label(self.fPortofolioFrame, text="My Portofolio", font=("Aptoos", 18, "bold"), style="LabelColor.TLabel")
        self.lMyPortofolioTextLable.pack(side="top", pady=10,  padx=20)
        self.fPortofolioData = ttk.Frame(self.fPortofolioFrame)
        self.fPortofolioData.pack(side="bottom",padx=10, expand=True)
        if (self.checkPorfofolioLength() == 0):
            self.bEmptyStockLabel1 = ttk.Button(self.fPortofolioData, text="Portofolio is Empty! Click Here To Add Stocks.",style="ButtonColor.TButton")
            self.bEmptyStockLabel1.grid(row=0,column=0,padx=5,pady=5, sticky="nsew")
        # self.lStockLabel1 = ttk.Label(self.fPortofolioData, text="Stock 1", font=("Aptos",14))
        # self.lStockLabel1.grid(row =0, column=0, padx=5, pady=5,sticky="nsew")
        # self.lStockLabel2 = ttk.Label(self.fPortofolioData, text="Stock 1", font=("Aptos",14))
        # self.lStockLabel2.grid(row =1, column=0, padx=5, pady=5,sticky="nsew")

        #News Compact Window
        self.fNewsFrame = ttk.Frame(self.fCenterRowFrame, padding=5, style="CustomColor2.TFrame")
        self.fNewsFrame.pack(side="right", padx=20)
        self.lNewsInfoLabel = ttk.Label(self.fNewsFrame, text="Daily News", font=("Aptos", 18,"bold"), style="LabelColor.TLabel")
        self.lNewsInfoLabel.pack(side ="top",padx=10, pady=20)
        self.fDailyNewsFrame = ttk.Frame(self.fNewsFrame)
        self.fDailyNewsFrame.pack(side="bottom", padx=10, expand=True)
        self.generatedArticles = self.generate5DifferentNewsArticles()
        self.articlesList = []
        for newsIndex in range(5):
            self.articlesList.append(ttk.Label(self.fDailyNewsFrame,text=f"{self.generatedArticles[newsIndex][0]}  (Date : {self.generatedArticles[newsIndex][1]})",font=("Aptos",12), style="LabelColor.TLabel"))
            self.articlesList[newsIndex].grid(row=newsIndex, column=0, padx=5, pady=5, sticky="nsew")
        # Main Operations
        self.driver = ShowData.initializeWebdriver()
        self.updateFinancialInstrumentCurrentPrice()
        self.updateTickerAndPrice()
        self.updateTickerLabel()
        self.generate5DifferentNewsArticles()
        self.updateTime()

    def updateTickerAndPrice(self):
        if self.current_index:
            t = threading.Thread(target=self.getTickerAndPRice)
            t.start()
        self.root.after(3000,self.updateTickerAndPrice)
    

    def updateTickerLabel(self):
        if self.current_index:
            self.lGraphIndexName.configure(text=f"{self.current_index} : {self.getCurrentPriceFromMemory()}")
        self.root.after(1000,self.updateTickerLabel)


    def checkPorfofolioLength(self):
        self.db.cursor.execute(
            "SELECT * from Protfolio"
        )
        portofolio_contents = self.db.cursor.fetchall()
        return len(portofolio_contents) 



    def drawNewGraph(self):
        (hs_price, hs_date) = self.getCurrentStockHistoricalData()
        self.line.set_data(hs_date,hs_price)
        self.ax.relim()
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        self.fig.autofmt_xdate()
        self.ax.autoscale_view()
        self.ax.set_xlabel("Date",color="black",fontsize = 10)
        self.ax.set_ylabel("Price: $",color="black",fontsize=10)
        self.fig.tight_layout()
        self.ax.tick_params(axis="x",size=8)
        self.cGraphsFrame.draw()


    def updateChartWithCurrentIndex(self):
        # graph_thread = threading.Thread(target=self.drawNewGraph)
        # graph_thread.start()
        self.drawNewGraph() 


    def generate5DifferentNewsArticles(self):
        self.db.cursor.execute(
            "SELECT article_title, article_date from NewsData order by random() limit 5"
        )
        news_article = self.db.cursor.fetchall()
        return news_article

    def getCurrentStockHistoricalData(self):
        if self.current_indexID != None:
            self.db.cursor.execute(
                "SELECT closing_price from HistoricalPrice where financial_instrument_id = ?",
                (self.current_indexID,)
            )
            closing_price_data = self.db.cursor.fetchall()
            self.db.cursor.execute(
                "SELECT date from HistoricalPrice where financial_instrument_id = ?",
                (self.current_indexID,)
            )
            date = self.db.cursor.fetchall()
        hs_price = [] 
        hs_date = []
        for i in range(len(closing_price_data)):
            hs_price.append(closing_price_data[i][0])
            hs_date.append(datetime.datetime.fromisoformat(date[i][0]))
        
        return (hs_price, hs_date)

    def getCurrentPriceFromMemory(self):
        self.db.mem_cursor.execute(
            "SELECT last_closing_price from FinancialInstrument where id= ?",
            (self.current_indexID,)
        )
        last_price = self.db.mem_cursor.fetchone()[0]
        return last_price


    def getTickerAndPRice(self):
            price = ShowData.getIndexPrice(url=self.url,driver=self.driver).replace("'","").replace(",","")
            #self.lGraphIndexName.configure(text=f"{self.current_index} : {price}")
            self.global_price = float(price)
            self.driver.refresh()    

    def updateFinancialInstrumentCurrentPrice(self):
        self.db.cursor.execute(
                "UPDATE FinancialInstrument SET last_closing_price= ? where id = ?",
                (float(self.global_price),self.current_indexID)
        )


        fin_lastClosing = self.retrieveLastClosingPriceFromFinancialInstrument()
        for i in range(len(fin_lastClosing)):
            #print(fin_lastClosing[i][0])
            #print(".......")
            self.db.mem_cursor.execute(
                "UPDATE FinancialInstrument SET last_closing_price= ? where id = ?",
                (fin_lastClosing[i][0],i)
            ) 
        #print("-------")



        self.db.conn.commit()
        self.db.mem_conn.commit()

        self.root.after(3000, self.updateFinancialInstrumentCurrentPrice)

    def retrieveLastClosingPriceFromFinancialInstrument(self):
        self.db.cursor.execute(
            "SELECT last_closing_price from FinancialInstrument where id=0 or id =1 or id =2 or id = 3 or id =4"
        )   
        fin_closing = self.db.cursor.fetchall()
        return fin_closing



    def activeTicker(self,ticker,indexid):
        self.current_index = ticker
        self.current_indexID = indexid
        self.url = f"https://finance.yahoo.com/quote/%5E{self.current_index}/"

    
    def updateTime(self):
        t_clock = threading.Thread(target=self.getTime)
        t_clock.start()
        self.root.after(1000,self.updateTime)

    def getTime(self):
        self.lTimeLabel.configure(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




    def _onClose(self):
        MainWindow._instance = None
        self.root.destroy()
        self.db.conn.close()
        self.db.mem_conn.close()
    
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
    
    

