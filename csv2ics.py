from csv import DictReader
from datetime import datetime, timedelta
import sys

from icalendar import Calendar, Event, vDate, vDatetime


class DateParseError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "Parse error: " + self.value

        
def mk_time(value):
    try:
        return vDate(datetime.strptime(value, "%a %b %d %Y"))
    except ValueError:
        try:
            return vDatetime(datetime.strptime(value, "%a %b %d %H:%M %Y"))
        except ValueError:
            raise DateParseError(value)

 
if __name__ == '__main__':
    cal = Calendar()
    cal.add('prodid', '-//shaleh c2v 2 ical//shaleh//')
    cal.add('version', '2.0')

    with open(sys.argv[1]) as fp:
        reader = DictReader(fp)
        for item in reader:
            start = mk_time(item['start'])
            end = mk_time(item['end'])

            event = Event()
            event.add('summary', item['summary'])
            event.add('description', item['description'])
            event.add('dtstart', start)
            event.add('dtend', end)

            cal.add_component(event)

    print cal.to_ical()
