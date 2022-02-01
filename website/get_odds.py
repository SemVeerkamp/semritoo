import requests
from bs4 import BeautifulSoup
from contextlib import suppress

def get_html(url):
    from requests_html import HTMLSession
    session = HTMLSession()
    r = session.get(url)
    r.html.render(wait = 8, sleep = 8)
    return r.html


url = "https://sport.toto.nl/wedden/sport/3938/schaatsen/outrights"


def get_odds(url):
    content = get_html(url)

    soup = BeautifulSoup(content.html, "html.parser")

    events = soup.find_all('div', class_="event-panel__heading__market-name")
    riders = soup.find_all('span', class_="button--outcome__text-title")
    odds = soup.find_all('span', class_="button--outcome__price")

    odds_dict = {}
    names = []
    with suppress(Exception):
        j = 0
        for event in events:
            keepGoing = True
            while keepGoing:
                if float(odds[j].text.replace(',', '.')) <= float(odds[j+1].text.replace(',', '.')):
                    odd = str(riders[j].text + ":  " + odds[j].text)
                    names.append(odd)
                    j = j + 1
                else:
                    odds_dict[event.text[23:]] = names
                    names = []
                    keepGoing = False
                    j = j + 1
    odds_dict[event.text[23:]] = names
    return odds_dict


