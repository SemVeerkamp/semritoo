from website.get_event_code import get_event_code
import requests
import json
from datetime import datetime
from datetime import timedelta

def get_events(year,tag):
    time_difference_hours = 1
    event_code = get_event_code(year, tag)
    url_events='https://api.isuresults.eu/events/'+event_code+'/competitions/'
    response_events = requests.get(url_events)
    response_dict = json.loads(response_events.text)
    events = []
    starttimes = []
    scheduleNumbers=[]
    for i in range(len(response_dict)):
        events.append(response_dict[i]['title'])
        scheduleNumbers.append(str(response_dict[i]['scheduleNumber']))
        date = datetime.strptime(response_dict[i]['start'], '%Y-%m-%dT%H:%M:%SZ')
        date = date + timedelta(hours=time_difference_hours)
        starttimes.append(date)
    return scheduleNumbers, events, starttimes




