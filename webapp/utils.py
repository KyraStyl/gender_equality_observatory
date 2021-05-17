import datetime

def to_date(text):
    day, month, year = [int(date_part) for date_part in text.split("/")]
    return datetime.date(year, month, day)
