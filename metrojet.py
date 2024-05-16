#create metrojet 
from api import *
from helper_func import *

airports = ['KALB','KATL','KBWI','KBHM','KBOS','KBUF','KMDW','KCLE','KCMH','KFLL','KRSW','KBDL','KJAX','KMHT','KMIA','KMKE','KMSY','KLGA','KMCO','KPVD','KRDU','KSTL','KSYR','KTPA','KTUS','KIAD','KPBI' ]
hub = ['KBWI']

print(airports)


def make_metrojet_routes(AIRPORTSDF):
    hub = hub[0]
    for airport in airports:
        if airport != hub:
            routedf = get_routes_from_new_table(hub, airport)
            how_many_routes = len(routedf)
            airportdf = AIRPORTSDF[AIRPORTSDF['ICAO Code']== airport]
            airlat = airportdf['Lat'].iloc[0]
            airlong = airportdf['Long'].iloc[0]
            if how_many_routes != 0:
                hubdf = AIRPORTSDF[AIRPORTSDF['ICAO Code']== hub]
                hublat = hubdf['Lat'].iloc[0]
                hublong = hubdf['Long'].iloc[0]
                unusable_distance = haversine(hublat, hublong, airlat, airlong)
                distance = convert_km_to_miles(unusable_distance)
                
        