import sqlite3
import pandas as pd
import yfinance as yf
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai import CrawlerRunConfig, AsyncWebCrawler, BrowserConfig
import re
import asyncio
import threading



class DataBase:

    _dbInstance = None
    tickers = ["^GSPC","^DJI","^IXIC","^NYA","^BUK100P","AMZN","GOOGL","MSFT","NVDA","NFLX","IBM","UAL","V","MA","AMD","CHGG","TTWO","NTES"]
    full_names = ["S&P 500","Dow Jones Industrial Average","NasDaq Composite", "NYSE Composite","Cboe UK 100",
                  "Amazon","Google","Microsoft","NVIDIA","Netflix","International Business Machines","United Airlines","Visa","Mastercard","Advanced Micro Devices","Chegg", "Take Two Interactive","NetEase"]

    ids = []
    links = ["https://www.investing.com/indices/us-spx-500-news","https://www.investing.com/indices/us-30-news",
                 "https://www.investing.com/indices/nasdaq-composite-news","https://www.investing.com/indices/nyse-composite-news",
                 "https://www.investing.com/equities/cboe-holdings-inc-news","https://www.investing.com/equities/amazon-com-inc-news",
                 "https://www.investing.com/equities/google-inc-news","https://www.investing.com/equities/microsoft-corp-news",
                 "https://www.investing.com/equities/nvidia-corp-news","https://www.investing.com/equities/netflix,-inc.-news",
                 "https://www.investing.com/equities/ibm-news","https://www.investing.com/equities/united-continenta-news",
                 "https://www.investing.com/equities/visa-inc-news","https://www.investing.com/equities/mastercard-cl-a-news",
                 "https://www.investing.com/equities/adv-micro-device-news","https://www.investing.com/equities/chegg-inc-news",
                 "https://www.investing.com/equities/take-two-interactive-news","https://www.investing.com/equities/netease.com-news"]


    def __init__(self):
        self.conn = sqlite3.connect("StockViewDatabase.db")
        self.cursor = self.conn.cursor()
        self.mem_conn = sqlite3.connect(":memory:")
        self.mem_cursor = self.mem_conn.cursor()
        
        self.cursor.executescript("""
        BEGIN;
        create table if not exists FinancialInstrument(
            id INTEGER primary key,
            ticker TEXT not null,
            full_name TEXT not null,
            last_closing_price real
        );
        
        
        create table if not exists HistoricalPrice(
            id TEXT primary key,
            financial_instrument_id int not null,
            closing_price real,
            open_price real,
            high_price real,
            low_price real, 
            volume int,
            date date not null,
            foreign key (financial_instrument_id) references FinancialInstrument(id)
        );           
        create table if not exists NewsData(
            id TEXT primary key,
            financial_instrument_id int not null,
            article_title TEXT,
            article_content TEXT,
            article_date date,
            article_url TEXT,
            foreign key (financial_instrument_id) references FinancialInstrument(id)
        );
                                  
        
        create table if not exists Protfolio(
            id INTEGER primary key,
            financial_instrument_id int not null,
            shares INTEGER,
            foreign key (financial_instrument_id) references FinancialInstrument(id)
        );
                                  
        COMMIT;
        """)


        self.mem_cursor.executescript("""
            BEGIN;
                create table if not exists FinancialInstrument(
                    id INTEGER primary key,
                    ticker TEXT not null,
                    full_name TEXT not null,
                    last_closing_price real
                );
            COMMIT;
                                    """)
        # self.deleteTableContents("FinancialInstrument")
        # self.deleteTableContents("HistoricalPrice")
        # self.deleteTableContents("NewsData")
        # self.deleteTableContents("Protfolio")

        for i in range(len(self.tickers)):
            self.ids.append(i)

        self.cursor.execute("SELECT * from FinancialInstrument")
        self.checkingDBLoad = self.cursor.fetchall()
        if len(self.checkingDBLoad) == 0:
            self.FinancialInstrumentInitialization()
            self.HistoricalPriceInitialization()
            asyncio.run(self.NewsDataInitialization())
        self.MemFinancialInstrumentIntialization()
    
    def MemFinancialInstrumentIntialization(self):
        try:
            for i in range(len(self.ids)):
                self.mem_cursor.execute(
                    "INSERT INTO FinancialInstrument(id, ticker,full_name) values (?,?,?)",
                        (self.ids[i], self.tickers[i], self.full_names[i])  
                )
            self.mem_conn.commit()
        except sqlite3.IntegrityError:
            pass

    def FinancialInstrumentInitialization(self):
        
        for i in range(len(self.ids)):
            self.cursor.execute(
                "INSERT INTO FinancialInstrument(id, ticker,full_name) values (?,?,?)",
                (self.ids[i], self.tickers[i], self.full_names[i])

                )
            self.mem_cursor.execute(
                  "INSERT INTO FinancialInstrument(id, ticker,full_name) values (?,?,?)",
                    (self.ids[i], self.tickers[i], self.full_names[i])  
            )
        self.conn.commit()
        self.mem_conn.commit()


    def HistoricalPriceInitialization(self):
     
        
        for ticker_index in range(len(self.ids)):
            yf_ticker = yf.Ticker(ticker=self.tickers[ticker_index])
            data = yf_ticker.history(period = "max", interval = "1d")
            for price_index in range(len(data)):
                self.cursor.execute(
                    "INSERT INTO HistoricalPrice(id,financial_instrument_id,closing_price,open_price,high_price,low_price,volume,date) values (?,?,?,?,?,?,?,?)",
                    (f"{self.tickers[ticker_index]}-{price_index}", self.ids[ticker_index],float(data["Close"].iloc[price_index]), float(data["Open"].iloc[price_index]),float(data["High"].iloc[price_index])
                     , float(data["Low"].iloc[price_index]), int(data["Volume"].iloc[price_index]), data.index[price_index].strftime("%Y-%m-%d %H:%M:%S"))
                )
        self.conn.commit()


    

    def deleteTableContents(self,table):
        self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()

    def deletTables(self):
        self.cursor.executescript("""
        BEGIN;
            Drop table FinancialInstrument;
            Drop table HistoricalPrice;
            Drop table NewsData;

                                  
        COMMIT;
                                  """)


    async def NewsDataInitialization(self):
        

        crawler_config = CrawlerRunConfig( 
        deep_crawl_strategy= BFSDeepCrawlStrategy(max_depth = 0,  include_external=False), stream=True,
        target_elements=["*[data-test='article-title-link']"]) 

        article_crawler_config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=0, include_external=False), stream=False,
        target_elements=["#article","div.flex.flex-row.items-center span"])


        async with AsyncWebCrawler() as crawler:

            try:
                for url_index in range(len(self.links)):
                    async for result in await crawler.arun(url=self.links[url_index], config=crawler_config):
                        article_title = re.findall(r"\[(.*?)\]", result.markdown) 
                        article_url = re.findall(r"\((.*?)\)", result.markdown)
                        for i in range(len(article_title)):
                            article_result = await crawler.arun(article_url[i],config=article_crawler_config)
                            idx = article_result.markdown.find("##") 
                            if idx != -1:
                                self.cursor.execute(
                                    "INSERT INTO NewsData(id,financial_instrument_id,article_title,article_content,article_date,article_url) values(?,?,?,?,?,?)",
                                    (f"N-{self.tickers[url_index]}-{i}", self.ids[url_index], article_title[i],article_result.markdown[:idx],article_result.html[article_result.html.index("Published")+12:article_result.html.index("Published") + 22],article_url[i])
                                )
                            else:
                                self.cursor.execute(
                                    "INSERT INTO NewsData(id,financial_instrument_id,article_title,article_content,article_date,article_url) values(?,?,?,?,?,?)",
                                    (f"N-{self.tickers[url_index]}-{i}", self.ids[url_index], article_title[i],article_result.markdown,article_result.html[article_result.html.index("Published")+12:article_result.html.index("Published") + 22],article_url[i])
                                )                                
            except (ValueError, AttributeError, TypeError):
                pass
        self.conn.commit()
        


    @classmethod
    def getInstance(cls):
        if cls._dbInstance is None:
            cls._dbInstance = cls()
        return cls._dbInstance


