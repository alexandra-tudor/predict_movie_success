import datetime
import sys
from pandas.tseries.holiday import USFederalHolidayCalendar


class HolidayCalendar:
	holidays = []

	def __init__(self):
		US_calendar = USFederalHolidayCalendar()
		self.holidays = US_calendar.holidays(start='1900-01-01', end='2017-03-31').to_pydatetime()

	def is_US_holiday(self, day, month, year):
		return datetime.datetime(year, month, day) in self.holidays

if __name__ == "__main__":
	args = sys.argv
	print (args)
	print (len(args))
