from math import pi, sin, cos, asin, sqrt 

earthRadiusKm = 6371

def deg2rad(deg):
    return (deg * pi / 180)

def rad2deg(rad):
    return (rad * 180 / pi)

def distanceEarth(lat1d, lon1d, lat2d, lon2d):
    """
    Returns the distance between two points on the Earth.
    Direct translation from http://en.wikipedia.org/wiki/Haversine_formula
    Code from https://stackoverflow.com/questions/10198985/calculating-the-distance-between-2-latitudes-and-longitudes-that-are-saved-in-a

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


