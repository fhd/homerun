def _equals(house1, house2):
    unique_keys = ["title", "price", "rent"]
    for unique_key in unique_keys:
        if not unique_key in house1 or not unique_key in house2:
            return False
        if house1[unique_key] != house2[unique_key]:
            return False
    return True

def contains(houses, house):
    for existing_house in houses:
        if _equals(house, existing_house):
            return True
    return False

def filter_duplicates(houses):
    unique_houses = []
    for house in houses:
        if not contains(unique_houses, house):
            unique_houses.append(house)
    return unique_houses
