from datetime import datetime

def format_date(date):
    return datetime.strptime(date.rsplit(".")[0], "%Y-%m-%d %H:%M:%S")