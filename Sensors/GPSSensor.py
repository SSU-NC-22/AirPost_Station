#! /usr/bin/python
from gps import *
import threading


class GPSSensor():
    def __init__(self):
        self.gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.report = 0
        self.data = dict()

        def ReadGPS():
            while True:
                self.report = self.gpsd.next()

        self.thread = threading.Thread(target=ReadGPS)
        self.thread.daemon = True
        self.thread.start()

    def Read(self):
        if self.report['class'] == 'TPV':
            report = self.report
            self.data = {'lat': getattr(report, 'lat', None),
                         'lon': getattr(report, 'lon', None),
                         'time': getattr(report, 'time', None),
                         'alt': getattr(report, 'alt', None),
                         'epv': getattr(report, 'epv', None),
                         'ept': getattr(report, 'ept', None),
                         'speed': getattr(report, 'speed', None),
                         'climb': getattr(report, 'climb', None)}
        else:
            self.data = {'lat': None,
                         'lon': None,
                         'time': None,
                         'alt': None,
                         'epv': None,
                         'ept': None,
                         'speed': None,
                         'climb': None}
            return self.data
