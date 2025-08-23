from datetime import datetime, timedelta
import pandas as pd

def findWeeklyHigh():
    # Find which day is most likely to create the high of the week
    columns = ["Date", "Price", "Open", "High", "Low", "Vol.", "Change %"]
    nasdaq_data = pd.read_csv("DataFiles\\Nasdaq 100 Futures Historical Data.csv")
    start_day_of_week=0
    weeks = {}

    #for date_str in dates:
    for row in nasdaq_data.itertuples():
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

def findWeeklyLow():
    # Find which day is most likely to create the low of the week
    columns = ["Date", "Price", "Open", "High", "Low", "Vol.", "Change %"]
    nasdaq_data = pd.read_csv("DataFiles\\Nasdaq 100 Futures Historical Data.csv")
    start_day_of_week=0
    weeks = {}
    
    #for date_str in dates:
    for row in nasdaq_data.itertuples():
        date_obj = datetime.strptime(row.Date, "%d/%m/%Y")
        
        # Determine the start of the week for the current date
        day_of_week = date_obj.weekday() # Monday is 0, Sunday is 6
        days_to_subtract = (day_of_week - start_day_of_week + 7) % 7
        week_start = date_obj - timedelta(days=days_to_subtract)
        
        # Use a consistent key for the week (e.g., the week's start date)
        week_key = week_start.strftime("%d/%m/%Y")
        
        if week_key not in weeks:
            weeks[week_key] = row

        elif float(weeks[week_key].Low.replace(',','')) > float(row.Low.replace(',','')):
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

def dailyVolatility():
    # Find which day is most volatile
    nasdaq_data = pd.read_csv("DataFiles\\Nasdaq 100 Futures Historical Data.csv")
    nasdaq_data.columns = nasdaq_data.columns.str.replace(' %', '')
    days = {
        "Monday": {"Counter": 0, "Percentage": 0}, 
        "Tuesday": {"Counter": 0, "Percentage": 0}, 
        "Wednesday": {"Counter": 0, "Percentage": 0}, 
        "Thursday": {"Counter": 0, "Percentage": 0}, 
        "Friday": {"Counter": 0, "Percentage": 0}
    }
    
    #for date_str in dates:
    for row in nasdaq_data.itertuples():
        dayname = datetime.strptime(row.Date, "%d/%m/%Y").strftime("%A")
        
        if dayname and dayname != "Saturday" and dayname != "Sunday":
            days[dayname]["Counter"] += 1
            days[dayname]["Percentage"] += abs(float(row.Change[:-1]))
    
    for day in days:
        days[day] = round(days[day]["Percentage"]/days[day]["Counter"], 2)

    return days

def dailydirection(): 
    # Find whether a day of the week is more likely to be bullish or bearish
    nasdaq_data = pd.read_csv("DataFiles\\Nasdaq 100 Futures Historical Data.csv")
    nasdaq_data.columns = nasdaq_data.columns.str.replace(' %', '')
    days = {
        "Monday": {"Bullish": 0, "Bearish": 0}, 
        "Tuesday": {"Bullish": 0, "Bearish": 0}, 
        "Wednesday": {"Bullish": 0, "Bearish": 0}, 
        "Thursday": {"Bullish": 0, "Bearish": 0}, 
        "Friday": {"Bullish": 0, "Bearish": 0}
    }
    
    #for date_str in dates:
    for row in nasdaq_data.itertuples():
        dayname = datetime.strptime(row.Date, "%d/%m/%Y").strftime("%A")
        
        if dayname and dayname != "Saturday" and dayname != "Sunday":
            if row.Change[0] == "-": 
                days[dayname]["Bearish"] += 1
            else: 
                days[dayname]["Bullish"] += 1
    return days

def findYearlyHigh():
    # Find which month is most likely to create the high of the year


    return

def findYearlyLow():
    # Find which month is most likely to create the low of the year


    return

if __name__ == "__main__":
    print(findWeeklyHigh())
    print(findWeeklyLow())
    print(dailyVolatility())
    print(dailydirection())