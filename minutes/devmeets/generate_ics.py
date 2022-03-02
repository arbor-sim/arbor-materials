#!/usr/bin/env python3

from icalendar import Calendar, Event
from pytz import timezone
from datetime import datetime
from pathlib import Path

cal = Calendar()
cal.add('prodid', '-//The Arbor Calender Generator//')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Arbor Developer Meeting')
event.add('dtstart', datetime(2022, 3, 2, 10, 0, 0, tzinfo=timezone('Europe/Amsterdam')))
event.add('dtend', datetime(2022, 3, 2, 13, 0, 0, tzinfo=timezone('Europe/Amsterdam')))
event.add('location', 'https://webconf.fz-juelich.de/b/hui-clp-qgu-ypp')
event.add('description', '''
          Agenda and minutes: https://github.com/arbor-sim/arbor-materials/blob/master/minutes/devmeets/
          Meeting coordinate: https://webconf.fz-juelich.de/b/hui-clp-qgu-ypp
          Arbor dev kanban: https://github.com/orgs/arbor-sim/projects/3
          ''')
        
cal.add_component(event)

with open(Path(__file__).parent / 'next-dev-meet.ics', 'wb') as f:
    f.write(cal.to_ical())
    f.close()
