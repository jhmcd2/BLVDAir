def make_route_skema(origin,destination,frequency,performance,flight_type,sched,distance):
    route_skema = {
        'Origin': origin,
        'Destination': destination,
        'Frequency' : frequency,
        'Performance' : performance,
        'Flight Type' : flight_type,
        'Scheduled?' : sched,
        'Distance' : distance,
    }
    return route_skema

def make_aircraft_performance_skema(aircraft,pax,cargo,fuel,ac_type):
    aircraft_performance_skema = {
        'Aircraft' :  aircraft,
        'Max Passengers' : pax,
        'Max Cargo' : cargo,
        'Total Fuel Requirement' : fuel,
        'Aircraft Type' :  ac_type,
    }
    return aircraft_performance_skema