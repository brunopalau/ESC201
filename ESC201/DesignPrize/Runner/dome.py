# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 13:21:41 2021

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
    
        
def dome01(setting):
    setting.boundary_function = "dome01"
    setting.placePlate((10,20),(35,45),300)
    setting.placePlate((10,40),(35,40),300)
    setting.placePlate((70,50),(70,65),500)
    setting.placePlate((50,60),(75,60),500)
    setting.placePlate((90,65),(90,75),800)
    setting.placePlate((85,70),(95,70),600)
    # setting.placePlate((99,75),(99,75),1000)
    

 
# Main__________________________________________________________________________

def main(): 
    cmap = cm.get_cmap(name='Reds')
    
    start1 = time.time()
    set1 = Setting(100,cmap,1.91,True)
    dome01(set1)
    set1.run()
    finished_setting1 = time.time()
    E1 = Electrons(set1)
    E1.addParticles(500)
    E1.move(1e-11,True)
    save_output(set1,E1,"C:/Users/User/Desktop/Uni/Computational/ESC201/Exercises/Ex9/DesignPrize/output_file.txt")
    finish1 = time.time()
    
    print(f"Setting: {finished_setting1-start1}")
    print(f"Calculation: {finish1-finished_setting1}")
    
    
    
if __name__== "__main__":
    main()