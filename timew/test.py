from datetime import date, datetime, time, timedelta
from time import sleep

from timewarrior import Timewarrior

tw = Timewarrior()

# task = tw.get_id(['first tag'])

tw.delete(1)

# ['#SND-22: Use ORM for database access', 'dev', 'westmont', 'westmont.dev'
# print(task)
# d = date(2018, 4, 22)
# st = time(18, 00)
# sdt = datetime.combine(d, st)
# et = time(18, 10)
# edt = datetime.combine(d, et)
# delta = timedelta(seconds=100)
# tw.track(sdt, delta, tags=['first tag'])
