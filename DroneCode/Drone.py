from dronekit import connect, VehicleMode, mavlink, LocationGlobalRelative, Command, mavutil
import time


class Drone:
    def __init__(self):  # Class Constructor
        print("Connecting to drone..")
        self.vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, baud=921)
        print("Connected to drone!")

    def vehicle_info(self):  # Prints out vehicle info on log screen
        print("Get some vehicle attribute values:")
        print(" GPS: %s" % self.vehicle.gps_0)
        print(" Last Heartbeat: %s" % self.vehicle.last_heartbeat)
        print(" Is Armable?: %s" % self.vehicle.is_armable)
        print(" System status: %s" % self.vehicle.system_status.state)
        print(" Mode: %s" % self.vehicle.mode.name)
        print(" Attitude: %s" % self.vehicle.attitude)
        print(" Location: %s" % self.vehicle.location)
        print(" Armed: %s" % self.vehicle.armed)
        print(" Location lat: %s" % self.vehicle.location.global_relative_frame.lat)
        print(" Location lon: %s" % self.vehicle.location.global_relative_frame.lon)

    def arm(self):
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
        print("Arming motors")

        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

    def disarm(self):
        self.vehicle.armed = False

    def force_arm(self):
        self.vehicle.armed = True

    def change_mode(self, mode):
        self.vehicle.mode = VehicleMode(mode)
        print("mode was changed to:", mode)

    def simple_takeoff(self, desiredalt):
        print("Taking off!")
        self.vehicle.simple_takeoff(desiredalt)
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= desiredalt * 0.94:
                print("Reached target altitude")
                break
            time.sleep(1)

    def set_speed(self, acc=150, spd=250):
        self.vehicle.parameters["WPNAV_ACCEL"] = acc
        self.vehicle.parameters["WPNAV_SPEED"] = spd

    def upload_mission_advanced(self, filename):
        self.vehicle.commands.clear()
        # missionlist = []
        with open(filename) as f:
            for i, line in enumerate(f):
                if i == 0:
                    if not line.startswith('QGC WPL 110'):
                        raise Exception('File is not supported WP version')
                else:
                    linearray = line.split('\t')
                    # ln_index = int(linearray[0])
                    ln_currentwp = int(linearray[1])
                    ln_frame = int(linearray[2])
                    ln_command = int(linearray[3])
                    ln_param1 = float(linearray[4])
                    ln_param2 = float(linearray[5])
                    ln_param3 = float(linearray[6])
                    ln_param4 = float(linearray[7])
                    ln_param5 = float(linearray[8])
                    ln_param6 = float(linearray[9])
                    ln_param7 = float(linearray[10])
                    ln_autocontinue = int(linearray[11].strip())
                    cmd = Command(0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2,
                                  ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                    self.vehicle.commands.add(cmd)
                    print(
                        "0", "0", "0", ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2,
                        ln_param3,
                        ln_param4, ln_param5, ln_param6, ln_param7)
            self.vehicle.commands.upload()

    def upload_mission(self, filename):
        liste = []
        dosya = open(filename, 'r')
        for satir in dosya:
            line = satir.split(",")
            if len(line) == 3:
                x = float(line[0])
                y = float(line[1])
                alt = float(line[2])
                cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                              mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                              0, 0, 5,
                              0, 0,
                              0, x, y, alt)
                liste.append(cmd)
        dosya.close()

        cmds = self.vehicle.commands
        cmds.clear()
        # TakeOff Command
        cmds.add(
            Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0,
                    0, 0,
                    0,
                    0, 0, 0, 10))

        # uploading commands
        for command in liste:
            cmds.add(command)
        print(' Upload mission')
        self.vehicle.commands.upload()

    def get_location(self):
        lat = self.vehicle.location.global_relative_frame.lat
        long = self.vehicle.location.global_relative_frame.lon
        alt = self.vehicle.location.global_relative_frame.alt
        return lat, long, alt

    def change_velocity(self, velocity_x, velocity_y, velocity_z, duration):
        # IMPORTANT

        # Set up velocity mappings
        # velocity_x > 0 => fly North
        # velocity_x < 0 => fly South
        # velocity_y > 0 => fly East
        # velocity_y < 0 => fly West
        # velocity_z < 0 => ascend
        # velocity_z > 0 => descend
        # south = -2
        # up = -0.5  # NOTE: up is negative!

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,  # time_boot_ms (not used)
            0, 0,  # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111000111,  # type_mask (only speeds enabled)
            0, 0, 0,  # x, y, z positions (not used)
            velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
            0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        for x in range(0, duration):
            self.vehicle.send_mavlink(msg)
            print(x)
            time.sleep(1)

    def simple_goto(self, lat, lon):
        point1 = LocationGlobalRelative(lat, lon)
        self.vehicle.simple_goto(point1)

    def close_vehicle(self):
        self.vehicle.close()
