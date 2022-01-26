from website.get_event_code import get_event_code
from website.get_events import get_events
import requests
import json


def get_result(year, tag):
    event_code = get_event_code(year, tag)
    scheduleNumbers, events_with_spaces, starttimes = get_events(year, tag)
    events = []
    for q in events_with_spaces:
        r = q.replace(' ', '')
        events.append(r)

    # Get the results
    results = {}
    names = []
    result_times = {}
    times = []
    podium_pictures = {}
    podium_event = []

    for i in range(len(scheduleNumbers)):
        response_result = requests.get('https://api.isuresults.eu/events/'
                                       + event_code
                                       + '/competitions/'
                                       + scheduleNumbers[i]
                                       + '/results/'
                                       )
        response_result_dict = json.loads(response_result.text)
        for j in range(len(response_result_dict)):
            if response_result_dict[j]:
                if response_result_dict[j]['time'] is not None:
                    key = 'competitor'
                    if key in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['competitor']['skater']['firstName']
                                        + " "
                                        + response_result_dict[j]['competitor']['skater']['lastName']
                                        + "   ("
                                        + response_result_dict[j]['competitor']['skater']['country']
                                        + ")"
                                        )
                        time = str(response_result_dict[j]['time']
                                   )
                        if j < 3:
                            podium_url = response_result_dict[j]['competitor']['skater']['photo']
                            podium_event.append(podium_url)
                            podium_url = None

                        names.append(Full_name)
                        times.append(time)
                    key2 = "team"
                    if key2 in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['team']['country']
                                        + " "
                                        )
                        time = str(response_result_dict[j]['time']
                                   )
                        names.append(Full_name)
                        times.append(time)
                else:
                    key = 'competitor'
                    if key in response_result_dict[j]:
                        Full_name = str(response_result_dict[j]['competitor']['skater']['firstName']
                                        + " "
                                        + response_result_dict[j]['competitor']['skater']['lastName']
                                        + "   ("
                                        + response_result_dict[j]['competitor']['skater']['country']
                                        + ") "
                                        )
                        time = "geen tijd"
                        names.append(Full_name)
                        times.append(time)
#                    key2 = "team"
#                    if key2 in response_result_dict[j]:
#                        Full_name = str(response_result_dict[j]['team']['country'])
#                        time = "geen tijd"
#                        names.append(Full_name)
#                        times.append(time)
            results[str("startlist_" + events[i])] = names
            result_times[str("startlist_" + events[i])] = times
            podium_pictures[str("startlist_" + events[i])] = podium_event
        names = []
        podium_event = []
        times = []
    return results, podium_pictures, result_times
