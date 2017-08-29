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

def plot_bw():
    with open("tx_values") as f:
        data = f.readlines()
    with open("time.out") as f:
        time = f.readlines()
    #data = data.split('\n')
    #time = time.split('\n')

    x = [line.split('\t')[0] for line in data]
    y = [line.split('\t')[1] for line in data]
    #y = [line.split('')[0] for line in data]

    ##matplotlib.pyplot.plot_date(data,time)
    fig = plt.figure()

    ax1 = fig.add_subplot(111)

    ax1.set_title("Bandwidth Utilization: 50GB from Chameleon Bare Metal Node to 4 Cooley Nodes")
    ax1.set_xlabel('Time (s)')
    plt.xlim(0,30)
    ax1.set_ylabel('Data Transfer Rate (Bytes/Second)')

    ax1.plot(x,y, c='r', label='Bandwidth Utilization')

    leg = ax1.legend()

    plt.show()

###################MAIN###########################
if __name__ == '__main__':

    plot_bw()
