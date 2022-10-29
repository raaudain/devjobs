from datetime import datetime

def date_formatter(date):
    date = date.replace("T", " ")
    return datetime.strptime(date.rsplit(".")[0], "%Y-%m-%d %H:%M:%S")