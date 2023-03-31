import pytz
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime
from pydantic import BaseModel
from typing import Optional


class Time(BaseModel):
    today_date: Optional[str]
    hour: Optional[str]
    minute: Optional[str]
    times: Optional[str]
    name_of_day: Optional[str]


def time() -> Time:
    today_date = JalaliDate(JalaliDate.today()).strftime("%Y_%m_%d")
    date_spilted = today_date.split('_')
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    times = '{}:{}'.format(hour, minute)
    prz = JalaliDateTime(int(date_spilted[0]), int(date_spilted[1]), int(date_spilted[2]), hour, minute, 0, 0,
                         pytz.utc).strftime("%c")
    name_of_day = prz.split(' ')[0]
    return_date = Time()
    return_date.today_date = today_date
    return_date.hour = hour
    return_date.minute = minute
    return_date.times = times
    return_date.name_of_day = name_of_day

    return return_date



