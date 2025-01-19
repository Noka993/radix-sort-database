from flask import Flask, flash, render_template, request, redirect, url_for
from helpers.radix_sort import convert_dates_to_strings, radix_sort
import sqlite3
from datetime import datetime

def initialise_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER NOT NULL
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
    if check == 0:
        for date in dates:
            cursor.execute("INSERT INTO dates (date) VALUES (?)", (date,))
    connection.commit()
    connection.close()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

initialise_db()

@app.route('/add', methods=['POST'])
def add_date():
    date_str = request.form['date']
    if not date_str:
        flash("No date provided!")
        return redirect(url_for('index'))
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        if date.year < 1000:
            flash("Year must be at least 1000!")
            return redirect(url_for('index'))
        # Convert date to integer format YYYYMMDDhhmmss
        date_int = int(date.strftime("%Y%m%d%H%M%S"))

        # Ensure the date is not in the future
        now_int = int(datetime.now().strftime("%Y%m%d%H%M%S"))
        if date_int > now_int:
            flash("You cannot add a future date!")
            return redirect(url_for('index'))
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO dates (date) VALUES (?)', (date_int,))
        connection.commit()
        connection.close()

    except ValueError:
        flash("Invalid date format!")
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_date():
    id = request.form['id']
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM dates WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    dates_db = connection.execute("SELECT id, date from dates").fetchall()
    just_dates = []
    just_id = []
    for date in dates_db:
        just_id.append(date[0])
        just_dates.append(date[1])
    converted_dates = convert_dates_to_strings(just_dates)
    sorted_dates = convert_dates_to_strings(radix_sort(just_dates))
    return render_template('index.html', ids=just_id, dates=converted_dates, sorted_dates=sorted_dates)

if __name__ == '__main__':
    app.run(debug=True)
