import re
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_address(soup):
    postal_code_field = soup.find(attrs={"itemprop": "postalCode"})
    postal_code = postal_code_field and postal_code_field.string.strip() or ""
    city = soup.find(attrs={"itemprop": "addressLocality"}).string.strip()
    address = postal_code and postal_code + " " + city or city
    address = re.sub(",$", "", address)
    return address

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
    soup = BeautifulSoup(content)
    data["title"] = soup.find("h1").string
    data["address"] = _get_address(soup)
    data["price"] = _get_number_attribute(content, "Kaufpreis")
    data["rooms"] = _get_number_attribute(content, "Zimmer")
    data["living_area"] = _get_number_attribute(content, r"Wohnfl.che")
    data["plot_area"] = _get_number_attribute(content, r"Grundst.ck")
    return data

def _get_houses(search_url):
    base_url = "http://www.kalaydo.de"
    url = base_url + search_url
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read())
    except urllib2.HTTPError as e:
        if e.code == 509:
            print "Ignoring HTTP 509 for: " + url
            return []
    items = soup.find(id="resultlist").findAll("li", recursive=False)
    houses = []
    for item in items:
        link = item.find("a", href=re.compile(r"^/immobilien/"))
        target = base_url + link["href"]
        try:
            data = _get_house(target)
        except urllib2.HTTPError as e:
            print "Ignoring HTTP 509 for: " + target
            continue
        data["url"] = target
        houses.append(data)
    next_link = soup.find("a", attrs={"class": "next"})
    if next_link:
        houses.extend(_get_houses(next_link["href"]))
    return houses

def get_houses(search_url):
    return _get_houses(search_url)
