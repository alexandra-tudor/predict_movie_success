import pytrends
from pytrends.request import TrendReq

pytrends = TrendReq('', '', hl='en-US', tz=360, custom_useragent=None)
pytrends.build_payload(["Star Wars"], timeframe='today 5-y')

print (pytrends.interest_over_time())

