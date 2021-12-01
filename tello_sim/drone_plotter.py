from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
# import numpy as np
import pandas as pd


# Plotting functions
def plot_altitude_steps(drone1_alt, drone2_alt, drone3_alt):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(drone1_alt, 'ro--', linewidth=2, markersize=12, label="Drone 1")
    ax.plot(drone2_alt, 'b^-.', linewidth=2, markersize=12, label="Drone 2")
    ax.plot(drone3_alt, 'gd:', linewidth=2, markersize=12, label="Drone 3")
    ax.grid()
    ax.set(xlabel='Step', ylabel='Altitude in Centimeters', title='Tello Altitude')
    ax.legend()

    plt.show()


def plot_horz_steps(drone1, drone2, drone3):
    drone1_bearing, drone1_path_coors, drone1_flip_coors = drone1
    drone2_bearing, drone2_path_coors, drone2_flip_coors = drone2
    drone3_bearing, drone3_path_coors, drone3_flip_coors = drone3
    if drone1_flip_coors is None:
        drone1_flip_coors = []
    if drone2_flip_coors is None:
        drone2_flip_coors = []
    if drone3_flip_coors is None:
        drone3_flip_coors = []

    title = "Path of drones from Takeoff Location."
    fig, ax = plt.subplots()

    drone1_horz_df = pd.DataFrame(drone1_path_coors)
    drone1_xlow = min(drone1_horz_df[0])
    drone1_xhi = max(drone1_horz_df[0])
    drone1_ylow = min(drone1_horz_df[1])
    drone1_yhi = max(drone1_horz_df[1])
    drone1_xlowlim = -200 if drone1_xlow > -200 else drone1_xlow - 40
    drone1_xhilim = 200 if drone1_xhi < 200 else drone1_xhi + 40
    drone1_ylowlim = -200 if drone1_ylow > -200 else drone1_ylow - 40
    drone1_yhilim = 200 if drone1_yhi < 200 else drone1_yhi + 40
    ax.set_xlim([drone1_xlowlim, drone1_xhilim])
    ax.set_ylim([drone1_ylowlim, drone1_yhilim])
    ax.plot(drone1_horz_df[0], drone1_horz_df[1], 'ro--', linewidth=2, markersize=12, label="Drone 1")

    drone2_horz_df = pd.DataFrame(drone2_path_coors)
    drone2_xlow = min(drone2_horz_df[0])
    drone2_xhi = max(drone2_horz_df[0])
    drone2_ylow = min(drone2_horz_df[1])
    drone2_yhi = max(drone2_horz_df[1])
    drone2_xlowlim = -200 if drone2_xlow > -200 else drone2_xlow - 40
    drone2_xhilim = 200 if drone2_xhi < 200 else drone2_xhi + 40
    drone2_ylowlim = -200 if drone2_ylow > -200 else drone2_ylow - 40
    drone2_yhilim = 200 if drone2_yhi < 200 else drone2_yhi + 40
    ax.set_xlim([drone2_xlowlim, drone2_xhilim])
    ax.set_ylim([drone2_ylowlim, drone2_yhilim])
    ax.plot(drone2_horz_df[0], drone2_horz_df[1], 'b^-', linewidth=2, markersize=12, label="Drone 2")

    drone3_horz_df = pd.DataFrame(drone3_path_coors)
    drone3_xlow = min(drone3_horz_df[0])
    drone3_xhi = max(drone3_horz_df[0])
    drone3_ylow = min(drone3_horz_df[1])
    drone3_yhi = max(drone3_horz_df[1])
    drone3_xlowlim = -200 if drone3_xlow > -200 else drone3_xlow - 40
    drone3_xhilim = 200 if drone3_xhi < 200 else drone3_xhi + 40
    drone3_ylowlim = -200 if drone3_ylow > -200 else drone3_ylow - 40
    drone3_yhilim = 200 if drone3_yhi < 200 else drone3_yhi + 40
    ax.set_xlim([drone3_xlowlim, drone3_xhilim])
    ax.set_ylim([drone3_ylowlim, drone3_yhilim])
    ax.plot(drone3_horz_df[0], drone3_horz_df[1], 'gd:', linewidth=2, markersize=12, label="Drone 3")

    if len(drone1_flip_coors) > 0:
        flip_df = pd.DataFrame(drone1_flip_coors)
        ax.plot(flip_df[0], flip_df[1], 'mo', markersize=12, label="Drone Flips")
    if len(drone2_flip_coors) > 0:
        flip_df = pd.DataFrame(drone2_flip_coors)
        ax.plot(flip_df[0], flip_df[1], 'c^', markersize=12, label="Drone Flips")
    if len(drone3_flip_coors) > 0:
        flip_df = pd.DataFrame(drone3_flip_coors)
        ax.plot(flip_df[0], flip_df[1], 'yd', markersize=12, label="Drone Flips")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid()
    ax.legend()
    ax.set(xlabel='X Distance from Takeoff', ylabel='Y Distance from Takeoff', title=title)
    plt.show()
