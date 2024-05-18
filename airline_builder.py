import pandas as pd
from api import *
from metrojet import * 
# Get global values
AIRPORTSDF = get_all_airports()

#Main function to run all code
def route_planner():

    #Get legacy Metrojet routes
    metrojet_hub, metrojet_airports = Metrojet_airports()
    # Pull all other airports
    hubdf = AIRPORTSDF[AIRPORTSDF['Airport Type']== 'HUB']
    hub_list = hubdf['ICAO Code'].tolist()
    destdf = AIRPORTSDF[AIRPORTSDF['Airport Type']!= 'HUB']
    dest_list = destdf['ICAO Code'].tolist()
    # Create a dataframe and fill with potential routes
    columns = ['Origin','Destination','Distance']
    potential_route_df = pd.DataFrame(columns)
    potential_route_df = return_a_route(metrojet_hub,metrojet_airports,potential_route_df,AIRPORTSDF)
    potential_route_df = return_a_route(hub_list,dest_list,potential_route_df,AIRPORTSDF)


if __name__=="__main__":
    route_planner()    
