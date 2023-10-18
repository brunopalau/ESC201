# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:20:01 2021

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt


e_me = -1.76e11

class Electrons():
    
    def __init__(self,Set):
        #location of single electrons
        self.loc = []
        #velocity of electrons (vx,vy)
        self.v = []
        #"set" is the space and its calculated potential
        self.set = Set
        #list used for stats at the end
        self.stats = []
        
    def addParticles(self,n):
        '''adds prticle at random position between 10,40(upper left corner) and with a random angle between -pi/2 and pi/2'''
        #save the amount of electrons inserted. Save where which electron started and at what angle for evaluation at the end
        self.total_e = n
        self.start_y = []
        self.angle = []
        for i in range(n):
            angle = np.random.uniform(-np.pi/2,np.pi/2)
            y = np.random.randint(0.1*self.set.x,0.4*self.set.x)
            self.loc.append([0,y])
            self.v.append([1e6 * np.cos(angle), 1e6 * np.sin(angle)])
            self.angle.append(angle*180/np.pi)
            self.start_y.append(y)
        self.loc = np.array(self.loc, dtype=float)
        self.v = np.array(self.v, dtype=float)
        #create a boolean array which indicates which electrons are still "valid", meaning still inside the "box"
        self.valid = np.full(self.loc.shape[0],True)
        #count the time steps each electron has gone through.
        #Safety measure so program doesnt run infinitely if electron gets stuck oscillating
        self.count = np.zeros_like(self.valid, dtype=int)
        self.start_y=np.array(self.start_y)
        self.angle= np.array(self.angle)
        
            
    def addParticle(self,x,y,angle):
        '''adds a single electron with given position and angle, only for testing purposes'''
        self.loc.append([x,y])
        self.v.append([1e6 * np.cos(angle), 1e6 * np.sin(angle)])
        self.loc = np.array(self.loc, dtype=float)
        self.v = np.array(self.v, dtype=float)
        self.valid = np.full(self.loc.shape[0],True)
        
    def move(self,h,plotElectrons=False):
        '''calculates new position of each electron based on acceleration calculated by accel()'''
        #optional to not plot electrons (safes time)
        self.plotElectrons = plotElectrons
        #creat a list to store path of electrons that dont hit detector
        if plotElectrons and self.set.plotSetting:
            self.store = [[] for _ in range(self.total_e)]
        
        #electrons can only be plotted if setting is plotted
        elif not self.set.plotSetting and plotElectrons:
            plotElectrons = False
            print("needs setting to plot Electrons")
        #step size h
        self.h = h
        #cond takes into account the step size and adjusts accordingly at how many locations samples should be taken,
        #for diagnostic electron plotting at the end
        cond = 10**(abs(np.log10(self.h))-9)+1
        count = 0
        #rund while there are still valid electrons
        while np.any(self.valid):
            self.loc[self.valid] = self.loc[self.valid] + h*0.5 * self.v[self.valid] #first drift
            self.inside() #check which electrons still valid
            a = self.accel() #calculate acceleration on new position
            if len(a) == 0:
                print("No valid electrons left")
                break
            self.v[self.valid] = self.v[self.valid] + h*a #kick         
            self.loc[self.valid] = self.loc[self.valid] + h*0.5 * self.v[self.valid] #second drift
            self.inside() #once again check valid electrons
            
            #keep count of iterations so it doesnt end up being an endless loop due to electrons oscillating
            self.count[self.valid]+=1
            #adjust number of store according to step size
            if plotElectrons and count%cond==0:
                for i, loc in enumerate(self.loc):
                    #store location of electrons
                    self.store[i].append(np.copy(loc))
            count+=1
        #call detector to plot results
        self.detector()
    
    def accel(self):
        '''calculate acceleration in respect to potential (given by phi of the setting)'''
        a = []
        #if no valid electrons left we return empty list
        if len(self.loc[self.valid]) <= 0:
            return []
        #calculate acceleration of all valid electrons left
        j,l = np.array(np.floor(self.loc[self.valid])[:,0],dtype=int), np.array(np.floor(self.loc[self.valid][:,1]),dtype=int)
        t,u = self.loc[self.valid][:,0]-j, self.loc[self.valid][:,1]-l
        
        U1 = self.set.phi[l,j]
        U2 = self.set.phi[l,j+1]
        U3 = self.set.phi[l+1,j]
        U4 = self.set.phi[l+1,j+1]
        interpolation_x = (1-u)*(U2 - U1) + u*(U4 - U3)
        interpolation_y = (1-t)*(U3 - U1) + t*(U4 - U2)
        
        ax = -e_me*interpolation_x/self.set.delta
        ay = -e_me*interpolation_y/self.set.delta
        
        a = np.column_stack((ax,ay))
        return a

        
    
    def inside(self):
        '''update which electrons are still valid and store it in self.valid'''
        #if outside x boundaries
        b = self.loc[:,0] <  0
        b2 = self.loc[:,0] >= self.set.x-1
        self.valid[b | b2] = False
        
        #if outside y boundaries
        c = self.loc[:,1] <  0
        c2 = self.loc[:,1] >= self.set.x-1
        self.valid[c | c2] = False
        
        #if already updating for 1mio steps
        d = self.count > 1000000
        self.valid[d] = False
        
    def detector(self):
        '''calculate and plot all final results'''
        #stats contains all gathered information of the simulation to be safed in the outputfile if desired
        self.stats = []
        #boolean array for all electrons that didnt hit a wall
        self.still_inside = (self.loc[:,0]>=0) & (self.loc[:,0]<self.set.x-1) & (self.loc[:,1] >= 0) & (self.loc[:,1] < self.set.x-1)
        self.e_still_inside = self.loc[self.still_inside]
        #boolean array for all electrons that his detector
        self.on_detector = (self.loc[:,0]>=self.set.x-1) & (self.loc[:,1]>=self.set.x*0.6) & (self.loc[:,1]<=self.set.x*0.9)
        self.e_on_detector = self.loc[self.on_detector]
        #count electrons that hit wall and those who didnt
        self.num_inside = len(self.e_still_inside)
        self.num_hit_wall = self.total_e - self.num_inside
        #calculate time electrons where flying
        self.time = self.count * self.h * 1e6 #tof in ms
        
        #plot the counts on all walls
        fig, ((u,r),(l,d)) = plt.subplots(2,2)
        self.right = self.right_side(r)
        self.left = self.left_side(l)
        self.up = self.up_side(u)
        self.down = self.down_side(d)
        fig.suptitle(f"Count of electrons hitting the side walls. Total e = {self.total_e}, hit the wall = {self.num_hit_wall}, did not hit wall = {self.num_inside}")
            
        #boolean array for electrons that hit right side but didnt hit the detector
        self.not_on_detector = (self.on_detector == False) & (self.right)
        self.e_not_on_detector = self.loc[self.not_on_detector]
        
        if self.plotElectrons:
            #plot the the path of the electrons that didnt hit our detector, maximal 5 for each wall (otherwise too crowded)
            self.store = np.array(self.store)
            fig, ((up,right),(left,down),(inside,angles_start)) = plt.subplots(3,2)
            self.set.settings((up,right,left,down,inside))
            self.path_right(right)
            self.path_left(left)
            self.path_up(up)
            self.path_down(down)
            self.path_inside_and_angles(inside,angles_start)

        #plot all information that would be gatered by detector
        self.plot_detector()

        
    def plot_detector(self):
        '''plots the distribution of electrons hitting right side(so detector included) aswell as tof for electrons hitting right side
        with some statistical numbers trying to visualize the results'''
        
        fig, (self.ax1,self.ax2) = plt.subplots(1,2)
        fig.suptitle(f"Detector ([{self.set.x*0.6},{self.set.x*0.9}])")
        
        #distribution of electrons hitting right side
        self.ax1.set_title("Distribution on right side")
        self.ax1_c = self.ax1.twinx()
        self.ax1.hist(x=(self.e_on_detector[:,1],self.e_not_on_detector[:,1]),color=("red","blue"), bins=100, width=1)
        y1, y2 = self.ax1.get_ylim()
        x1, x2 = self.ax1.get_xlim()
        self.ax1_c.set_ylim(0, (y2/self.total_e)) 
        self.ax1.set_ylabel("Count")
        self.ax1_c.set_ylabel("Probability")
        self.ax1.set_xlabel("Y coordinates on right wall")
        self.ax1.text(x1+(x2-x1)/5,y2-(y2-y1)/5,f"Electrons hitting detector:\n {len(self.e_on_detector)} ({round((len(self.e_on_detector)/self.total_e)*100,2)}%)",bbox=dict(facecolor='w'))
        
        #tof
        self.ax2.hist(x=(self.time[self.on_detector],self.time[self.not_on_detector]),color=("red","blue"),bins=50)
        self.ax2.set_title("TOF")
        self.ax2.set_ylabel("count")
        self.ax2.set_xlabel("time of flight [ms]")
        #catch error if empty array
        try:
            maxi = round(np.max(self.time[self.on_detector]),2)
            mini = round(np.min(self.time[self.on_detector]),2)
            mean = round(np.mean(self.time[self.on_detector]),2)
            mean_overall = round(np.mean(self.time),2)
        except:
            maxi = 0
            mini = 0
            mean = 0
            mean_overall = 0
            
        #tof
        self.tof = f"{maxi},{mini},{mean},{mean_overall}"
        y1, y2 = self.ax2.get_ylim()
        x1, x2 = self.ax2.get_xlim()
        self.ax2.text(x1+0.2*(x2-x1),y2-((y2-y1)/5),f"max(of detected e): {maxi}\nmin(of detected e): {mini}\nmean(of detected e): {mean}\nmean(overall): {mean_overall}",bbox=dict(facecolor='w'))
        

        

    def right_side(self, r):
        '''plot histogram of right side representing where electrons hit the wall'''
        right = self.loc[:,0] >= self.set.x-1
        r.set_box_aspect(1)
        r.set_xlim([self.total_e,0])
        n, bins, patches = r.hist(self.loc[right][:,1], bins = 50, range=(0,self.set.x), color="blue", orientation=u"horizontal")

        r.invert_yaxis()
        r.yaxis.tick_right()
        k = np.arange(int(50*0.6),int(50*0.9),1)
        for i in k:
            patches[i].set_fc('r')
        r.set_title("Right Boundary Count")
        self.stats.append(f"{len(self.e_on_detector)} ({round((len(self.e_on_detector)/self.total_e)*100,2)}%)")
        self.stats.append(f"{len(self.loc[right])} ({round((len(self.loc[right])/self.total_e)*100,2)}%)")
        r.text(self.total_e-self.total_e/10,r.get_ylim()[0]/3,f"Electrons hitting right wall: {len(self.loc[right])} ({round((len(self.loc[right])/self.total_e)*100,2)}%)\nElectrons hitting detector:\n {len(self.e_on_detector)} ({round((len(self.e_on_detector)/self.total_e)*100,2)}%)",bbox=dict(facecolor='w'))
        return right
    
    def left_side(self,l):
        '''plot histogram of left side representing where electrons hit the wall'''
        left = self.loc[:,0] < 0
        l.set_box_aspect(1)
        l.set_ylim([0,self.set.x])
        l.set_xlim([0,self.total_e])
        l.hist(self.loc[left][:,1], bins = 50, color="blue", orientation="horizontal")
        l.invert_yaxis()
        l.set_title("Left Boundary Count")
        self.stats.append(f"{len(self.loc[left])} ({round((len(self.loc[left])/self.total_e)*100,2)}%)")
        l.text(self.total_e-self.total_e/3,2*l.get_ylim()[0]/3,f"Electrons hitting left wall:\n {len(self.loc[left])} ({round((len(self.loc[left])/self.total_e)*100,2)}%)",bbox=dict(facecolor='w'))
        return left
    
    def up_side(self,u):   
        '''plot histogram of upper side representing where electrons hit the wall'''
        up = self.loc[:,1] < 0
        u.set_ylim([self.total_e,0])
        u.set_box_aspect(1)
        u.hist(self.loc[up][:,0], bins = 50, range=(0,self.set.x), color="blue",width=1)
        u.xaxis.tick_top()
        u.set_title("Up Boundary Count")
        self.stats.append(f"{len(self.loc[up])} ({round((len(self.loc[up])/self.total_e)*100,2)}%)")
        u.text(self.set.x/5,3*self.total_e/5,f"Electrons hitting upper wall:\n {len(self.loc[up])} ({round((len(self.loc[up])/self.total_e)*100,2)}%)",bbox=dict(facecolor='w'))
        return up
    
    def down_side(self,d):
        '''plot histogram of lower side representing where electrons hit the wall'''
        down = self.loc[:,1] >= self.set.x-1        
        d.set_box_aspect(1)
        d.set_ylim([0,self.total_e])
        d.hist(self.loc[down][:,0], bins = 50, range=(0,self.set.x), color="blue",width=1)
        d.set_title("Down Boundary Count")
        self.stats.append(f"{len(self.loc[down])} ({round((len(self.loc[down])/self.total_e)*100,2)}%)")
        d.text(self.set.x/5,3*self.total_e/5,f"Electrons hitting lower wall:\n {len(self.loc[down])} ({round((len(self.loc[down])/self.total_e)*100,2)}%)",bbox=dict(facecolor='w'))
        return down
    
    
    def path_right(self,right):
        '''plot the path electrons took on their way to hit right wall'''
        #limit to 5 electrons otherwise too crowded
        right.set_title(f"Path electrons hitting right Wall {len(self.loc[self.not_on_detector])} ({round((len(self.loc[self.not_on_detector])/self.total_e)*100,2)}%)")
        right.scatter(self.store[self.not_on_detector,:,0][:5],self.store[self.not_on_detector,:,1][:5], color = "black", s=2)
    
    def path_left(self,left):
        '''plot the path electrons took on their way to hit left wall'''
        #limit to 5 electrons otherwise too crowded
        left.set_title(f"Path electrons hitting left Wall {len(self.loc[self.left])} ({round((len(self.loc[self.left])/self.total_e)*100,2)}%)")
        left.scatter(self.store[self.left,:,0][:5],self.store[self.left,:,1][:5], color = "blue", s=2)
        
    def path_up(self,up):
        '''plot the path electrons took on their way to hit upper wall'''
        #limit to 5 electrons otherwise too crowded
        up.set_title(f"Path electrons hitting upper Wall {len(self.loc[self.up])} ({round((len(self.loc[self.up])/self.total_e)*100,2)}%)")
        up.scatter(self.store[self.up,:,0][:5],self.store[self.up,:,1][:5], color = "orange", s=2)
        
    def path_down(self,down):
        '''plot the path electrons took on their way to hit lower wall'''
        #limit to 5 electrons otherwise too crowded
        down.set_title(f"Path electrons hitting lower Wall {len(self.loc[self.down])} ({round((len(self.loc[self.down])/self.total_e)*100,2)}%)")
        down.scatter(self.store[self.down,:,0][:5],self.store[self.down,:,1][:5], color = "violet", s=2)
        
    def path_inside_and_angles(self,inside,angles):
        '''plotting of angle to y-coord at start colored according to final state(which wall was hit) to see if there is any correlation
        or specific region which is not being taking care of'''
        inside.set_title(f"Path electrons hitting no Wall {len(self.loc[self.still_inside])} ({round((len(self.loc[self.still_inside])/self.total_e)*100,2)}%)")
        inside.scatter(self.store[self.still_inside,:,0][:5],self.store[self.still_inside,:,1][:5], color = "green", s=2)
        
        angles.scatter(self.angle[self.not_on_detector],self.start_y[self.not_on_detector],color="black",label="right Wall")
        angles.scatter(self.angle[self.left],self.start_y[self.left],color="blue",label="left Wall")
        angles.scatter(self.angle[self.up],self.start_y[self.up],color="orange",label="upper Wall")
        angles.scatter(self.angle[self.down],self.start_y[self.down],color="violet",label="lower Wall")
        angles.scatter(self.angle[self.still_inside],self.start_y[self.still_inside],color="green",label="still inside")
        angles.set_title("Start condition")
        angles.set_ylabel("Y coordinate")
        angles.set_ylim(9,41)
        angles.set_ylim(angles.get_ylim()[::-1])
        angles.set_xlabel("angle to x axis")
        angles.set_xlim(-91,91)
        plt.legend()
