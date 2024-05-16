from api import *



AIRPORTSDF = get_all_airports()
def kill_the_routes():
    hubsDF = AIRPORTSDF[AIRPORTSDF['Airport Type']== "HUB"]
    hub_list = hubsDF['ICAO Code'].tolist()
    ap_list = AIRPORTSDF['ICAO Code'].tolist()
    i = 0
    for hub in hub_list:
        for airport in ap_list:
            if i == 0:
                if hub != airport:
                    print('HUB: ' + hub)
                    print('DEST: ' + airport)
                    routesdf = get_route(hub,airport)
                    enteries = len(routesdf)
                    if enteries > 1:
                        count = 0 
                        while count < enteries:
                            if count != 0:
                                id = routesdf['_id'].iloc[count]
                                removed = delete_route(id)
                                print('Redundant ' + hub + ' and ' + airport + ' routes removed ' + str(removed))
                            count = count + 1

def who_doesnt_have_lat_long():
    no = []
    for index, row in AIRPORTSDF.iterrows():
        name = row['ICAO Code']
        lat = row['Lat']
        long = row['Long']
        if lat == '' or long == '':
            no.append(name)
    with open('nolatlong.txt', 'w') as fp:
        for item in no:
            # Write each item on a new line
            fp.write(f"{item}\n")
    print(len(no))
    print(no)  

if __name__=="__main__":      
    who_doesnt_have_lat_long()