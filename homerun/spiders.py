import immobilienscout24_spider
import kalaydo_spider
import house_utils

def get_houses():
    houses = []
    houses.extend(immobilienscout24_spider.get_houses())
    houses.extend(kalaydo_spider.get_houses())
    houses = house_utils.filter_duplicates(houses)
    return houses
