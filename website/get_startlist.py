from website.get_event_code import get_event_code
from website.get_events import get_events
import requests
import json


def get_startlist(year, tag):
    event_code = get_event_code(year, tag)
    scheduleNumbers, events_with_spaces, starttimes = get_events(year, tag)
    events = []
    for q in events_with_spaces:
        r = q.replace(' ', '')
        events.append(r)

    # Get the startlists
    startlist = {}
    names = []
    startnumbers = []
    numbers_list = {}
    for i in range(len(scheduleNumbers)):
        quarter = "Quarter"
        semi = "Semi"
        if quarter not in events[i]:
            if semi not in events[i]:
                response_startlist = requests.get('https://api.isuresults.eu/events/'
                                                  + event_code
                                                  + '/competitions/'
                                                  + scheduleNumbers[i]
                                                  + '/start-list/'
                                                  )
                response_startlist_dict = json.loads(response_startlist.text)
                for j in range(len(response_startlist_dict)):
                    if response_startlist_dict[j]:
                        key = 'competitor'
                        if key in response_startlist_dict[j]:
                            Full_name = str(response_startlist_dict[j]['competitor']['skater']['firstName']
                                            + " "
                                            + response_startlist_dict[j]['competitor']['skater']['lastName']
                                            + "   ("
                                            + response_startlist_dict[j]['competitor']['skater']['country']
                                            + ")"
                                            )
                            number = str(response_startlist_dict[j]['competitor']['skater']['id'])
                            names.append(Full_name)
                            startnumbers.append(number)
                            startlist[str("startlist_" + events[i])] = names
                            numbers_list[str("startlist_" + events[i])] = startnumbers
        #                key2 = 'team'
        #                if key2 in response_startlist_dict[j]:
        #                    Full_name = str(response_startlist_dict[j]['team']['country'])
        #                    names.append(Full_name)

        names = []
        startnumbers = []
    scheduled_events = []
    scheduled_starttimes = []
    quarter = 'Quarter'
    semi = 'Semi'
    team = 'Team'
    for index, event in enumerate(events):
        if quarter not in event:
            if semi not in event:
                if team not in event:
                    scheduled_events.append(event)
                    scheduled_starttimes.append(starttimes[index])
    return startlist, starttimes, events, scheduled_starttimes, scheduled_events, numbers_list
