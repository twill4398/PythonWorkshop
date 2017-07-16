# -*- coding: utf-8 -*-
"""
MSUQFA Python Workshop Intermediate/Advanced
Topic: Monte Carlo Simulations

Monte Carlo Simulation to Determine the Value of Pi

"""

"""
How it works:

Let us inscribe a unit circle inside a 2x2 square centered around the origin
(as shown on the board).

We generate a number of random coordinates, then count how many lie within 
the bounds of the circle versus how many lie within the bounds of the square.

That ratio is equal to the ratio of areas.  Since the area of the circle is Pi
and the area of the square is 4, their ratio is Pi over 4; we can thus solve 
for Pi.

"""

import random
import math
import matplotlib.pyplot as plt


iterations = int(input("How many iterations: "))

## We'll be graphing later to illustrate the point
iterations_list = []
error_list = []


while(iterations != 0):
    ## We begin by getting user input for the number of iterations to complete.
    
    
    ## Now we set the count of coordinates that lie within the circle and within 
    ## the square to 0.
    
    count_circle, count_square = 0,0
    
    ## Now let's do the number of iterations
    for i in range(iterations):
        
        #random generates a number 0 <= num < 1.0
        x = random.random()
        y = random.random()
        
        count_square += 1
        
        #if these coordinates lie in the circle
        if x ** 2 + y ** 2 <= 1: 
            count_circle += 1
            
    pi_estimate = 4 * count_circle/count_square
    error = math.pi - pi_estimate
    
    #For graphing 
    iterations_list.append(iterations)
    error_list.append(error)
    
    print("With", iterations, " iterations, our Pi estimate is: ", pi_estimate)
    print("This differs from our true value by: ", error)
    
    iterations = int(input("How many iterations: "))
 
   
plt.semilogx(iterations_list, error_list, 'bo')
plt.ylabel("Deviation from Pi")
plt.xlabel("Number of iterations")
plt.show()


