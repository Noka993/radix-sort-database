import sqlite3

def load_dates():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    dates_db = connection.execute("SELECT * from dates").fetchall()
    just_dates = []
    just_id = []
    
    if dates_db:
        for date in dates_db:
            just_id.append(date[0])
            date_str = str(date[1])  
            for j in range(2, 7):  
                date_str += f"{date[j]:02d}" 
            just_dates.append(date_str)
    
    connection.close()
    return just_id, just_dates