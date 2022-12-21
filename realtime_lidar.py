#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, pi
from matplotlib.animation import FuncAnimation
import rospy
from sensor_msgs.msg import LaserScan
import time


class lidar_plot:
    def __init__(self, scan_topic):
        # subscribing the scan topic
        print(scan_topic)
        self.scan_info = rospy.Subscriber(
            scan_topic, LaserScan, self._scan_registration)
        self.fig = plt.figure()
        self.ax = plt.axes()
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.scatter = self.ax.scatter([], [])
        self.x_arr = []
        self.y_arr = []
        # plt.axis("equal")
        # self.start()
        plt.grid()

    def _scan_registration(self, scan_topic):

        self.angle_min = scan_topic.angle_min  # in radians
        self.angle_max = scan_topic.angle_max  # in radians
        self.angle_increment = scan_topic.angle_increment
        self.range_min = scan_topic.range_min
        self.range_min = scan_topic.range_max
        self.range_arr = scan_topic.ranges  # array of range values
        self.plotting_scan()
        # passing the range info to plotting scan

    def plotting_scan(self):
        x_arr = []
        y_arr = []
        angle_min = self.angle_min
        t = time.time()
        for i in self.range_arr:
            angle_min = angle_min + self.angle_increment
            x = i * np.cos(angle_min)
            y = i * np.sin(angle_min)
            x_arr.append(x)
            y_arr.append(y)

        self.x_arr = x_arr
        self.y_arr = y_arr

        # print(x_arr)
        # return x_arr, y_arr

    def _update(self, i):
        points = np.transpose(np.array([self.x_arr, self.y_arr]))
        self.scatter.set_offsets(points)
        return self.scatter,

    def start(self):
        self.anim = FuncAnimation(
            self.fig, self._update, interval=20, blit=True)


if __name__ == "__main__":
    rospy.init_node("scan_node", anonymous=False)
    scan_topic = "/scan"
    read = lidar_plot(scan_topic)
    read.start()
    plt.show()

    rospy.spin()


# def data_read(f):
#     """
#     Reading LIDAR laser beams (angles and corresponding distance data)
#     """
#     measures = [line.split(",") for line in open(f)]
#     angles = []
#     distances = []
#     for measure in measures:
#         angles.append(float(measure[0]))
#         distances.append(float(measure[1]))
#     angles = np.array(angles)
#     distances = np.array(distances)

#     ang, dist = data_read("lidar01.csv")
#     ox = np.sin(ang) * dist
#     oy = np.cos(ang) * dist

#     return angles, distances


# def listner():
#     rospy.init_node("scan_node", anonymous=False)
#     rospy.Subscriber("/scan", LaserScan, data_read)


# plt.axis("equal")


# fig = plt.figure()

# # marking the x-axis and y-axis
# axis = plt.axes(xlim=(-5, 5),
#                 ylim=(-5, 5))

# line, = axis.plot([], [], lw=3)


# def init():
#     line.set_data([], [])
#     return line,


# def animate(i):
#     x = np.linspace(0, 4, 1000)

#     # plots a sine graph
#     y = np.sin(2 * np.pi * (x - 0.01 * i))
#     line.set_data(x, y)

#     return line,


# anim = FuncAnimation(fig, animate, init_func=init,
#                      frames=200, interval=20, blit=True)
