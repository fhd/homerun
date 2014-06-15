import re
import sys
import time
import urllib2
from BeautifulSoup import BeautifulSoup

def _get_house_urls(search_url):
    base_url = "http://www.kalaydo.de"
    url = base_url + search_url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    items = soup.find(id="resultlist").findAll("li", recursive=False)
    urls = []
    for item in items:
        link = item.find("a", href=re.compile(r"^/immobilien/"))
        target = base_url + link["href"]
        urls.append(target)
    next_link = soup.find("a", attrs={"class": "next"})
    if next_link:
        urls.extend(_get_house_urls(next_link["href"]))
    return urls

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
    data["rent"] = _get_number_attribute(content, "Kaltmiete")
    data["rooms"] = _get_number_attribute(content, "Zimmer")
    data["living_area"] = _get_number_attribute(content, r"Wohnfl.che")
    data["plot_area"] = _get_number_attribute(content, r"Grundst.ck")
    return data

def _get_houses(urls):
    houses = []
    for index, url in enumerate(urls):
        if index > 0 and index % 50 == 0:
            time.sleep(300)
        try:
            house = _get_house(url)
        except urllib2.HTTPError as e:
            message = "Failed to fetch %s, HTTP error %d." % (url, e.code)
            print >>sys.stderr, message
            house = {}
        house["url"] = url
        houses.append(house)
    return houses

def get_houses(search_url):
    urls = _get_house_urls(search_url)
    return _get_houses(urls)
