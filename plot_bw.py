import numpy as np
import matplotlib
import matplotlib.pyplot as plt

##============================================================================##
##----------------------------- plot_bw.py -----------------------------##
##============================================================================##

'''
Purpose:             Plotting bandwidth over time

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         August 24, 2017
Date Last Modified:   August 24, 2017
'''

##============================================================================##
##--------------------------------- plot---- -------------------------------##
##============================================================================##


with open("tx_values") as f:
    data = f.readlines()
with open("time.out") as f:
    time = f.readlines()
#data = data.split('\n')
#time = time.split('\n')

x = [line.split(' ')[0] for line in time]
y = [line.split(' ')[0] for line in data]

##matplotlib.pyplot.plot_date(data,time)
fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Bandwidth Utilization: Chameleon Node to  Chameleon Node")
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Data Transfer Rate (Bytes/Second)')

ax1.plot(x,y, c='r', label='Bandwidth Utilization')

leg = ax1.legend()

plt.show()
