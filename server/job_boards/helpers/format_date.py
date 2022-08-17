from datetime import datetime

def format_date(date):
    date = date.replace("T", " ")
    return datetime.strptime(date.rsplit(".")[0], "%Y-%m-%d %H:%M:%S")