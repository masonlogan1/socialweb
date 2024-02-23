import re
from datetime import datetime
from types import NoneType

AS2_TIME = re.compile(
    r'(0\d|1\d|2[0123]):[012345]\d(:([012345]\d|60))?[\.\-+Z]')
AS2_TZ = re.compile(r'(Z?[\-+](0\d|1\d|2[0123]):[012345]\d)$')

AS2_DATE_TIME = re.compile(r'\d{4}-' +  # year
                           r'(0[1-9]|1[012])-' +  # month (1-12)
                           r'(0[1-9]|1\d|2\d|3[01])' +  # day (1-31)
                           r'T' +  # mandatory T
                           r'(0\d|1\d|2[0123])' +  # hour (00-23)
                           r':[012345]\d' +  # minute (00-59)
                           r'(:([012345]\d|60))?' +  # second (00-60)
                           r'(\.\d{1,6})?' +  # fraction (6 digit int)
                           # mandatory Z if no timezone
                           # optional Z and timezone (+|-)(00-23):(00-59))
                           r'(Z|(Z?[\-+](0\d|1\d|2[0123]):[012345]\d))$')


def is_activity_datetime(val, prop='', **kwargs):
    if isinstance(val, NoneType):
        return
    if isinstance(val, datetime):
        return True
    if isinstance(val, str) and re.search(AS2_DATE_TIME, val) is None:
        raise ValueError(
            f'Property "{prop}" must be in "YYYY-mm-dd-THH:MM:SSZ" format; ' +
            f'got {val} ({type(val)})')


def parse_activitystream_datetime(val):
    if isinstance(val, (datetime, NoneType)):
        return val
    dt_str = '%Y-%m-%dT%H:%M'
    val_time = re.search(AS2_TIME, val)
    # 9 characters indicates seconds have been included
    dt_str += ':%S' if val_time.span()[1] - val_time.span()[0] == 9 else ''
    dt_str += '.%f' if '.' in val else ''
    dt_str += 'Z' if not re.search(AS2_TZ, val) else (
        'Z%z' if 'Z' in val else '%z')
    return datetime.strptime(val, dt_str)


def timedelta_str(obj) -> str:
    """
    Converts a timedelta to an ISO 8601 string
    :param obj: timedelta to convert
    :return: "P<years>Y<months>M<days>DT<hours>H<minutes>M<seconds>S" string
    """
    years = obj.days // 365
    months = (obj.days % 365) // 30
    days = (obj.days % 365) % 30
    hours = obj.seconds // 3600
    minutes = (obj.seconds % 3600) // 60
    seconds = (obj.seconds % 3600) % 60
    # P<years>Y<months>M<days>D
    ymd = 'P' + (f'{years}Y' if years else '') + \
          (f'{months}M' if months else '') + \
          (f'{days}D' if days else '')
    # T<hours>H<minutes>M<seconds>S
    hms = 'T' + (f'{hours}H' if hours else '') + \
          (f'{minutes}M' if minutes else '') + \
          (f'{seconds}S' if seconds else '')
    # The entire HMS section is optional, however we ALWAYS need at least the
    # "P" from the ymd section (indicates this is a "period")
    return f'{ymd}{hms if len(hms) > 1 else ""}'


def datetime_str(obj: datetime) -> str:
    """
    Converts a datetime object to ISO 8601 format
    :param obj: the datetime object to convert
    :return: "YYYY-mm-ddTHH:MM:SSZ" string
    """
    # TODO: implement handling for timezone-aware datetimes
    # TODO: implement millisecond handling
    return obj.strftime('%Y-%m-%dT%H:%M:%SZ')