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

# Function to evaluate aircraft suitability
def evaluate_aircraft(aircraft, distance, runway_length):
  # Calculate usable range after reserve fuel
  usable_range = aircraft["Range"] - calculate_reserve_fuel(aircraft["Fuel Burn"], aircraft["Range"])
  
  # Check if aircraft range is sufficient for the trip
  if usable_range < distance:
    return None  # Skip if range is insufficient

  # Check runway length for takeoff and landing
  if runway_length < aircraft["Takeoff Distance (MTOW)"]:
    # Minimum landing distance might be the limiting factor
    if runway_length >= aircraft["Minimum Landing Distance"]:
      # Calculate required fuel for the trip
      trip_fuel = calculate_trip_fuel(distance, aircraft["Fuel Burn"], calculate_reserve_fuel(aircraft["Fuel Burn"], aircraft["Range"]))

      # Calculate remaining payload capacity after fuel
      payload_capacity = aircraft["MTOW"] - trip_fuel - aircraft["Minimum Landing Weight"]

      # Remove cargo first, then passengers (with their baggage)
      cargo_reduction = min(aircraft["Cargo"], payload_capacity - calculate_total_payload(aircraft["Passenger Count"], 0))
      remaining_cargo = aircraft["Cargo"] - cargo_reduction

      # If cargo reduction isn't enough, remove passengers
      passenger_reduction = 0
      if payload_capacity - calculate_total_payload(aircraft["Passenger Count"] - 1, remaining_cargo) < 0:
        passengers_to_remove = int((payload_capacity - calculate_total_payload(0, remaining_cargo)) / (calculate_passenger_weight(1) + 2 * 50))  # Account for baggage
        passenger_reduction = min(aircraft["Passenger Count"], passengers_to_remove)
        remaining_passengers = aircraft["Passenger Count"] - passenger_reduction

      # Update payload information if restrictions are needed
      if cargo_reduction > 0 or passenger_reduction > 0:
        return {
          "Model": aircraft["Model"],
          "Performance Score": None,  # Performance score not calculated due to restrictions
          "Cargo Restriction": cargo_reduction,
          "Passenger Restriction": passenger_reduction,
          "Remaining Cargo": remaining_cargo,
          "Remaining Passengers": remaining_passengers
        }
    else:
      return None  # Skip if runway is too short for landing


  # Calculate remaining payload capacity after fuel
  payload_capacity = aircraft["MTOW"] - trip_fuel - aircraft["Minimum Landing Weight"]

  # Check if payload capacity is enough for passengers and cargo
  total_payload = calculate_total_payload(aircraft["Passenger Count"], aircraft["Cargo"])
  if payload_capacity < total_payload:
    return None  # Skip if payload is too heavy

  # Calculate performance score (higher is better)
  performance_score = aircraft["Passenger Count"] * (usable_range / trip_fuel)
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
