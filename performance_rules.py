import pandas as pd

# Function to calculate reserve fuel
def calculate_reserve_fuel(fuel_burn, range):
  reserve_hours = 1  # Assuming 1 hour reserve requirement
  reserve_fuel = fuel_burn * reserve_hours
  return reserve_fuel

# Function to calculate required fuel for the trip
def calculate_trip_fuel(distance, fuel_burn, reserve_fuel):
  total_fuel = distance * fuel_burn + reserve_fuel
  return total_fuel

# Function to calculate passenger weight
def calculate_passenger_weight(passenger_count):
  passenger_weight = passenger_count * 195  # Using FAA winter factor
  return passenger_weight

# Function to calculate total payload (passengers + cargo) weight
def calculate_total_payload(passenger_count, cargo_weight):
  passenger_weight = calculate_passenger_weight(passenger_count)
  total_payload = passenger_weight + cargo_weight
  return total_payload

# Get weight factor
def weight_factor(actual_landingweight,MLW):
  #actual landing weight/ max landing weight
  # should work for take off too
  wf = actual_landingweight / MLW
  return wf

#Determine new ac weight
def new_ac_weight(wf,MW):
  new_weight = wf * MW
  return new_weight

# Get adjusted number for runway use
def adjusted_runway_use(wf,max_rwny):
  # weight factor time max distance
  adjusted_runway_length = wf * max_rwny
  return adjusted_runway_length

# Now get how much we need to change weight factor
def reverse_adjusted_runway_use(airport_runway_length,Min_LND_length_MLW):
  wf = airport_runway_length / Min_LND_length_MLW
  return wf

#Function to determine drop weight from the aircraft 
def weight_reduction(diff,Maxpax,Maxcargo,passenger_baggage_weight):
  cargo_only = Maxcargo - passenger_baggage_weight
  new_cargo = cargo_only
  New_Maxpax = Maxpax
  while new_cargo > 0 or diff > 0:
    new_cargo = new_cargo - 1
    diff = diff - 1
  if diff > 0:
    while diff > 0 or New_Maxpax > 0 :
      New_Maxpax = New_Maxpax - 300
      diff = diff - 300
  if New_Maxpax < 0:
    possible = False
  return New_Maxpax, new_cargo, possible



# Function to modify aircraft performance so that it can take off or land at a specific airport
def calculate_performance(aircraft,airport_runway_length,trip_fuel,cominggoing):
    # Constants
    average_passenger_weight = 195
    baggage_weight = 100
    jet_fuel_weight_per_gallon = 7
    MTOW = aircraft['MTOW']
    maxlw = aircraft['MLW']
    Maxpax = aircraft['Passenger Numbers']
    Maxcargo = aircraft['Cargo']
    fuel_burn = aircraft['Fuel Burn per Hour']
    Min_TO_length_MTOW = aircraft['TO Distance MTOW']
    Min_LND_length_MLW = aircraft['Lnd Distance MLW']
    MIN_LAND_DISTANCE = aircraft['min LND Distance']
    MAX_LAND_WEIGHT = aircraft['MLW']
    maxpaxweight = Maxpax * average_passenger_weight
    total_fuel_weight = trip_fuel * jet_fuel_weight_per_gallon
    empty_weight = MTOW - total_fuel_weight - Maxcargo - maxpaxweight
    min_landing_weight_legal = empty_weight + fuel_burn
    difference = min_landing_weight_legal - MAX_LAND_WEIGHT
    reserve_fuel_weight = fuel_burn * jet_fuel_weight_per_gallon
    passenger_baggage_weight = Maxpax * 100

    takeoffweight = Maxpax + Maxcargo + total_fuel_weight
    landing_weight = takeoffweight - total_fuel_weight + reserve_fuel_weight

    if cominggoing == 'TO':
      wf = weight_factor(takeoffweight,MTOW)  
      adjusted_runway_length = adjusted_runway_use(wf,Min_TO_length_MTOW)
    else: 
      wf = weight_factor(landing_weight,MAX_LAND_WEIGHT)  
      adjusted_runway_length = adjusted_runway_use(wf,Min_LND_length_MLW)
    
    if adjusted_runway_length > airport_runway_length:
      if cominggoing == 'LND':
        wf = reverse_adjusted_runway_use(airport_runway_length,Min_LND_length_MLW)
        new_weight = new_ac_weight(wf,MAX_LAND_WEIGHT)
        diff = landing_weight - new_weight 
        new_pax, new_cargo, possible = weight_reduction(diff,Maxpax,Maxcargo)
      else:   
        wf = reverse_adjusted_runway_use(airport_runway_length,Min_TO_length_MTOW)
        new_weight = new_ac_weight(wf,MTOW)
        diff = takeoffweight - new_weight 
        new_pax, new_cargo, possible = weight_reduction(diff,Maxpax,Maxcargo,passenger_baggage_weight)
    if possible == True:    
      return True, new_pax, new_cargo
    else:
      return False, 0, 0
    
