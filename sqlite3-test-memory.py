import sqlite3

mem_conn = sqlite3.connect(":memory:")
cursor = mem_conn.cursor()

cursor.executescript("""
        BEGIN;
        create table if not exists FinancialInstrument(
            id INTEGER primary key,
            ticker TEXT not null,
            full_name TEXT not null,
            last_closing_price real
        );
        COMMIT;
                     """)

cursor.execute(
    "INSERT INTO FinancialInstrument(id,ticker, full_name,last_closing_price) values (?,?,?,?)",
    (1,"AMZN","Amazon Inc.",255.3)
)

cursor.execute(
    "INSERT INTO FinancialInstrument(id,ticker, full_name,last_closing_price) values (?,?,?,?)",
    (2,"MSFT","Microsoft Inc.",400.2)
)

cursor.execute(
    "SELECT id, ticker, last_closing_price from FinancialInstrument where id = 1"
)
mem_conn.commit()

amzn_data = cursor.fetchall()[0][2]

print(amzn_data)

mem_conn.close()
