import datetime


def prep_data(data: dict):
    """Takes a dict intended to be converted to JSON for use with Google Charts and transforms dates and datetimes
    into date string representations as described here:

    https://developers.google.com/chart/interactive/docs/datesandtimes

    TODO:  Implement Timeofday formatting"""

    for row in data['rows']:
        for val in row['c']:
            if isinstance(val['v'], datetime.datetime):
                val['v'] = "Date({}, {}, {})".format(val['v'].year,
                                                     val['v'].month-1,  # JS Dates are 0-based
                                                     val['v'].day,
                                                     val['v'].hour,
                                                     val['v'].minute,
                                                     val['v'].second,
                                                     val['v'].microsecond)
            elif isinstance(val['v'], datetime.date):
                val['v'] = "Date({}, {}, {})".format(val['v'].year,
                                                     val['v'].month-1,  # JS Dates are 0-based
                                                     val['v'].day)
    return data
