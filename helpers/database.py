import sqlite3

def initialise_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            second INTEGER NOT NULL
        )
    ''')

    dates = [
        20250116184530,  # January 16, 2025, 18:45:30
        20231225123045,  # December 25, 2023, 12:30:45
        20241108150015,  # November 8, 2024, 15:00:15
        20251030071559,  # October 30, 2025, 07:15:59
        20260401225905,  # April 1, 2026, 22:59:05
        20230822103025,  # August 22, 2023, 10:30:25
        20270704000000,  # July 4, 2027, 00:00:00
        20251031120010,  # October 31, 2025, 12:00:10
        20240229083040,  # February 29, 2024 (leap year), 08:30:40
        20251231115959,  # December 31, 2025, 11:59:59
        20230822104550,  # August 22, 2023, 10:45:50
        20230822102035,  # August 22, 2023, 10:20:35
    ]

    cursor.execute("SELECT COUNT(*) FROM dates")
    check = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    
    if check == 0:
        for date in dates:
            insert_date(date)
    
def insert_date(date_int): 
    year = int(str(date_int)[:4])
    month = int(str(date_int)[4:6])
    day = int(str(date_int)[6:8])
    hour = int(str(date_int)[8:10])
    minute = int(str(date_int)[10:12])
    second = int(str(date_int)[12:])
    
    insert_query = "INSERT INTO dates (year,month,day,hour,minute,second) VALUES (?,?,?,?,?,?)"
    execute_query(insert_query, year, month,day, hour, minute, second)

def execute_query(query, *args):
    print("args", args)
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()