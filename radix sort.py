from datetime import datetime

def convert_dates_to_strings(dates):
    formatted_dates = []
    for date_int in dates:
        # Convert the integer to a string
        date_str = str(date_int)
        
        # Extract the year, month, day, hour, and minute
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        hour = int(date_str[8:10])
        minute = int(date_str[10:12])
        
        # Create a datetime object
        dt = datetime(year, month, day, hour, minute)
        
        # Format the datetime object into a readable string
        formatted_date = dt.strftime("%B %d, %Y, %H:%M")
        formatted_dates.append(formatted_date)
    
    return formatted_dates

def radix_sort(arr):
    # 
    max_digits = max([len(str(x)) for x in arr])

    base = 10

    bins = [[] for _ in range(base)]

    for i in range(0, max_digits):
        # Iterate through the elements in the list
        for x in arr:
            # Extract the i-th digit from the element
            # (starting from the rightest digit)
            digit = (x // base ** i) % base
            # Add the element to the bin for the i-th digit
            bins[digit].append(x)
        # Combine the bins back into the list, starting with the elements in the 0 queue
        arr = [x for queue in bins for x in queue]
        # Clear the bins for the next iteration
        bins = [[] for _ in range(base)]

    return arr


dates = [
    202501161845,  # January 16, 2025, 18:45
    202312251230,  # December 25, 2023, 12:30
    202411081500,  # November 8, 2024, 15:00
    202510300715,  # October 30, 2025, 07:15
    202604012259,  # April 1, 2026, 22:59
    202308221030,  # August 22, 2023, 10:30
    202707040000,  # July 4, 2027, 00:00
    202510311200,  # October 31, 2025, 12:00
    202402290830,  # February 29, 2024 (leap year), 08:30
    202512311159,   # December 31, 2025, 11:59
    202308221045,  # August 22, 2023, 10:45
    202308221020,  # August 22, 2023, 10:20
]

dates = convert_dates_to_strings(radix_sort(dates))

for date in dates:
    print(date)

