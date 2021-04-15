from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import math


# degrees to radians
def deg2rad(degrees):
    return math.pi * degrees / 180.0


# radians to degrees
def rad2deg(radians):
    return 180.0 * radians / math.pi


# Semi-axes de la référence géodésique WGS-84
WGS84_a = 6378137.0  # Demi Grand Axe (Equatorial radius) [m]
WGS84_b = 6356752.3  # Demi Petit Axe (Polar radius) [m]


# Rayon de la Terre à une latitude donnée, selon l'ellipsoïde WGS-84. [m]
def WGS84EarthRadius(lat):
    An = WGS84_a * WGS84_a * math.cos(lat)
    Bn = WGS84_b * WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt((An * An + Bn * Bn) / (Ad * Ad + Bd * Bd))


# Boîte englobante entourant le point aux coordonnées données,
# en supposant une approximation locale de la surface terrestre comme une sphère
# de rayon donné par le WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000 * halfSideInKm

    # Rayon de la Terre à une latitude donnée
    radius = WGS84EarthRadius(lat)
    # Rayon du parallèle à une latitude donnée
    pradius = radius * math.cos(lat)

    latMin = lat - halfSide / radius
    latMax = lat + halfSide / radius
    lonMin = lon - halfSide / pradius
    lonMax = lon + halfSide / pradius

    return rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax)


# polygon : liste des points du polygon à tracer
# attention : l'ordre des points du polygon est imporatnt
def point_interieur_polygon(latitude, longitude, poly):
    point = Point(latitude, longitude)
    pol = Polygon(poly)
    return pol.contains(point)

# polygon = [(0, 0), (0, 1), (1, 1), (1, 0)]
# print(point_interieur_polygon(0.5, 0.5, polygon))
