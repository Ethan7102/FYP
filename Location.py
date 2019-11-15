import pytz
import datetime as dt
import geocoder

g = geocoder.ip('me')
print (g.city)


hktz = pytz.timezone('Asia/Hong_Kong')
print(dt.datetime.now(hktz).strftime('%Y-%m-%d %H:%M:%S'))

