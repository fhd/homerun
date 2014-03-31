import house_utils
import importlib
import json
import os
import sys

def _get_houses(spider_name, search_url):
    spider = importlib.import_module("homerun.spiders." + spider_name)
    return spider.get_houses(search_url)

def get_houses():
    spiders_file = "spiders.json"
    if not os.path.isfile(spiders_file):
        print >>sys.stderr, "%s missing, please create it." % spiders_file
        return []
    spiders = json.loads(open(spiders_file).read())
    houses = []
    for name in spiders.keys():
        houses.extend(_get_houses(name, spiders[name]))
    houses = house_utils.filter_duplicates(houses)
    return houses
