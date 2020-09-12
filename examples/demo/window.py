import csv

x = []
y = []
y2 = []
y3 = []
with open('output1200_200.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    x = []
    y = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            x.append(int(row[0]) / 2)
            y.append(float(row[1]))
            line_count += 1

with open('output12000_200.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count = 0
    y2 = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            y2.append(float(row[1]))
            line_count += 1

with open('output120000_200.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count = 0
    y3 = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            y3.append(float(row[1]))
            line_count += 1

import numpy as np
# def smooth(y, box_pts):
#     box = np.ones(box_pts)/box_pts
#     y_smooth = np.convolve(y, box, mode='same')
#     return y_smooth
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# xx = np.linspace(min(x),max(x), 200)

# itp = interp1d(x,y, kind='linear')
# window_size, poly_order = 9, 2
# yy_sg = savgol_filter(itp(xx), window_size, poly_order)

import matplotlib.pyplot as plt
plt.xlabel('cell execution count')
plt.ylabel('time (s)')
plt.plot(x, y, marker="o", label="1200 rows")
plt.plot(x, y2, marker="o", label="12000 rows")
plt.plot(x, y3, marker="o", label="120000 rows")

# plt.ylim(0, 10.0)
plt.legend(title="200 df calls \nwith dataset capped at 10K rows", loc='upper right', bbox_to_anchor=(1, 0.7))
# plt.legend(loc="upper left")

plt.show()