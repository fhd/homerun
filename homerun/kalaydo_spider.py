# coding=utf-8

import re
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_number_attribute(content, label_text):
    # No BeautifulSoup parser can handle the kalaydo.de detail pages properly,
    # resorting to regex.
    pattern = label_text + r".*?<div.*?>(.*?)<"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return 0
    value = match.groups()[0].strip()
    match = re.search(r"([\d,\.]+)", value)
    if not match:
        return 0
    number_string = match.group(0).replace(".", "").replace(",", ".")
    try:
        return float(number_string)
    except:
        return 0

def _get_house(url):
    data = {}
    content = urllib2.urlopen(url).read()
    data["title"] = BeautifulSoup(content).find("h1").string
    data["price"] = _get_number_attribute(content, "Kaufpreis")
    data["rooms"] = _get_number_attribute(content, "Zimmer")
    data["living_area"] = _get_number_attribute(content, r"Wohnfl.che")
    data["plot_area"] = _get_number_attribute(content, r"Grundst.ck")
    return data

def _get_houses(search_url):
    base_url = "http://www.kalaydo.de"
    url = base_url + search_url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    items = soup.findAll(id="resultlist")[0].findAll("li", recursive=False)
    houses = []
    for item in items:
        link = item.findAll("a", href=re.compile(r"^/immobilien/"))[0]
        target = base_url + link["href"]
        data = _get_house(target)
        data["url"] = target
        houses.append(data)
    next_link = soup.find("a", attrs={"class": "next"})
    if next_link:
        houses.extend(_get_houses(next_link["href"]))
    return houses

def get_houses():
    search_url = "/immobilien/haus-kaufen/o/rheinisch-bergischer-kreis/bergisch-gladbach"
    return _get_houses(search_url)
