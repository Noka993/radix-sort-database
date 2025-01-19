from flask import Flask, render_template
from helpers.radix_sort import convert_dates_to_strings, radix_sort

app = Flask(__name__)


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


@app.route('/')
def index():
    converted_dates = convert_dates_to_strings(dates)
    sorted_dates = convert_dates_to_strings(radix_sort(dates))
    print(sorted_dates)
    return render_template('index.html', dates=converted_dates, sorted_dates=sorted_dates)

if __name__ == '__main__':
    app.run(debug=True)
