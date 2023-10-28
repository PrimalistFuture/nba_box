from datetime import date, timedelta

def strip_date(datetime_dict):
    """Given datetime obj, returns string of year-month-day
    Input = datetime_dict like datetime.date(2023,10,13)
    Output = '2023-10-13'
    """

    if type(datetime_dict) is not date:
        raise TypeError

    singles = [1,2,3,4,5,6,7,8,9]

    year = datetime_dict.year

    month = datetime_dict.month
    if month in singles:
        month = f'0{month}'

    day = datetime_dict.day
    if day in singles:
        day = f'0{day}'

    return f'{year}-{month}-{day}'

def populate_days_of_this_past_week(datetime):
    """Given a datetime obj, returns an array of stringed dates from the past week
    Input: datetime_dict like datetime.date(2023,10,20)
    Output: ['2023-10-20', '2023-10-19', ... '2023-10-13']
    """

    if type(datetime) is not date:
        raise TypeError

    today = timedelta(days=0)
    one_day = timedelta(days=1)
    two_day = timedelta(days=2)
    three_day = timedelta(days=3)
    four_day = timedelta(days=4)
    five_day = timedelta(days=5)
    six_day = timedelta(days=6)
    seven_day = timedelta(days=7)
    days = [today, one_day, two_day, three_day, four_day, five_day, six_day, seven_day]
    all_days_of_this_past_week = [strip_date(datetime - day) for day in days]

    return all_days_of_this_past_week