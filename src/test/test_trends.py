from pytrends.request import TrendReq

pytrend = TrendReq('', '', hl='en-US', tz=360, custom_useragent=None)
pytrend.build_payload(["Star Wars"], timeframe='today 5-y')

print (pytrend.interest_over_time())

