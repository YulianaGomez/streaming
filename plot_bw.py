import numpy as np
import matplotlib
import matplotlib.pyplot as plt


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

ax1.set_title("Bandwidth Utilization from Chameleon to Cooley")
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Bytes Transferred')

ax1.plot(x,y, c='r', label='Bytes')

leg = ax1.legend()

plt.show()
