from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the simulated vehicle (SITL)
print("Connecting to vehicle on 127.0.0.1:14550...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# Function to arm and takeoff
def arm_and_takeoff(target_altitude):
    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Wait for arming
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print(f"Taking off to {target_altitude} meters...")
    vehicle.simple_takeoff(target_altitude)

    # Wait until the vehicle reaches a safe height
    while True:
        print(f"Current altitude: {vehicle.location.global_relative_frame.alt:.2f}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached.")
            break
        time.sleep(1)

# Start the mission
arm_and_takeoff(3)

print("Hovering for 5 seconds...")
time.sleep(5)

print("Initiating landing...")
vehicle.mode = VehicleMode("LAND")

# Wait for landing
while vehicle.armed:
    print(f"Altitude during landing: {vehicle.location.global_relative_frame.alt:.2f}")
    time.sleep(1)

print("Landed and disarmed.")
vehicle.close()