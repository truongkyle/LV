import time
import datetime
# start = datetime.datetime.now()
# time.sleep(10)
# end = datetime.datetime.now()
# duration = end - start
now = datetime.datetime.now()
current_day = now.strftime("%H:%M:%S")
print(current_day)