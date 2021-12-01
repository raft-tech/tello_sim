import json
import time
# from matplotlib import pyplot as plt
# from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
# import pandas as pd

from easytello.tello import Tello
import tello_sim.drone_plotter as drone_plotter


class Drone:
    def __init__(self, name):
        self.name = name
        self.takeoff_alt = 81
        self._init_state()
        self.driver_instance = None

        # Put drone into command mode
        self.command()

    def _init_state(self):
        self.altitude = 0
        self.cur_loc = (0, 0)
        self.bearing = 0
        self.altitude_data = []
        self.path_coors = [(0, 0)]
        self.flip_coors = []
        self.fig_count = 1
        self.command_log = []

    @staticmethod
    def serialize_command(command: dict):
        serialized = command['command']
        command_args = command.get('arguments', ())
        if len(command_args) > 0:
            serialized = '{} {}'.format(serialized, ' '.join([str(arg) for arg in command_args]))
        return serialized

    @staticmethod
    def check_flip_param(param: str):
        if param not in ["f", "b", "r", "l", ""]:
            raise Exception("I can't tell which way to flip. Please use f, b, r, or l. If not flipping, use ''")
        else:
            pass

    @staticmethod
    def check_int_param(param: int):
        if type(param) != int:
            raise Exception("This command only accepts whole numbers without quotation marks.")
        else:
            pass

    def send_command(self, command: str, *args):
        # Command log allows for replaying commands to the actual drone
        command_json = {
            'command': command,
            'arguments': args
        }
        self.command_log.append(command_json)
        print('I am running your "{}" command.'.format(self.serialize_command(command_json)))

        time.sleep(2)

    # Control Commands
    def command(self):
        print(f"Hi! I am {self.name}.")
        print("I am now ready to take off. 🚁")
        self.send_command('command')

    def check_altitude(self):
        if self.altitude == 0:
            raise Exception("I can't do that unless I take off first!")
        else:
            print(f"{self.name} flying at {self.altitude} centimeters above my takeoff altitude.")
            pass

    # Determine bearing relative to start which is inline with positive y-axis
    @staticmethod
    def dist_bearing(orig, bearing, dist):
        rads = np.deg2rad(bearing)
        sines = np.sin(rads)
        coses = np.cos(rads)
        dx = sines * dist
        dy = coses * dist
        x_n = np.cumsum(dx) + orig[0]
        y_n = np.cumsum(dy) + orig[1]
        return x_n[0], y_n[0]

    # Movement Commands
    def takeoff(self):
        """
        Command drone to takeoff.

        Examples
        ----------
        drone.takeoff() # command drone to takeoff

        """
        if self.altitude == 0:
            print(f"{self.name} ready for takeoff!")
            self.altitude = self.takeoff_alt
            self.altitude_data.append(self.takeoff_alt)
            self.send_command('takeoff')
            print(f"{self.name} estimated takeoff altitude is {self.altitude} centimeters")
        else:
            print(f"{self.name} current altitude is {self.altitude} centimeters, so I can't takeoff again!")
        print("\n")

    def land(self):
        """
        Command drone to land.

        Examples
        ----------
        drone.land() # command drone to land

        """
        print(f"{self.name} ready for landing!")
        self.check_altitude()
        self.altitude = 0
        self.send_command('land')
        print("All drones have landed")
        print("\n")

    def up(self, dist: int):
        """
        Command drone to fly up a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.up(100) # move drone up 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        print(f"{self.name} current bearing is {self.bearing} degrees.")

        self.altitude = self.altitude + dist
        self.altitude_data.append(self.altitude)
        self.send_command('up', dist)
        print("\n")

    def down(self, dist: int):
        """
        Command drone to fly down a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.down(100) # move drone down 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        print(f"{self.name} current bearing is {self.bearing} degrees.")

        self.altitude = self.altitude - dist
        self.altitude_data.append(self.altitude)
        self.send_command('down', dist)
        print("\n")

    def left(self, dist: int):
        """
        Command drone to fly left a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.left(100) # move drone left 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        print(f"{self.name} current bearing is {self.bearing} degrees.")

        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing - 90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        print(self.path_coors)
        self.send_command('left', dist)
        print("\n")

    def right(self, dist: int):
        """
        Command drone to fly right a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.right(100) # move drone right 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        print(f"{self.name} current bearing is {self.bearing} degrees.")

        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing + 90, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('right', dist)
        print("\n")

    def forward(self, dist: int):
        """
        Command drone to fly forward a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.forward(100) # move drone forward 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        print(f"{self.name} current bearing is {self.bearing} degrees.")

        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('forward', dist)
        print("\n")

    def back(self, dist: int):
        """
        Command drone to fly backward a given number of centimeters.

        Parameters
        ----------
        dist : int

        Examples
        ----------
        drone.back(100) # move drone backward 100 centimeters

        """
        self.check_altitude()
        self.check_int_param(dist)
        new_loc = self.dist_bearing(orig=self.cur_loc, bearing=self.bearing + 180, dist=dist)
        self.cur_loc = new_loc
        self.path_coors.append(new_loc)
        self.send_command('back', dist)
        print("\n")

    def cw(self, degr: int):
        """
        Rotate drone clockwise.

        Parameters
        ----------
        degr : int

        Examples
        ----------
        drone.cw(90) # rotates drone 90 degrees clockwise

        """
        self.check_altitude()
        self.check_int_param(degr)
        print(f"{self.name} current bearing is {self.bearing} degrees.")
        self.bearing = self.bearing + (degr % 360)
        self.send_command('cw', degr)
        print(f"{self.name} new bearing is {self.bearing} degrees.")
        print("\n")

    def ccw(self, degr: int):
        """
        Rotate drone counter clockwise.

        Parameters
        ----------
        degr : int

        Examples
        ----------
        drone.ccw(90) # rotates drone 90 degrees counter clockwise

        """
        self.check_altitude()
        self.check_int_param(degr)
        print(f"{self.name} current bearing is {self.bearing} degrees.")
        self.bearing = self.bearing - (degr % 360)
        self.send_command('ccw', degr)
        print(f"{self.name} current bearing is {self.bearing} degrees.")
        print("\n")

    def flip(self, direc: str):
        """
        Flips drones in one of four directions:
        l - left
        r - right
        f - forward
        b - back

        Parameters
        ----------
        direc : str

        Examples
        ----------
        drone.flip("f") # flips drone forward

        """
        self.check_altitude()
        self.check_flip_param(direc)
        if direc == "":
            pass
        else:
            self.send_command('flip', direc)
        self.flip_coors.append(self.cur_loc)
        # drone_plotter.plot_horz_steps(self.bearing, self.path_coors, self.flip_coors)
        print("\n")

    # Resets the simulation state back to the beginning: no commands + landed
    def reset(self):
        """
        Reset the drone object to initialization state.

        Examples
        ----------
        drone.reset() # reset sim state

        """
        print('Resetting simulator state...')
        self._init_state()
        self.command()
        print("\n")


class Swarm:
    def __init__(self):
        self.drone1 = Drone("Drone_1")
        self.drone2 = Drone("Drone_2")
        self.drone3 = Drone("Drone_3")

    def swarm_takeoff(self):
        """Set all drones to takeoff"""
        self.drone1.takeoff()
        self.drone2.takeoff()
        self.drone3.takeoff()

    def swarm_land(self):
        self.drone1.land()
        self.drone2.land()
        self.drone3.land()

    def swarm_up(self, up1, up2, up3):
        self.drone1.up(up1)
        self.drone2.up(up2)
        self.drone3.up(up3)
        drone_plotter.plot_altitude_steps(self.drone1.altitude_data, self.drone2.altitude_data,
                                          self.drone3.altitude_data)

    def swarm_down(self, down1, down2, down3):
        self.drone1.down(down1)
        self.drone2.down(down2)
        self.drone3.down(down3)
        drone_plotter.plot_altitude_steps(self.drone1.altitude_data, self.drone2.altitude_data,
                                          self.drone3.altitude_data)

    def swarm_left(self, left1, left2, left3):
        self.drone1.left(left1)
        self.drone2.left(left2)
        self.drone3.left(left3)
        drone_plotter.plot_horz_steps((self.drone1.bearing, self.drone1.path_coors, self.drone1.flip_coors),
                                      (self.drone2.bearing, self.drone2.path_coors, self.drone2.flip_coors),
                                      (self.drone3.bearing, self.drone3.path_coors, self.drone3.flip_coors))

    def swarm_right(self, right1, right2, right3):
        self.drone1.right(right1)
        self.drone2.right(right2)
        self.drone3.right(right3)
        drone_plotter.plot_horz_steps((self.drone1.bearing, self.drone1.path_coors, self.drone1.flip_coors),
                                      (self.drone2.bearing, self.drone2.path_coors, self.drone2.flip_coors),
                                      (self.drone3.bearing, self.drone3.path_coors, self.drone3.flip_coors))

    def swarm_forward(self, for1, for2, for3):
        self.drone1.forward(for1)
        self.drone2.forward(for2)
        self.drone3.forward(for3)
        drone_plotter.plot_horz_steps((self.drone1.bearing, self.drone1.path_coors, self.drone1.flip_coors),
                                      (self.drone2.bearing, self.drone2.path_coors, self.drone2.flip_coors),
                                      (self.drone3.bearing, self.drone3.path_coors, self.drone3.flip_coors))

    def swarm_back(self, back1, back2, back3):
        self.drone1.back(back1)
        self.drone2.back(back2)
        self.drone3.back(back3)
        drone_plotter.plot_horz_steps((self.drone1.bearing, self.drone1.path_coors, self.drone1.flip_coors),
                                      (self.drone2.bearing, self.drone2.path_coors, self.drone2.flip_coors),
                                      (self.drone3.bearing, self.drone3.path_coors, self.drone3.flip_coors))

    def swarm_cw(self, cw1, cw2, cw3):
        self.drone1.cw(cw1)
        self.drone2.cw(cw2)
        self.drone3.cw(cw3)

    def swarm_ccw(self, ccw1, ccw2, ccw3):
        self.drone1.ccw(ccw1)
        self.drone2.ccw(ccw2)
        self.drone3.ccw(ccw3)

    def swarm_flip(self, flip1, flip2, flip3):
        self.drone1.flip(flip1)
        self.drone2.flip(flip2)
        self.drone3.flip(flip3)
        drone_plotter.plot_horz_steps((self.drone1.bearing, self.drone1.path_coors, self.drone1.flip_coors),
                                      (self.drone2.bearing, self.drone2.path_coors, self.drone2.flip_coors),
                                      (self.drone3.bearing, self.drone3.path_coors, self.drone3.flip_coors))

    def swarm_rest(self):
        self.drone1.reset()
        self.drone2.reset()
        self.drone3.reset()


if __name__ == "__main__":
    swarm = Swarm()
    swarm.swarm_takeoff()
    swarm.swarm_up(50, 25, 0)
    swarm.swarm_left(40, 0, 0)
    swarm.swarm_right(0, 35, 0)
    swarm.swarm_ccw(0, 0, 45)
    swarm.swarm_forward(0, 60, 60)
    swarm.swarm_flip("f", "", "r")
    swarm.swarm_down(20, 0, 5)
    swarm.swarm_forward(35, 60, 80)
    swarm.swarm_land()
