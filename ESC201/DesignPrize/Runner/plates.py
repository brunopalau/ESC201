# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 08:37:43 2021

@author: User
"""


import numpy as np
import matplotlib.cm as cm
import time
import sys
sys.path.insert(1,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/Classes_Functions")
from Setting import Setting
from Electrons import Electrons
from Output import save_output, compare_output


'''actual script that has to run. It includes the creation of all needed objects like the setting and its electrons aswell as the needed calls to 
functions like run, move, and save_output. Different variants of these scripts exist, trying to group similar starting conditions or similiar ideas/concepts together'''
    

def plates01(setting):
    setting.boundary_function = "plates01"
    setting.comment = "Inspired by points04 but trying to minimize the amount of plates used.\nLooking at the potential density plot we see that the last column has very low potential.\nThis seems to be crucial for the electrons that dont fully arrive and turn all the way back"
    space = 5
    length = 4
    x = np.linspace(1,98,30)
    y = x**0.849+25
    for i,num in enumerate(x):
        if not i%space:
            setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),min(250+30*i,800))
        
def plates02(setting):
    setting.boundary_function = "plates02"
    setting.comment = "Very much successful with just adjusting last plate and creating more of a gradient due to larger steps, Many electrons didnt hit -> potential too small"
    space = 10
    length = 8
    x = np.linspace(1,98,100)
    y = x**0.849+25
    for i,num in enumerate(x):
        if i == len(x)-1:
            setting.placePlate((int(x[i]),int(y[i])),(99,75),min(250+50*(i/space),800))
        elif not i%space:
            setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),min(250+30*(i/space),800))
            

def plates04(setting):
    setting.boundary_function = "plates04"
    setting.comment = "Trying to minimize amount of plates to compensate made much bigger steps in potential. Last plate doesnt always fit so turned around order the plates are placed.\nCreates an almost as perfect gradient with 6 plates"
    space = 20
    length = 16
    x = np.linspace(99,2,100)
    y = x**0.849+25
    for i,num in enumerate(x):
        if i == len(x)-1:
            setting.placePlate((int(x[i]),int(y[i])),(1,25),min(250*((len(x)-(i))/space),850))
        if not i%space:
            setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),min(250*((len(x)-i)/space),850))
            
            
def plates05(setting):
    setting.boundary_function = "plates05"
    setting.comment = ""
    space = 20
    length = 16
    x = np.linspace(99,2,100)
    y = x**0.849+25
    for i,num in enumerate(x):
        if i == len(x)-1:
            setting.placePlate((int(x[i]),int(y[i])),(1,25),min(250*((len(x)-(i))/space),850))
        if not i%space:
            setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),min(250*((len(x)-i)/space),850))
            
def plates06(setting):
    setting.boundary_function = "plates06"
    setting.comment = "Find lowest possible amount of plates to still create sufficient gradient\nImportant to scale the space inbetween the plates according to difference in potential so gradient is smooth"
    space = 44
    length = 36
    x = np.linspace(99,2,100)
    y = x**0.849+25
    for i,num in enumerate(x):
        try:
            if not i%space:
                setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),min(100+300*((len(x)-i)/space),850))
        except IndexError:
            setting.placePlate((int(x[i]),int(y[i])),(1,25),min(50+300*((len(x)-(i))/space),850))
    setting.placePlate((99,73),(99,75),1000)



def plates_simple(setting):
    setting.boundary_function = "plates_simple"
    setting.comment = "Simple version with almost same performance. One plate less and linear order of plates"
    space = 44
    length = 36
    x = np.linspace(99,2,100)
    y = 0.5*x+25
    potential = [680,480,130]
    for i,num in enumerate(x):
        try:
            if not i%space:
                setting.placePlate((int(x[i]),int(y[i])),(int(x[i+length]),int(y[i+length])),potential[i//space])
        except IndexError:
            pass
    setting.placePlate((99,73),(99,75),1000)

def main(): 
    '''make calls for each starting condition'''
    cmap = cm.get_cmap(name='Reds')
    
    # start1 = time.time()
    # set1 = Setting(100,cmap,1.91,True)
    # plates01(set1)
    # set1.run()
    # finished_setting1 = time.time()
    # E1 = Electrons(set1)
    # E1.addParticles(50)
    # E1.move(1e-11,True)
    # save_output(set1,E1,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish1 = time.time()
    # print(f"Setting: {finished_setting1-start1}")
    # print(f"Calculation: {finish1-finished_setting1}")
    
    # start2 = time.time()
    # set2 = Setting(100,cmap,1.91,True)
    # plates02(set2)
    # set2.run()
    # finished_setting2 = time.time()
    # E2 = Electrons(set2)
    # E2.addParticles(500)
    # E2.move(1e-11,True)
    # save_output(set2,E2,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish2 = time.time()
    # print(f"Setting: {finished_setting2-start2}")
    # print(f"Calculation: {finish2-finished_setting2}")
    
    # start3 = time.time()
    # set3 = Setting(100,cmap,1.91,True)
    # plates03(set3)
    # set3.run()
    # finished_setting3 = time.time()
    # E3 = Electrons(set3)
    # E3.addParticles(500)
    # E3.move(1e-11,True)
    # save_output(set3,E3,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish3 = time.time()
    # print(f"Setting: {finished_setting3-start3}")
    # print(f"Calculation: {finish3-finished_setting3}")
     
    # start4 = time.time()
    # set4 = Setting(100,cmap,1.91,True)
    # plates04(set4)
    # set4.run()
    # finished_setting4 = time.time()
    # E4 = Electrons(set4)
    # E4.addParticles(500)
    # E4.move(1e-11,True)
    # save_output(set4,E4,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish4 = time.time()
    # print(f"Setting: {finished_setting4-start4}")
    # print(f"Calculation: {finish4-finished_setting4}")
      
    # start5 = time.time()
    # set5 = Setting(100,cmap,1.91,True)
    # plates05(set5)
    # set5.run()
    # finished_setting5 = time.time()
    # E5 = Electrons(set5)
    # E5.addParticles(500)
    # E5.move(1e-11,True)
    # save_output(set5,E5,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish5 = time.time()
    # print(f"Setting: {finished_setting5-start5}")
    # print(f"Calculation: {finish5-finished_setting5}")
    
    # start6 = time.time()
    # set6 = Setting(100,cmap,1.91,True)
    # plates06(set6)
    # set6.run()
    # finished_setting6 = time.time()
    # E6 = Electrons(set6)
    # E6.addParticles(500)
    # E6.move(1e-11,True)
    # save_output(set6,E6,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish6 = time.time()
    # print(f"Setting: {finished_setting6-start6}")
    # print(f"Calculation: {finish6-finished_setting6}")
    
    start7 = time.time()
    set7 = Setting(100,cmap,1.91,True)
    plates_simple(set7)
    set7.run()
    finished_setting7 = time.time()
    E7 = Electrons(set7)
    E7.addParticles(5000)
    E7.move(1e-11,True)
    save_output(set7,E7,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)
    finish7 = time.time()
    print(f"Setting: {finished_setting7-start7}")
    print(f"Calculation: {finish7-finished_setting7}")
    
    
if __name__== "__main__":
    main()