import re
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_address(soup):
    address_pattern = re.compile(r"is24-expose-address")
    address_field = soup.find(attrs={"data-qa": address_pattern})
    address_value = address_field.find("strong").string
    return re.sub("\s+", " ", address_value.strip())

def _get_number_attribute(soup, class_name):
    attribute = soup.find(attrs={"class": class_name})
    if not attribute:
        return 0
    return float(attribute.string.split()[0].replace(",", ""))

def _get_house(url):
    data = {}
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    data["title"] = soup.find(id="expose-title").string
    data["address"] = _get_address(soup)
    data["price"] = _get_number_attribute(soup, "is24qa-kaufpreis")
    data["rent"] = _get_number_attribute(soup, "is24qa-kaltmiete")
    data["rooms"] = _get_number_attribute(soup, "is24qa-zimmer")
    data["living_area"] = _get_number_attribute(soup, "is24qa-wohnflaeche-ca")
    data["plot_area"] = _get_number_attribute(soup,
                                              "is24qa-grundstuecksflaeche-ca")
    return data

def _get_houses(search_url):
    base_url = "http://www.immobilienscout24.de"
    url = base_url + search_url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    items = soup.find(id="resultListItems").findAll("li", recursive=False)
    houses = []
    for item in items:
        links = item.findAll("a", href=re.compile(r"^/expose/"))
        if len(links) == 0:
            continue
        target = base_url + links[0]["href"]
        data = _get_house(target)
        data["url"] = target
        houses.append(data)
    next_link = soup.find("a", attrs={"data-is24-qa": "paging_bottom_next"})
    if next_link:
        houses.extend(_get_houses(next_link["href"]))
    return houses

def get_houses(search_url):
    return _get_houses(search_url)
