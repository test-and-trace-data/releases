from datetime import datetime

import dateutil.parser


def formatdatestring(date_string):
    """Filter for formatting a date string in a Jinja template."""
    try:
        # check if this is an ISO date string with no time, just a date
        datetime.strptime(date_string, "%Y-%m-%d")
        # if so, then return the date only
        parsed = dateutil.parser.parse(date_string)
        return parsed.strftime("%d %B %Y")
    except ValueError:
        parsed = dateutil.parser.parse(date_string)
        return parsed.strftime("%d %B %Y, %H:%M")
