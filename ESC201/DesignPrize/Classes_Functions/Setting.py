# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:17:04 2021

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve as conv

#i called setting or "set" the environment that is created in which electrons will be put in

class Setting():
    def __init__(self, x,cmap,omega,plotSetting=False):
        #set x dimension (same as y dimension)
        self.x = x
        #create a square matrix with x 
        self.phi = np.zeros(shape=(x,x))
        #create a kernel and a boolean array for indxing while updating
        self.kernel()
        self.conditional()
        #creat and fill omega array with the value omega, is set to 0 at locations where plates are placed in placePlate function
        self.omega = np.full((x,x),omega)
        #set a delta assuming square is 1cm by 1cm
        self.delta = 0.01/self.x
        self.cmap = cmap
        #set boolean if setting should be plotted
        self.plotSetting = plotSetting
        #create array where location of plates will be stored for final analysis
        self.plates = []
    
    # Functions__________________________________________________________________________
    
    def kernel(self):
        '''create kernel for convolution'''
        self.kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    
    def conditional(self):
        '''create boolean arrray for chess-like update'''
        self.c = np.zeros((self.x, self.x), dtype=bool)
        self.c[::2, ::2] = True
        self.c[1::2, 1::2] = True
        
    def update(self):
        '''update function gets called for each time step. Applies convolution on phi and updates using omega as weight matrix'''
        self.out = np.zeros_like(self.phi)
        conv(self.phi,self.kernel,output=self.out, mode="constant", cval=0)
        self.out *= self.omega/4
        self.phi[self.c] += self.out[self.c]        
        max1 = np.max(abs(self.out[self.c]))
        
        
        conv(self.phi,self.kernel,output=self.out, mode="constant", cval=0)
        self.out *= self.omega/4
        self.phi[~self.c] += self.out[~self.c]      
        max2 = np.max(abs(self.out[~self.c]))
          
        return max(max1,max2)

    def run(self):
        '''run function gets calles at the start and calls update functino for as many time steps as needed to get desired precision'''
        dif = self.update()
        while abs(dif) > 0.1:
            dif = np.max(self.update())
        #if desired plots setting
        if self.plotSetting:
            self.plot()
    
    def plot(self):
        '''plot the setting(phi) twice (2D density plots), once on white background so electrons are easier visible'''
        self.fig, (ax1,self.ax) = plt.subplots(1,2)      
        self.ax.set_title("Electrostatic Potential")
        cp = self.ax.imshow(self.phi,cmap=self.cmap)
        cbar = self.fig.colorbar(cp, ax=self.ax)
        
        ax1.imshow(self.phi, cmap = "plasma")
        CS = ax1.contour(self.phi, 10, colors = "black", linestyles = "dotted")
        ax1.clabel(CS, CS.levels, inline=True, fontsize=10, fmt = '%dV', colors = "black")

    def settings(self, axes):
        '''plot setting multiple times'''
        for ax in axes:
            ax.imshow(self.phi,cmap=self.cmap)
            
    def placePlate(self, p1, p2, potential):
        '''places plate from given points p1, p2 with the potential given by potential'''
        x0,y0 = p1[0], p1[1]
        x1,y1 = p2[0], p2[1]
              
        if not (0 <= x0 < self.phi.shape[0] and 0 <= x1 < self.phi.shape[0] and
                0 <= y0 < self.phi.shape[1] and 0 <= y1 < self.phi.shape[1]):
            raise ValueError('Invalid coordinates.')
            
        if (x0, y0) == (x1, y1):
            self.phi[y0, x0] = potential
            self.omega[y0, x0] = 0
            self.plates.append([(x0,y0,potential)])
            return
        # Swap axes if Y slope is smaller than X slope
        transpose = abs(x1 - x0) < abs(y1 - y0)
        if transpose:
            self.phi = self.phi.T
            self.omega = self.omega.T
            x0, y0, x1, y1 = y0, x0, y1, x1
        # Swap line direction to go left-to-right if necessary
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        # Write line ends
        self.phi[y0, x0] = potential
        self.phi[y1, x1] = potential
        self.omega[y0, x0] = 0
        self.omega[y1, x1] = 0
        # Compute intermediate coordinates using line equation
        x = np.arange(x0 + 1, x1)
        y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
        # Write intermediate coordinates
        self.phi[y, x] = potential
        self.omega[y, x] = 0
        if transpose:
            self.phi = self.phi.T
            self.omega = self.omega.T
            self.plates.append([(y0,x0),(y1,x1),potential])
        else:
            self.plates.append([(x0,y0),(x1,y1),potential])