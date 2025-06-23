from dronekit import connect, VehicleMode
import time
import random

# ------------------ Constants ------------------ #
TARGET_ALTITUDE = 3.0  # Meters
SIDESTEP_DISTANCE = 0.5  # Meters (right sidestep)
GOAL_DETECTED_FAKE = False  # Emulated in Phase 1
DRIFT_FAKE = False  # Toggle this to simulate drift

# ------------------ Connect to Vehicle ------------------ #
print("Connecting to vehicle on 127.0.0.1:14550...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# ------------------ FSM States ------------------ #
class State:
    START = "START"
    SCAN = "FORWARD_SCAN"
    SIDESTEP = "SIDESTEP_RIGHT"
    GOAL_FOUND = "GOAL_FOUND"
    LAND = "LAND"
    DRIFT_HOLD = "DRIFT_HOLD"

current_state = State.START

# ------------------ FSM Behaviors ------------------ #
def arm_and_takeoff(altitude):
    print("Arming and taking off...")
    while not vehicle.is_armable:
        print("Waiting for vehicle to become armable...")
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    vehicle.simple_takeoff(altitude)
    while True:
        print(f" Current altitude: {vehicle.location.global_relative_frame.alt:.2f} m")
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print("Target altitude reached.")
            break
        time.sleep(1)

def forward_scan():
    print("[SCAN] Simulating forward motion...")
    time.sleep(2)
    return True  # Always detect obstacle for demo

def sidestep_right():
    print("[SIDESTEP] Simulating sidestep right...")
    time.sleep(1)

def check_for_goal():
    return GOAL_DETECTED_FAKE

def check_for_drift_fault():
    return DRIFT_FAKE or random.random() < 0.2  # 20% chance of simulated drift

def drift_hold():
    print("[DRIFT_HOLD] Detected simulated drift. Holding position...")
    time.sleep(3)

def land():
    print("Initiating landing...")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.armed:
        print(f" Altitude during landing: {vehicle.location.global_relative_frame.alt:.2f}")
        time.sleep(1)
    print("Landed and disarmed.")

# ------------------ FSM Execution ------------------ #
try:
    arm_and_takeoff(TARGET_ALTITUDE)
    current_state = State.SCAN

    while True:
        if current_state == State.SCAN:
            if check_for_drift_fault():
                current_state = State.DRIFT_HOLD
            elif forward_scan():
                current_state = State.SIDESTEP
            elif check_for_goal():
                current_state = State.GOAL_FOUND

        elif current_state == State.SIDESTEP:
            sidestep_right()
            current_state = State.SCAN

        elif current_state == State.GOAL_FOUND:
            current_state = State.LAND

        elif current_state == State.DRIFT_HOLD:
            drift_hold()
            current_state = State.SCAN

        elif current_state == State.LAND:
            land()
            break

        else:
            print(f"[ERROR] Unknown state: {current_state}")
            break

except KeyboardInterrupt:
    print("Mission interrupted by user.")
finally:
    vehicle.close()
