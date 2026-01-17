import tkinter as tk
from tkinter import ttk
import datetime

class MainWindow:

    _instance = None
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.sMainStyle = ttk.Style()
        self.sMainStyle.configure("MainColor.TFrame",background ="#536878", foreground ="#FFFFFF")
        self.sMainStyle.configure("LabelColor.TLabel", background = "#536878",foreground ="#FFFFFF")
        self.sMainStyle.configure("CustomColor1.TFrame",background = "#A1FA57")
        self.sMainStyle.configure("CustomColor2.TFrame",background = "#FA3636")
        self.sMainStyle.configure("CustomColor3.TFrame",background = "#277DE6")
        self.fMainFrame = ttk.Frame(self.root,padding=2,style="MainColor.TFrame")
        self.fMainFrame.pack(fill="both", expand=True)
        self.mMenuBar = tk.Menu(background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mPortofolioBar= tk.Menu(self.mMenuBar,tearoff=False,background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mNewsBar = tk.Menu(self.mMenuBar, tearoff=False,background="#536878", foreground="#FFFFFF", activebackground="#536878",activeforeground="#FFFFFF")
        self.mMenuBar.add_cascade(label="My Portofolio", menu=self.mPortofolioBar, font=("Aptos",14))
        self.mMenuBar.add_cascade(label="News", menu=self.mNewsBar, font=("Aptos", 14))
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
        self.fCenterRowFrame = ttk.Frame(self.fContentFrame,style="CustomColor3.TFrame")
        self.fCenterRowFrame.pack(side="top",fill="both",expand=True)

        #Visualization Compact Window
        self.fGraphInfoFrame = ttk.Frame(self.fCenterRowFrame,padding=2)
        self.fGraphInfoFrame.pack(side="left")
        self.lGraphTitleLabel = ttk.Label(self.fGraphInfoFrame, text="Charts", font=("Aptos", 18,"bold"))
        self.lGraphTitleLabel.pack(side = "top",pady= 10, padx= 20)
        self.cGraphsFrame = tk.Canvas(self.fGraphInfoFrame,bg="yellow",height=300,width=400)
        self.cGraphsFrame.pack(side="bottom",padx = 10) 
        

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
    

