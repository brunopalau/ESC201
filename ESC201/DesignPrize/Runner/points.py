# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 19:29:22 2021

@author: User
"""


import numpy as np
import time
import matplotlib.cm as cm
import sys
sys.path.insert(1,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/Classes_Functions")
from Setting import Setting
from Electrons import Electrons
from Output import save_output, compare_output


'''actual script that has to run. It includes the creation of all needed objects like the setting and its electrons aswell as the needed calls to 
functions like run, move, and save_output. Different variants of these scripts exist, trying to group similar starting conditions or similiar ideas/concepts together'''
    
        
def points01(setting):
    setting.boundary_function = "points01"
    setting.placePlate((10,35),(13,25),200)
    setting.placePlate((15,25),(18,25),200)
    setting.placePlate((20,25),(23,25),200)
    setting.placePlate((25,25),(28,25),200)
    setting.placePlate((90,65),(90,75),800)
    # setting.placePlate((85,70),(95,70),600)
    # setting.placePlate((99,75),(99,75),1000)
    
def points02(setting):
    setting.boundary_function = "points02"
    x = np.linspace(0,95,20)
    y = x**0.849+25 #use exponential funcion trying to make a smooth connection between start and detector
    for i,num in enumerate(x):
        setting.placePlate((int(num),int(y[i])),(int(num)+1,int(y[i])+1),200+30*i)
        
def points03(setting):
    setting.boundary_function = "points03"
    x = np.linspace(0,95,30)
    y = x**0.849+25
    for i,num in enumerate(x):
        setting.placePlate((int(num),int(y[i])),(int(num)+1,int(y[i])+1),200+30*i)
    
def points04(setting):
    setting.boundary_function = "points04"
    setting.comment = "Improved version: tried different variants with less or more points, different steps in potential and a max potential.\n Mostly those starting on the upper edge end up looping and hitting the left wall"
    x = np.linspace(1,98,30)
    y = x**0.849+25
    for i,num in enumerate(x):
        setting.placePlate((int(num),int(y[i])),(int(num)+1,int(y[i])+1),min(200+25*i,800))
        
def points05(setting):
    setting.boundary_function = "points05"
    x = np.linspace(0,98,30)
    y = x**0.849+25
    for i,num in enumerate(x):
        setting.placePlate((int(num),int(y[i])),(int(num)+1,int(y[i])+1),100+30*i)
        
# Main__________________________________________________________________________

def main(): 
    cmap = cm.get_cmap(name='Reds')
    
    # start1 = time.time()
    # set1 = Setting(100,cmap,1.91,True)
    # points01(set1)
    # set1.run()
    # finished_setting1 = time.time()
    # E1 = Electrons(set1)
    # E1.addParticles(50)
    # E1.move(1e-11,True)
    # # save_output(set1,E1,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    # finish1 = time.time()
    # print(f"Setting: {finished_setting1-start1}")
    # print(f"Calculation: {finish1-finished_setting1}")
    
    # start2 = time.time()
    # set2 = Setting(100,cmap,1.91,True)
    # points02(set2)
    # set2.run()
    # finished_setting2 = time.time()
    # E2 = Electrons(set2)
    # E2.addParticles(50)
    # E2.move(1e-11,True)#1e-10/11
    # finish2 = time.time()
    # save_output(set2,E2,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)    
    # print(f"Setting: {finished_setting2-start2}")
    # print(f"Calculation: {finish2-finished_setting2}")
    
        
    start4 = time.time()
    set4 = Setting(100,cmap,1.91,True)
    points04(set4)
    set4.run()
    finished_setting4 = time.time()
    E4 = Electrons(set4)
    E4.addParticles(500)
    E4.move(1e-11,True)#1e-10/11
    finish4 = time.time()
    save_output(set4,E4,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)    
    print(f"Setting: {finished_setting4-start4}")
    print(f"Calculation: {finish4-finished_setting4}")
    
    # start5 = time.time()
    # set5 = Setting(100,cmap,1.91,True)
    # points05(set5)
    # set5.run()
    # finished_setting5 = time.time()
    # E5 = Electrons(set5)
    # E5.addParticles(50)
    # E5.move(1e-10,True)#1e-10/11
    # finish5 = time.time()
    # save_output(set5,E5,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)    
    # print(f"Setting: {finished_setting5-start5}")
    # print(f"Calculation: {finish5-finished_setting5}")
    
  
if __name__== "__main__":
    main()

    #time still ify
    #documentation and comments