from datetime import datetime, timedelta
import pandas as pd

def split_dates_into_weeks(dates, start_day_of_week=0): # 0 for Monday, 6 for Sunday
    weeks = {}
    #for date_str in dates:
    for row in dates.itertuples():
        date_obj = datetime.strptime(row.Date, "%d/%m/%Y")
        
        # Determine the start of the week for the current date
        day_of_week = date_obj.weekday() # Monday is 0, Sunday is 6
        days_to_subtract = (day_of_week - start_day_of_week + 7) % 7
        week_start = date_obj - timedelta(days=days_to_subtract)
        
        # Use a consistent key for the week (e.g., the week's start date)
        week_key = week_start.strftime("%d/%m/%Y")
        
        if week_key not in weeks:
            weeks[week_key] = row

        elif float(weeks[week_key].High.replace(',','')) < float(row.High.replace(',','')):
            weeks[week_key] = row

    days = {
        "Monday": 0, 
        "Tuesday": 0, 
        "Wednesday": 0, 
        "Thursday": 0, 
        "Friday": 0
    }

    for day in weeks.values():
        dayname = datetime.strptime(day.Date, "%d/%m/%Y").strftime("%A")
        if dayname and dayname != "Saturday" and dayname != "Sunday":
            days[dayname] += 1

    return days

def findHigh():
    # Find which day is most likely to create the high of the week
    columns = ["Date", "Price", "Open", "High", "Low", "Vol.", "Change %"]
    nasdaq_data = pd.read_csv("DataFiles\\Nasdaq 100 Futures Historical Data.csv")
    weekly_dates = split_dates_into_weeks(nasdaq_data)
    return weekly_dates

def findLow():
    # Find which day is most likely to create the low of the week
    return


if __name__ == "__main__":
    print(findHigh())