import immobilienscout24_spider
import kalaydo_spider
import house_utils

def get_houses(min_rooms, max_price):
    houses = []
    houses.extend(immobilienscout24_spider.get_houses(min_rooms, max_price))
    houses.extend(kalaydo_spider.get_houses(min_rooms, max_price))
    houses = house_utils.filter_duplicates(houses)
    return houses
