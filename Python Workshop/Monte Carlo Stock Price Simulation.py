# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 12:34:34 2017

@author: twill
"""

"""
MSUQFA Intermediate/Advanced Workshop
Monte Carlo Simulation of S&P 500 Index Stock Returns

4/22/2017

We begin with historical return data for an index of the S&P 500.
We parse the data, obtaining values for the expected return for each day as 
well as the standard deviation of returns.

We then perform a Monte Carlo Simulation with a geometric brownian motion model
in order to get a better understanding of where the S&P will likely move in the
future.

"""


"""
Assumptions (for those who care):
    -Stock prices follow a random walk: past trends do not influence future trends
    -The weak form of the efficient market hypothesis holds: past information
     is already included and the next price movement is conditionally 
     independent of previous movements

We will use an average of returns over the past five years as an expected 
return for our index- this may not be entirely valid, but is the most intuitive
simple method for obtaning an expected return. 

"""

import numpy
import matplotlib.pyplot as plt
import scipy.stats as stt

fp = open("sp500_returnsdata.csv")
header = fp.readline() #get rid of the header so we can parse the rest


#get the closing prices into a list
closing_lst = []
for line in fp:
    
    line = line.strip().split(",")
    
    #time orders from earliest to latest- remember our csv begins with most recent
    closing_lst.insert( 0, float(line[4]) )
    
fp.close()

#turn closing prices into returns
returns_lst = []
for i in range(len(closing_lst) - 1):
    
        percent_return = (closing_lst[i+1] - closing_lst[i])/(closing_lst[i])
        returns_lst.append(percent_return)
        
#get some summary statistics
expected_return = numpy.mean(returns_lst)
stdev = numpy.std(returns_lst)

#implement our GBM model
#Change in price = price(expected return * change in time + random_var * stdev * sqrt(time))
#We use time =  1 day
simulation_list = []

num_sims = int(input("Input the number of simulations to be run: ") or 50)
duration = int(input("Enter the number of days ahead we ought to forecast: ") or 30)

for i in range(num_sims):
    
    old_price = closing_lst[-1]
    price_simulation = [old_price]
    
    for i in range(duration - 1):
        
        change_in_price = (expected_return * old_price) \
        + numpy.random.normal(0,1) * stdev * old_price
        
        new_price = old_price + change_in_price
        price_simulation.append(new_price)
        old_price = new_price
        
    simulation_list.append(price_simulation)
        
        
plt.xlabel("Days")
plt.ylabel("S&P 500 Value")
plt.title("Simulations of S&P 500 Index Value")


for i in range(len(simulation_list)):
    plt.plot(simulation_list[i])

plt.show()
        
# Let's do a confidence interval
finish_list = [ simulation_list[i][-1] for i in range(len(simulation_list)) ]

confidence_interval = stt.t.interval(.95, len(finish_list) - 1 ,\
loc=numpy.mean(finish_list), scale=stt.sem(finish_list))

confidence_interval = [round(element, 1) for element in confidence_interval]

print("The current value of the S&P 500 Index is: ", round(closing_lst[-1],2))
print("We can be 95% confident that the true value of the S&P 500 Index in",\
duration, "days will be in the range", confidence_interval, "given", num_sims,\
 "simulations.")

print("This confidence interval has a length of: ", confidence_interval[1] - confidence_interval[0])

