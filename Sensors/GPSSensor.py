#! /usr/bin/python
from gps import *


class GPSSensor():
	def __init__(self):
		self.gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
		self.report = 0
		self.data = dict()

	def Read(self):
		try:
			self.report = self.gpsd.next()
			if self.report['class'] == 'TPV':
				report = self.report
				self.data = {'lat': getattr(report, 'lat', 0.0),
				       'lon': getattr(report, 'lon', 0.0),
				       'time': getattr(report, 'time', ''),
				       'alt': getattr(report, 'alt', 'nan'),
				       'epv': getattr(report, 'epv', 'nan'),
				       'ept': getattr(report, 'ept', 'nan'),
				       'speed': getattr(report, 'speed', 'nan'),
				       'climb': getattr(report, 'climb', 'nan')}
			else :
				self.data = {'lat': 0,
				       'lon': 0,
				       'time': '',
				       'alt': 'nan',
				       'epv': 'nan',
				       'ept': 'nan',
				       'speed': 'nan',
				       'climb': 'nan'}
			return self.data
		except (KeyboardInterrupt, SystemExit):
			return -1
