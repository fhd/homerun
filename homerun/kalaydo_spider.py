# coding=utf-8

import re
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_number_attribute(soup, label_text):
    labels = soup.findAll(text=re.compile(r"^" + label_text))
    if len(labels) == 0:
        return 0
    label = labels[0]
    value = label.parent.findNextSibling("div")
    number_strings = re.findall(r"[\d,]+", value.string)
    return float(number_strings[0].replace(",", "."))

def _get_house(url):
    data = {}
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    data["title"] = soup.findAll("h1")[0].string
    data["price"] = _get_number_attribute(soup, "Kaufpreis")
    data["rooms"] = _get_number_attribute(soup, "Zimmer")
    data["living_area"] = _get_number_attribute(soup, r"Wohnfl.che")
    data["plot_area"] = _get_number_attribute(soup, r"Gesamtfl.che")
    return data

def get_houses(min_rooms, max_price):
    url_template = "%s/immobilien/haus-kaufen/o/rheinisch-bergischer-kreis/bergisch-gladbach/?ROOMS_FROM=%d&PRICE_TO=%d"
    base_url = "http://www.kalaydo.de"
    url = url_template % (base_url, min_rooms, max_price)
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    items = soup.findAll(id="resultlist")[0].findAll("li", recursive=False)
    houses = []
    for item in items:
        link = item.findAll("a", href=re.compile(r"^/immobilien/"))[0]
        target = base_url + link["href"]
        data = _get_house(target)
        data["url"] = target
        houses.append(data)
    return houses