# Calculate Range performance
def calculate_range_performance(aircraft, distance,usable_range):
  MTOW = aircraft['MTOW']
  max_range = aircraft['Range']
  paxweight = aircraft['Passenger Numbers'] * 300
  cargoweight = aircraft['Cargo']
  Max_pax_weight = aircraft['Passenger Numbers'] * 190
  passenger_baggage_weight = aircraft['Passenger Numbers'] * 100
  jet_fuel_weight_per_gallon = 7
  fuel_avail = calculate_reserve_fuel(aircraft["Fuel Burn"], aircraft["Range"])
  fuel_weight = fuel_avail * jet_fuel_weight_per_gallon
  toweight = fuel_weight + paxweight + cargoweight
  wf = weight_factor(MTOW,toweight)
  adjusted_range = adjusted_runway_use(wf,max_range)
  if adjusted_range < distance:
    wf = reverse_adjusted_runway_use(adjusted_range,distance)
    new_weight = new_ac_weight(wf,MTOW)
    diff = MTOW - new_weight
    new_pax, new_cargo, possible = weight_reduction(diff,Max_pax_weight,cargoweight,passenger_baggage_weight)
    if possible == True:
      return True, new_pax, new_cargo 
    else:
      return False, 0, 0


# Function to evaluate aircraft suitability
def evaluate_aircraft(aircraft, distance, departing_runway_length, landing_runway_length):
  # Calculate usable range after reserve fuel
  usable_range = aircraft["Range"] - calculate_reserve_fuel(aircraft["Fuel Burn"], aircraft["Range"])
  old_pax = aircraft['Passenger Numbers']
  old_cargo = aircraft['Cargo']

  # Check if aircraft range is sufficient for the trip
  if usable_range < distance:
    achievable,new_pax, new_cargo = calculate_range_performance(aircraft, distance,usable_range)
    if achievable != True:
      return None  # Skip if range is insufficient
    else:
      reserve_fuel = calculate_reserve_fuel(aircraft["fuel_burn"], usable_range)
      trip_fuel = calculate_trip_fuel(distance, aircraft["fuel_burn"], reserve_fuel)
      aircraft['Passenger Numbers'] = new_pax
      aircraft['Cargo'] = new_cargo

  # Check runway length for takeoff
  if departing_runway_length < aircraft["Takeoff Distance (MTOW)"]:
    achievable, new_pax, new_cargo = calculate_performance(aircraft,departing_runway_length,trip_fuel,'TO')
    if achievable == False:
      return None # Skip if runway is too short for take off
    else:
      aircraft['Passenger Numbers'] = new_pax
      aircraft['Cargo'] = new_cargo
    
  # Minimum landing distance might be the limiting factor
  if runway_length < aircraft["Minimum Landing Distance"]:
    achievable, new_pax, new_cargo = calculate_performance(aircraft,departing_runway_length,trip_fuel,'LND')
    if achievable == False:
      return None  # Skip if runway is too short for landing
    else:
      aircraft['Passenger Numbers'] = new_pax
      aircraft['Cargo'] = new_cargo

  # Calculate performance score (higher is better)
  performance_score = (1-(aircraft["Passenger Numbers"]/old_pax) * ((usable_range / trip_fuel)/100)*(aircraft['Cargo']/old_cargo))*100
  return {"Model": aircraft["Model"], "Performance Score": performance_score}

# Load aircraft data from a DataFrame
aircraft_data = pd.read_csv("aircraft_data.csv")  # Replace with your data source

# Get distance from another method (replace with your distance calculation)
distance = get_distance()  # Replace with your distance function call

# Get runway length for the destination airport
runway_length = get_runway_length()  # Replace with your runway length retrieval

# Evaluate each aircraft
ranked_aircraft = []
for index, row in aircraft_data.iterrows():
  aircraft_evaluation = evaluate_aircraft(row.to_dict(), distance, runway_length)
  if aircraft_evaluation:
    ranked_aircraft.append(aircraft_evaluation)

# Sort ranked aircraft by performance score (descending)
ranked_aircraft.sort(key=lambda x: x["Performance Score"], reverse=True)

# Return top two ranked aircraft
top_two_aircraft = ranked_aircraft[:2]

print(f"Top Ranked Aircraft:")
for aircraft in top_two_aircraft:
  print(f"\tModel: {aircraft['Model']}")
  print(f"\tPerformance Score: {aircraft['Performance Score']:.2f}")
