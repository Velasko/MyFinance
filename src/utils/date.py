import datetime

from dateutil.relativedelta import relativedelta

ms = relativedelta(microseconds=1)
minute = relativedelta(minute=1)
sec = relativedelta(seconds=1)
hour = relativedelta(hours=1)
day = relativedelta(days=1)
week = relativedelta(weeks=1)
month = relativedelta(months=1)
year = relativedelta(years=1)

def string_to_date(date):
	date = date.replace('-', '/')

	date = '01/'*(2-date.count('/')) + date

	try:
		ret = datetime.datetime.strptime(date,"%d/%m/%y")
	except ValueError:
		try:
			ret = datetime.datetime.strptime(date,"%d/%m/%Y")
		except ValueError:
			raise ValueError('date must be dd/mm/yy or dd/mm/yyyy format')

	return ret

def string_to_interval(date):
	date = date.replace('-', '/')

	initial_date_str = '01/'*(2-date.count('/')) + date

	try:
		initial_date = datetime.datetime.strptime(initial_date_str,"%d/%m/%y")
	except ValueError:
		try:
			initial_date = datetime.datetime.strptime(initial_date_str,"%d/%m/%Y")
		except ValueError:
			raise ValueError('date must be on dd/mm/yy or dd/mm/yyyy format')

	final_date = initial_date + (year, month, day)[date.count('/')] - ms

	return initial_date, final_date

def slice_by_date(index):
	if isinstance(index, str):
		date_interval = string_to_interval(index)
	elif isinstance(index, slice):
		start = string_to_date(index.start) if isinstance(index.start, str) else index.start
		end = string_to_date(index.stop) if isinstance(index.stop, str) else index.stop
		date_interval = (start, end-ms)

	return date_interval


if __file__ == '__main__':
	string_to_date('02/03/21')