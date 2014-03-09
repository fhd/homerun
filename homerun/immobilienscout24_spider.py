import re
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_number_attribute(soup, class_name):
    attribute = soup.findAll(attrs={"class": class_name})[0].string
    return float(attribute.split()[0].replace(",", ""))

def _get_house(url):
    data = {}
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    data["title"] = soup.findAll(id="expose-title")[0].string
    data["rent"] = _get_number_attribute(soup, "is24qa-kaltmiete")
    data["rooms"] = _get_number_attribute(soup, "is24qa-zimmer")
    data["living_area"] = _get_number_attribute(soup, "is24qa-wohnflaeche-ca")
    data["plot_area"] = _get_number_attribute(soup,
                                             "is24qa-grundstuecksflaeche-ca")
    return data

def get_houses(min_rooms, max_rent):
    url_template = "%s/Suche/S-T/Haus-Miete/Nordrhein-Westfalen/Rheinisch-Bergischer-Kreis/Bergisch-Gladbach/%d,00-/-/EURO--%d,00?enteredFrom=one_step_search"
    base_url = "http://www.immobilienscout24.de"
    url = url_template % (base_url, min_rooms, max_rent)
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    items = soup.findAll(id="resultListItems")[0].findAll("li", recursive=False)
    houses = []
    for item in items:
        links = item.findAll("a", href=re.compile(r"^/expose/"))
        if len(links) == 0:
            continue
        target = base_url + links[0]["href"]
        data = _get_house(target)
        data["url"] = target
        houses.append(data)
    return houses
