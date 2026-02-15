import psycopg2
from ics import Calendar, Event
from datetime import datetime

import supersecrets as shh

OUTPUT_FILE = f"/output/{shh.CAL_ID}.ics"

DB_PARAMS = {'host': shh.db_ip,
			 'user': shh.db_user,
			 'dbname': shh.db_name1,
			 'password': shh.db_password,
			 'port': shh.db_port}

class REC_Event():
    def __init__(self, title, start, end, location):
        self.title = title
        self.start = start
        self.end = end
        self.location = location

    def make_event(self):
        e = Event()
        e.name = self.title
        e.begin = self.start
        e.end = self.end
        e.location = self.location

        return e

def log(msg):
	print(f"{[datetime.now().strftime('%H:%M:%S')]} {msg}", flush = True)

def pull_events():
    log("Pulling Events")
	
    sql = """
    SELECT event_title, start_time, end_time, event_loc
	FROM prd.edr_calevents
	WHERE event_desc NOT LIKE '%CANCELED%'
	"""

    with psycopg2.connect(**DB_PARAMS) as home:
        with home.cursor() as cur:
            cur.execute(sql)
            pull = cur.fetchall()

            allevents = [REC_Event(*i) for i in pull]

    log("Events Pulled")
    return allevents

def make_calendar(events_array):
    log("Making Calendar")

    cal = Calendar()
    for ev in events_array:
         
         e = ev.make_event()
         cal.events.add(e)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(cal.serialize())
    log("Calendar Made")

if __name__ == "__main__":
    log("Starting!")
    calevents = pull_events()
    make_calendar(calevents)
    log("Done!")



	

