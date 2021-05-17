from math import pi, sin, cos, asin, sqrt, radians

earthRadiusKm = 6371


def deg2rad(deg):
    return (deg * pi / 180)

def rad2deg(rad):
    return (rad * 180 / pi)

def haversine(lat1d, lon1d, lat2d, lon2d):
    """
    Returns the distance between two points on the Earth.
    Direct translation from http://en.wikipedia.org/wiki/Haversine_formula
    Code from
    https://stackoverflow.com/questions/10198985/calculating-the-distance-between-2-latitudes-and-longitudes-that-are-saved-in-a

    :param lat1d: Latitude of the first point in degrees
    :param lon1d: Longitude of the first point in degrees
    :param lat2d: Latitude of the second point in degrees
    :param lon2d: Longitude of the second point in degrees
    :return: The distance between the two points in kilometers
    """

    lat1r = deg2rad(lat1d)
    lon1r = deg2rad(lon1d)
    lat2r = deg2rad(lat2d)
    lon2r = deg2rad(lon2d)
    u = sin((lat2r - lat1r) / 2)
    v = sin((lon2r - lon1r) / 2)
    return 2 * earthRadiusKm * asin(sqrt(u * u + cos(lat1r) * cos(lat2r) * v * v))

def haversine2(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = earthRadiusKm * c
    return km

def minkowski(x1, y1, x2, y2, p=2**.5):
    """ Compute the minkowski distance between two geographic points """
    return (abs(x2 - x1) ** p + abs(y2 - y1) ** p) ** (1/p)

def euclidean(x1, y1, x2, y2):
    """ Compute the euclidean distance between two geographic points """
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5

def manhattan(x1, y1, x2, y2):
    """ Compute the manhattan distance between two geographic points """
    return abs(x2 - x1) + abs(y2 - y1)

def octile(x1, y1, x2, y2):
    """ Compute the octile distance between two geographic points """
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    return max(dx, dy) + (2**.5 - 1) * min(dx, dy)

def bearing(lat1, lon1, lat2, lon2, positive):
    """Given latitudes and longitudes coordinates of 2 points,
    returns absolute bearing from first to second."""
    import math
    d_lon = lon2 - lon1
    y_val = math.sin(d_lon) * math.cos(lat2)
    x_val = (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) *
             math.cos(lat2) * math.cos(d_lon))
    bearing = math.degrees(math.atan2(y_val, x_val))
    if positive and bearing < 0:
        bearing = 360 + bearing
    return bearing

def bearing_angle(brng1, brng2):
    """Returns the smallest angle between two bearings."""
    if (brng1 >= 0 and brng2 >= 0 or brng1 <= 0 and brng2 <= 0):
        return abs(brng1 - brng2)
    else:
        if brng1 < 0:
            result = abs(180 + brng1) + (180 - brng2)
        elif brng1 > 0:
            result = abs(180 + brng2) + (180 - brng1)
        if result > 180:
            result = abs(result - 360)
        return result

def path_len(coords_list):
    """Given a list of (lat,lon) tuples, returns the length in km"""
    if not len(coords_list):
        return 0
    length = 0
    prev_lat, prev_lng = coords_list[0]
    for lat,lng in coords_list:
        length += haversine(prev_lat, prev_lng, lat, lng)
        prev_lat, prev_lng = lat, lng
    return length

if __name__== "__main__":
    point1 = 50.846, 4.3496
    point2 = 50.860, 4.37
    print(haversine(point1[0], point1[1], point2[0], point2[1]))
    print(haversine2(point1[0], point1[1], point2[0], point2[1]))
