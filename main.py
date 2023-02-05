import time
from ImageProcessing.ThreadCamera import ThreadCamera
from DroneCode.Drone import Drone

# thread camera is instantiated
cap = ThreadCamera(src=0).start()


drone = Drone()
drone.vehicle_info()
time.sleep(3)
drone.arm()
time.sleep(3)
drone.set_speed(150, 250)
time.sleep(1)
drone.simple_takeoff(10)
time.sleep(5)
print(drone.get_location())
time.sleep(1)
# drone.Upload_mission("deneme.txt")
# time.sleep(2)
# drone.Change_mode("AUTO")
# time.sleep(30)
drone.change_mode("GUIDED")
time.sleep(1)
while True:
    value = cap.detect_mid_and_close()
    print(value)
    if value == "east":
        drone.change_velocity(0,1,0,1)
        time.sleep(1)
    elif value == "west":
        drone.change_velocity(0, -1, 0, 1)
        time.sleep(1)
    elif value == "center":
        drone.change_velocity(1,0,0,1)
        time.sleep(1)


time.sleep(1)
drone.change_mode("LAND")
time.sleep(5)
drone.close_vehicle()
