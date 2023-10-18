# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 20:14:47 2021

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

'''acttual script that has to run. It includes the creation of all needed objects like the setting and its electrons aswell as the needed calls to 
functions like run, move, and save_output. Different variants of these scripts exist, trying to group similar starting conditions or similiar ideas/concepts together'''
    
def tweezer01(setting):
    setting.boundary_function = "tweezer01"
    setting.comment = "Improved Version: Used different lengths and differnet potential, but if potential too strong it pulls electrons back.\nNot having a verical plate connecting both tips lead to many electrons going up or down"
    setting.placePlate((15,40),(99,75),500)
    setting.placePlate((15,10),(99,75),500)
    setting.placePlate((15,10),(15,40),200)
    
        
def tweezer01_neg_plate(setting):
    setting.boundary_function = "tweezer01_neg_plate"
    setting.comment = "Negativ plates lead to more oscillation"
    setting.placePlate((5,35),(99,75),500)
    setting.placePlate((5,15),(99,75),500)
    # setting.placePlate((15,10),(15,40),200)
    setting.placePlate((80,99),(1,55),-200)
    setting.placePlate((5,5),(99,20),-200)

def tweezer01_pos_plate(setting):
    setting.boundary_function = "tweezer01_pos_plate"
    setting.placePlate((5,35),(93,75),500)
    setting.placePlate((5,15),(93,75),500)
    # setting.placePlate((15,10),(15,40),200)
    setting.placePlate((99,80),(99,70),800)
    
def tweezer_two_different_pot(setting):
    setting.placePlate((15,40),(99,75),700)
    setting.placePlate((15,10),(99,75),400)
    setting.placePlate((15,10),(15,40),200)
    
     
# Main__________________________________________________________________________

def main(): 
    cmap = cm.get_cmap(name='Reds')
    
    
    
    # start4 = time.time()
    # set4 = Setting(100,cmap,2/1.91,True)
    # tweezer01(set4)
    # set4.run()
    # finished_setting4 = time.time()
    # E4 = Electrons(set4)
    # E4.addParticles(500)
    # E4.move(1e-11,True)#1e-10/11
    # finish4 = time.time()
    # save_output(set4,E4,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)   
    # print(f"Setting: {finished_setting4-start4}")
    # print(f"Calculation: {finish4-finished_setting4}")
    
 

    # start5 = time.time()
    # set5 = Setting(100,cmap,1.91,True)
    # tweezer01_neg_plate(set5)
    # set5.run()
    # finished_setting5 = time.time()
    # E5 = Electrons(set5)
    # E5.addParticles(500)
    # E5.move(1e-11,True)#1e-10/11
    # finish5 = time.time()
    # save_output(set5,E5,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)    
    # print(f"Setting: {finished_setting5-start5}")
    # print(f"Calculation: {finish5-finished_setting5}")
    
        
    start6 = time.time()
    set6 = Setting(100,cmap,1.91,True)
    tweezer01_pos_plate(set6)
    set6.run()
    finished_setting6 = time.time()
    E6 = Electrons(set6)
    E6.addParticles(500)
    E6.move(1e-10,True)#1e-10/11
    finish6 = time.time()
    save_output(set6,E6,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt",True)    
    print(f"Setting: {finished_setting6-start6}")
    print(f"Calculation: {finish6-finished_setting6}")
        
    
    #because most go from up to low and hit lower wall or no wall hand go back to hit left -> all hit upper wall with 300,500 pot
    # start8 = time.time()
    # set8 = Setting(100,cmap,1.91,True)
    # tweezer_two_different_pot(set8)
    # set8.run()
    # finished_setting8 = time.time()
    # E8 = Electrons(set8)
    # E8.addParticles(500)
    # E8.move(1e-10,True)#1e-10/11
    # finish8 = time.time()
    
    # print(f"Setting: {finished_setting8-start8}")
    # print(f"Calculation: {finish8-finished_setting8}")
    
if __name__== "__main__":
    main()
    