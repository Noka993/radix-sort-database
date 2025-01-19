from flask import Flask, flash, render_template, request, redirect, url_for
from helpers.radix_sort import convert_dates_to_strings, radix_sort
from helpers.database import initialise_db, insert_date, execute_query
from helpers.dates import load_dates
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'

initialise_db()

@app.route('/add', methods=['POST'])
def add_date():
    date_str = request.form['date']
    if not date_str:
        flash("No date provided!")
        return redirect(url_for('index'))
    
    if len(date_str) == 16:  # Format: "YYYY-MM-DDTHH:MM"
        date_str += ":00"

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
            
        insert_date(date_int)

    except ValueError as e:
        flash(f"Invalid date format!")
    
    finally:
        return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_date():
    id = request.form['id']
    delete_query = 'DELETE FROM dates WHERE id = ?'
    execute_query(delete_query, id)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    just_id, just_dates = load_dates()
    just_dates_int = [int(date) for date in just_dates]
    
    converted_dates = convert_dates_to_strings(just_dates_int)
    sorted_dates = convert_dates_to_strings(radix_sort(just_dates_int))
    
    return render_template('index.html', ids=just_id, dates=converted_dates, sorted_dates=sorted_dates)

if __name__ == '__main__':
    app.run(debug=True)
