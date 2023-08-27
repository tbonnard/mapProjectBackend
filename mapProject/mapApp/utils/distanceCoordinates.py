import math
from decimal import Decimal

import geopy.distance

def get_distance(lat_1, lng_1, lat_2, lng_2):
    d_lat = Decimal(lat_2) - lat_1
    d_lng = Decimal(lng_2) - lng_1

    coords_1 = (lat_1, lng_1)
    coords_2 = (Decimal(lat_2), Decimal(lng_2))

    distance = geopy.distance.geodesic(coords_1, coords_2).km
    return distance
