import immobilienscout24_spider
import kalaydo_spider
import house_utils

def get_houses(min_rooms, max_rent):
    houses = []
    houses.extend(immobilienscout24_spider.get_houses(min_rooms, max_rent))
    houses.extend(kalaydo_spider.get_houses(min_rooms, max_rent))
    houses = house_utils.filter_duplicates(houses)
    return houses
