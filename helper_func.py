from math import sin, cos, acos, radians

KBWI_int_list = ['RJTT','LFPG', 'VHHH', 'EGSS', 'RKSI','RJBB']

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

# Distance Processor
def distance_processor(ap1,ap2,AIRPORTSDF):
  hubdf = AIRPORTSDF[AIRPORTSDF['ICAO Code']== ap1]
  hublat = hubdf['Lat'].iloc[0]
  hublong = hubdf['Long'].iloc[0]
  airportdf = AIRPORTSDF[AIRPORTSDF['ICAO Code']== ap2]
  airlat = airportdf['Lat'].iloc[0]
  airlong = airportdf['Long'].iloc[0]
  unusable_distance = haversine(hublat, hublong, airlat, airlong)
  distance = convert_km_to_miles(unusable_distance)
  return distance

# Method to evaluate if Hub can fly here
def evaluate_hub(ap1,ap2,AIRPORTSDF,distance):
  good = None
  ap1df = AIRPORTSDF[AIRPORTSDF['ICAO Code']== ap1]
  ap2df = AIRPORTSDF[AIRPORTSDF['ICAO Code']== ap2]
  if ap1df["Country"] == ap2df["Country"]:
    #Are they in the same country
    if ap1df["Domestic Region"] == ap2df["Domestic Region"]:
      #Are they in the same domestic region
      good = True
    else:
      #They are not in the same domestic region
      advpax = (ap1df["Pax"] + ap2df["Pax"])/2
      pax_per_day = advpax/365
      if distance < 1500:
        if pax_per_day > 10000:
          good = True
        else:
          good = False
      elif 1501 < distance < 2500:
        if pax_per_day > 15000:
          good = True
        else:
          good = False
      elif distance > 3000:
        if pax_per_day > 20000:
          good = True
        else:
          good= False
  else:
    #They are not in the same country
    if ap1df["Airport Type"] == 'HUB' and ap2df["Airport Type"] == 'HUB':
      #are they both hubs
      good = True
    else:
      #One is not a hub
      advpax = (ap1df["Pax"] + ap2df["Pax"])/2
      pax_per_day = advpax/365
      if ap1 == 'KBWI' or ap2 == 'KBWI':
        if (ap1 in KBWI_int_list) or (ap2 in KBWI_int_list):
          good = True
        elif (ap1 in ap1df["Special_routes"]) or (ap2 in ap1df["Special_routes"]):
          good = True
      else:
        good = False
      if distance < 9000:
        
      elif (ap1 in ap1df["Special_routes"]) or (ap2 in ap1df["Special_routes"]):
        good = True


  
  
# Method to evaluate if dest can fly here
def evaluate_dest(origin, destination):
  pass
# Method parses all hubs and destination and builds out the hub and point to point system
def return_a_route(hub,dest,route_df,AIRPORTSDF):
  for h in hub:
    for destination in dest:
      distance = distance_processor(h,destination,AIRPORTSDF)
      good = evaluate_hub(h,destination,AIRPORTSDF,distance)
      if good == True:
        route_df.loc[len(route_df.index)] = [h,destination,distance]
        route_df.loc[len(route_df.index)] = [destination,h,distance]
  for origin in dest:
    for destination in dest:
      distance = distance_processor(origin,destination,AIRPORTSDF)
      good = evaluate_dest(origin, destination,AIRPORTSDF,distance)
      if good == True:
        route_df.loc[len(route_df.index)] = [origin,destination,distance]
        route_df.loc[len(route_df.index)] = [destination,origin,distance]
  return route_df


