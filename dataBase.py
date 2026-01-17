import sqlite3



class DataBase:

    _dbInstance = None
    def __init__(self):
        self.conn = sqlite3.connect("StockViewDatabase.db")
        self.cursor = self.conn.cursor()
        print(self.cursor)


    @classmethod
    def getInstance(cls):
        if cls._dbInstance is None:
            cls._dbInstance = cls()
        return cls._dbInstance


if __name__ == "__main__":
    dbconnection = DataBase.getInstance()
    


