import requests
from bs4 import BeautifulSoup
import datetime
url = "https://olympics.com/en/beijing-2022/sports/speed-skating/"


def get_event_list(url):
    event_list = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    events = soup.find_all("a", class_="b2p-nav__link subtitle")
    for i in range(len(events)):
        event = events[i]['href'][88:]
        event_list.append(event)
    return event_list


def get_result(url):
    url_start = 'https://olympics.com/beijing-2022/olympic-games/en/results/speed-skating/results-'
    url_end = '-fnl-000100.htm'
    results={}
    names = []
    event_list = get_event_list(url)
    for event in event_list:
        event = event.replace('.htm', '')
        page = requests.get(url_start + event + url_end)
        soup = BeautifulSoup(page.content, "html.parser")
        time = soup.find_all("span", class_="text-nowrap")
        results.append(time.text)
        names = []
    return results


def get_startlists(url):
    url_start = 'https://olympics.com/beijing-2022/olympic-games/en/results/speed-skating/entries-by-event-'
    startlist = {}
    names = []
    event_list = get_event_list(url)
    for event in event_list:
        page = requests.get(url_start + event)
        soup = BeautifulSoup(page.content, "html.parser")
        riders = soup.find_all("span", class_="d-none d-md-inline")
        for i in range(len(riders)):
            names.append(riders[i].text)
        startlist[event] = names
        names = []
    return startlist

def get_starttimes():
    a = datetime.datetime(2022, 2, 13, 14, 56)
    b = datetime.datetime(2022, 2, 17, 9, 30)
    c = datetime.datetime(2022, 2, 7, 9, 30)
    d = datetime.datetime(2022, 2, 5, 9, 30)
    e = datetime.datetime(2022, 2, 10, 9, 30)
    f = datetime.datetime(2022, 2, 19, 8, 45)
    g = datetime.datetime(2022, 2, 12, 9)
    h = datetime.datetime(2022, 2, 12, 9, 53)
    i = datetime.datetime(2022, 2, 18, 9, 30)
    j = datetime.datetime(2022, 2, 8, 11, 30)
    k = datetime.datetime(2022, 2, 6, 9, 30)
    l = datetime.datetime(2022, 2, 11, 9)
    m = datetime.datetime(2022, 2, 19, 8)
    n = datetime.datetime(2022, 2, 13, 14)
    starttimes = (a,b,c,d,e,f,g,h,i,j,k,l,m,n)
    return starttimes





# url3 = 'https://olympics.com/beijing-2022/olympic-games/en/results/luge/results-men-s-singles-trno-b00300-.htm'

