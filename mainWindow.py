import tkinter as tk
from tkinter import ttk
import datetime

class MainWindow:

    _instance = None
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.fMainFrame = ttk.Frame(self.root,padding=2)
        self.fMainFrame.pack(fill="both", expand=True)
        self.fTitleFrame = ttk.Frame(self.fMainFrame, padding=10)
        self.fTitleFrame.pack(fill="both")
        self.lTitleLabel = ttk.Label(self.fTitleFrame, text="StockView", font=("Aptos", 20, "bold"))
        self.lTitleLabel.pack(pady=5)
        self.lTimeLabel = ttk.Label(self.fTitleFrame, text=f"{self.getTime()}", font=("Aptos",12,"italic"))
        self.lTimeLabel.pack(pady=5)
        self.pwResizingFrame = ttk.PanedWindow(self.fMainFrame,orient='horizontal')
        self.pwResizingFrame.pack(fill="both",expand=True)
        self.root.protocol("WM_DELETE_WINDOW",self._onClose)
        
        self.fContentFrame = ttk.Frame(self.pwResizingFrame, padding=5)
        self.pwResizingFrame.add(self.fContentFrame)
        self.fGraphInfoFrame = ttk.Frame(self.fContentFrame,padding=2)
        self.fGraphInfoFrame.pack(side="top",fill="x")
        self.lGraphTitleLabel = ttk.Label(self.fGraphInfoFrame, text="Charts", font=("Aptos", 18,"bold"))
        self.lGraphTitleLabel.pack(side = "left",pady= 30, padx= 20)
        self.cGraphsFrame = tk.Canvas(self.fContentFrame,bg="yellow",height=200,width=300)
        self.cGraphsFrame.pack(side="top", anchor="w", padx = 20) 
        


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
    

