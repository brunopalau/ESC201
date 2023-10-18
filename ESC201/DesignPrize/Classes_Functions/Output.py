# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 07:36:47 2021

@author: User
"""

import os

def find_results(text, function):
    '''finds the percentage of electrons hitting the detector for a specific function'''
    text = text[text.find(function):]
    text = text[text.find("stats"):]
    text = text[text.find("("):]
    stat = float(text[1:text.find("%")])
    return stat
    

def save_output(setting,ele,path,overwrite=False,comment=None):
    '''saves results in a .txt file of a specific simulation given by the setting and the electrons ele.
    If the used fucntion to set starting state has not been safed a new entry is created, otherwise the better of the two is safed.
    Optional overwrite can be set to true, in which case the already existing entry is overwritten'''
    #only change if not already existent or better
    text_new = ""
    header = f"<{setting.boundary_function}:\n"
    if not os.path.exists(path):
        raise Warning("Wrong path file: no file found")
    with open(path, "r") as text:
        text = text.read()
    
    
    text_new += header
    text_new += f"conditions: {ele.total_e}, {ele.h}"
    text_new += f", plates: {len(setting.plates)}"
    for plate in setting.plates:
        text_new+=f" {plate}"
    text_new+="\n"
    text_new+= "stats:\n"
    text_new += f"\t{ele.stats}\n\t"
    text_new += ele.tof+" [ms]"
    #if a comment is given it is included in the entry
    try:
        if setting.comment:
            text_new+=f"\ncomment: {setting.comment}"
    except:
        pass
    text_new+=">\n\n"
    #if the used starting conditions has no entry
    if text.find(header) == -1:
        with open(path, "w") as f_out:
            f_out.write(text+text_new)
        #if there already exist an entry but it had worse results or it should be overwritten
    elif find_results(text_new,setting.boundary_function) >= find_results(text,setting.boundary_function) or overwrite:
        start = text.find(header)
        end = start + text[start:].find(">") +3
        text = text[:start] + text_new + text[end:]
        with open(path, "w") as f_out:
            f_out.write(text)
    else:
        print("results worse")
    return text_new
    
def compare_output():
    
    pass



'''
boundary_function_name:
conditions: totale_e, step_size, plate placement,
stats:
 	detector(percent), right(percent), down(percent),left(percent),up(percent)
 	tof: max,min,mean,mean_overall

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<tweezer01:
conditions: 500, 1e-11, plates: 3 [(15, 40), (99, 75), 500] [(15, 10), (99, 75), 500] [(15, 10), (15, 40), 200]
stats:
	['466 (93.2%)', '469 (93.8%)', '18 (3.6%)', '10 (2.0%)', '3 (0.6%)']
	5.62,0.1,0.84,0.86 [ms]
comment: Improved Version: Used different lengths and differnet potential, but if potential too strong it pulls electrons back(still 7%).
Not having a verical plate connecting both tips lead to many electrons going up or down>

<tweezer01_neg_plate:
conditions: 500, 1e-11, plates: 4 [(5, 35), (99, 75), 500] [(5, 15), (99, 75), 500] [(1, 55), (80, 99), -200] [(5, 5), (99, 20), -200]
stats:
	['440 (88.0%)', '440 (88.0%)', '44 (8.8%)', '0 (0.0%)', '0 (0.0%)']
	9.73,0.09,0.94,1.27 [ms]
comment: Negativ plates lead to more oscillation>

<tweezer01_pos_plate:
conditions: 500, 1e-10, plates: 3 [(5, 35), (93, 75), 500] [(5, 15), (93, 75), 500] [(99, 70), (99, 80), 800]
stats:
	['428 (85.6%)', '428 (85.6%)', '72 (14.4%)', '0 (0.0%)', '0 (0.0%)']
	20.34,0.09,0.65,0.69 [ms]>

<dome01:
conditions: 500, 1e-11, plates: 6 [(10, 20), (35, 45), 300] [(10, 40), (35, 40), 300] [(70, 50), (70, 65), 500] [(50, 60), (75, 60), 500] [(90, 65), (90, 75), 800] [(85, 70), (95, 70), 600]
stats:
	['366 (73.2%)', '416 (83.2%)', '29 (5.8%)', '0 (0.0%)', '48 (9.6%)']
	8.58,0.13,0.98,1.3 [ms]
comment: a lot of uncontrolled oscillation>
'''