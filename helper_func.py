from math import sin, cos, acos, radians

def haversine(lat1, lon1, lat2, lon2):
  """
  Calculates the distance between two points on Earth using the Haversine formula.

  Args:
      lat1 (float): Latitude of the first point in degrees.
      lon1 (float): Longitude of the first point in degrees.
      lat2 (float): Latitude of the second point in degrees.
      lon2 (float): Longitude of the second point in degrees.

  Returns:
      float: Distance between the two points in kilometers.
  """
  # Convert degrees to radians
  lat1 = radians(lat1)
  lon1 = radians(lon1)
  lat2 = radians(lat2)
  lon2 = radians(lon2)

  # Calculate the distance using the Haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
  c = 2 * acos(min(1, a))
  r = 6371  # Earth's radius in kilometers

  return c * r

#distance = haversine(latitude_airport1, longitude_airport1, latitude_airport2, longitude_airport2)

print(f"Distance between the two points: {distance:.2f} kilometers")

def convert_km_to_miles(distance_km):
  conversion_factor = 0.54
  distance_naughtical_miles = distance_km * conversion_factor
  return distance_naughtical_miles
