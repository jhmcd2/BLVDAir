import pandas as pd
from api import *
from metrojet import * 
# Get global values
AIRPORTSDF = get_all_airports()

def route_planner():
    routes = make_metrojet_routes(AIRPORTSDF)

if __name__=="__main__":
    route_planner()    
