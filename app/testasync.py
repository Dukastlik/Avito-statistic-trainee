from datetime import datetime


ex = '2020-12-11-01'

my_date_time = datetime.strptime(ex, "%Y-%m-%d-%H")
print(my_date_time.timestamp())
now_time = datetime.now().timestamp()
today_time = datetime.today().timestamp()
print(now_time, today_time)
#timestamp = datetime.timestamp(now_time)
#print(type(timestamp))

