"""
Utility functions

today()               return today's date as datetime.date
set_today(new_date)   set the date that today() should return
parse_date(date|str)  return a datetime.date for parameter which can
                      be either a date or string in the form "yyyy-mm-dd"
"""
import datetime

# See set_today() and today() for meaning of __today.
__today = None


def parse_date(date_value: str|datetime.date) -> datetime.date:
    """Return a date object from date_value, which can be a 
    string in the form "yyyy-mm-dd" or datetime.date.
    
    :raises ValueError: if date_value cannot be parsed
    :raises TypeError:  if date_value is neither str or datetime.date
    """
    if isinstance(date_value, str):
        try:
            # strptime parse a date/time string according to a format
            return datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
        except Exception:
            raise ValueError(f'Invalid date string "{date_value}"')
    elif isinstance(date_value, datetime.date):
        # param is already a date
        return date_value
    else:
        raise TypeError("Argument must be string or date object")


def today():
    """Return today's date as a datetime.date.

    If set_today() is invoked first, this method uses that value as
    today's date. Otherwise, it uses the value of `datetime.date.today()`.

    Our app calls this method wherever the current date is needed.
    This is so we can change the value of "today" for testing.

    :returns: Today's date. Either the actual value or value from set_today.
    """
    global __today
    return __today if __today else datetime.date.today()


def set_today(today: str|datetime.date) -> None:
    """Set today's date to the parameter value.
    Once set, the library application will use this date instead of the
    actual value of today.

    :param today: date object or string in the form "yyyy-mm-dd" for today's date.
    """
    global __today 
    __today = parse_date(today)