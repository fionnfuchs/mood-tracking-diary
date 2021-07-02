import re
from datetime import datetime
import pytz


def validate_current_time(message_text):

    time_formats = [re.compile(r"[0-9]{1,2}:[0-9]{1,2}"), re.compile(r"[0-9]{1,2}")]

    for exp in time_formats:
        if exp.search(message_text):
            return True

    return False


def get_timezone_by_current_time(message_text):

    time_format_1 = re.compile(r"[0-9]{1,2}:[0-9]{1,2}")
    time_format_2 = re.compile(r"[0-9]{1,2}")

    matches = re.findall(time_format_1, message_text)
    if len(matches) > 0:
        hours = int(matches[0].split(":")[0])
        return get_timezone_by_hours(hours)

    matches = re.findall(time_format_2, message_text)
    if len(matches) > 0:
        hours = int(matches[0])
        return get_timezone_by_hours(hours)

    return None


def get_polltime_by_message_time(message_text):
    time_format_1 = re.compile(r"[0-9]{1,2}:[0-9]{1,2}")
    time_format_2 = re.compile(r"[0-9]{1,2}")

    matches = re.findall(time_format_1, message_text)
    if len(matches) > 0:
        hours = int(matches[0].split(":")[0])
        return hours

    matches = re.findall(time_format_2, message_text)
    if len(matches) > 0:
        hours = int(matches[0])
        return hours

    return None


def get_timezone_by_hours(hours):

    tz_utc = pytz.utc
    time = datetime.now(tz_utc)

    utc_offset = hours - time.hour

    for timezone in pytz.common_timezones:
        tz = pytz.timezone(timezone)
        utc_tz_offset = int(datetime.now(tz).utcoffset().total_seconds() / 3600)
        if utc_offset == utc_tz_offset:
            return timezone

    return "Europe/Berlin"