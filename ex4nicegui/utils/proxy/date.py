from . import utils
import datetime


class DateProxy(datetime.date):
    def __new__(cls, year, month=None, day=None):
        return super().__new__(cls, year, month, day)

    def __init__(self, year, month, day):
        from ex4nicegui.utils.signals import to_ref

        self._ref = to_ref(datetime.date(year, month, day))

    def __str__(self):
        return str(self._ref.value)

    def ctime(self):
        return self._ref.value.ctime()

    def strftime(self, fmt):
        return self._ref.value.strftime(fmt)

    def __format__(self, fmt):
        return self._ref.value.__format__(fmt)

    def isoformat(self):
        return self._ref.value.isoformat()

    @property
    def year(self):
        return self._ref.value.year

    @property
    def month(self):
        return self._ref.value.month

    @property
    def day(self):
        return self._ref.value.day

    def timetuple(self):
        return self._ref.value.timetuple()

    def toordinal(self):
        return self._ref.value.toordinal()

    def replace(self, year=None, month=None, day=None):
        return self._ref.value.replace(year=year, month=month, day=day)

    def __eq__(self, other):
        return self._ref.value.__eq__(utils.to_value(other))

    def __le__(self, other):
        return self._ref.value.__le__(utils.to_value(other))

    def __lt__(self, other):
        return self._ref.value.__lt__(utils.to_value(other))

    def __ge__(self, other):
        return self._ref.value.__ge__(utils.to_value(other))

    def __gt__(self, other):
        return self._ref.value.__gt__(utils.to_value(other))

    def __hash__(self):
        return self._ref.value.__hash__()

    def __add__(self, other):
        return self._ref.value.__add__(utils.to_value(other))

    def __radd__(self, other):
        return self._ref.value.__radd__(utils.to_value(other))

    def __sub__(self, other):
        return self._ref.value.__sub__(utils.to_value(other))

    def weekday(self):
        return self._ref.value.weekday()

    def isoweekday(self):
        return self._ref.value.isoweekday()

    def isocalendar(self):
        return self._ref.value.isocalendar()

    def __reduce__(self):
        return self._ref.value.__reduce__()
