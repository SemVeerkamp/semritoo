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
        quarter = "Quarter"
        semi = "Semi"
        if quarter not in events[i]:
            if semi not in events[i]:
                response_result = requests.get('https://api.isuresults.eu/events/'
                                               + event_code
                                               + '/competitions/'
                                               + scheduleNumbers[i]
                                               + '/results/'
                                               )
                response_result_dict = json.loads(response_result.text)
                for j in range(len(response_result_dict)):
                    if response_result_dict[j]:
                        key = 'competitor'
#                        if response_result_dict[j]['time'] is not None:
                        if key in response_result_dict[j]:
                                if response_result_dict[j]['time'] is not None:

                                    Full_name = str(response_result_dict[j]['competitor']['skater']['lastName']
                                                    + " "
                                                    + response_result_dict[j]['competitor']['skater']['firstName']
    #                                                + "   ("
    #                                                + response_result_dict[j]['competitor']['skater']['country']
    #                                                + ")"
                                                    )
                                    if Full_name == "Lee Seung-Hoon":
                                        Full_name = "LEE Seung Hoon"
                                    if Full_name == "Chung Jaewon":
                                        Full_name = "CHUNG Jae Won"
                                    time = str(response_result_dict[j]['time']
                                               )
                                    if j < 3:
                                        podium_url = response_result_dict[j]['competitor']['skater']['photo']
                                        podium_event.append(podium_url)
                                        podium_url = None

                                    names.append(Full_name)
                                    times.append(time)
                                else:
                                    key = 'competitor'
                                    if key in response_result_dict[j]:
                                        Full_name = str(response_result_dict[j]['competitor']['skater']['lastName']
                                                        + " "
                                                        + response_result_dict[j]['competitor']['skater']['firstName']
#                                                       + "   ("
#                                                       + response_result_dict[j]['competitor']['skater']['country']
#                                                       + ") "
                                                        )
                                        if Full_name == "Lee Seung-Hoon":
                                            Full_name = "LEE Seung Hoon"
                                        if Full_name == "Chung Jaewon":
                                            Full_name = "CHUNG Jae Won"
                                        time = "geen tijd"
                                        names.append(Full_name)
                                        times.append(time)
                                if i == 20:
                                    results['men-s-mass-start.htm'] = names
                                    result_times['men-s-mass-start.htm'] = times
                                    podium_pictures['men-s-mass-start.htm'] = podium_event
                                elif i == 21:
                                    results['women-s-mass-start.htm'] = names
                                    result_times['women-s-mass-start.htm'] = times
                                    podium_pictures['women-s-mass-start.htm'] = podium_event
                                else:
                                    init_event = events[i].partition('0m')
                                    results[str(init_event[2]+'-s-'+init_event[0]+init_event[1]+'.htm').lower()] = names
                                    result_times[str(init_event[2]+'-s-'+init_event[0]+init_event[1]+'.htm').lower()] = times
                                    podium_pictures[str(init_event[2]+'-s-'+init_event[0]+init_event[1]+'.htm').lower()] = podium_event
        names = []
        podium_event = []
        times = []
    return results, podium_pictures, result_times
