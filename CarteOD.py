#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:07:52 2018

@author: fabienduranson
"""

import Trace_carte
import ExtractODMat
from PIL import Image,ImageDraw
import random

class ODMap:
    
    def __init__(self,name,n,p,ODmat):
        self.name = name
        self.front_map = OMap(n,p,[[]])
        self.matrix = ODmat
        self.reduced_matrix = [[]]
    
    def display(self):
        self.front_map.display()
        im.show()
    
    def simulate_reduced_matrix(self):
        sRm = []
        N = self.front_map.columns*self.front_map.rows
        for i in range (N):
            l = []
            for j in range (N):
                if random.random()>0.1:
                    l.append(random.randint(0,5))
                else:
                    l.append(0)
            sRm.append(l)
        self.reduced_matrix = sRm
        self.front_map.r_mat = sRm
        self.front_map.max_flow = matrix_max(sRm)
        self.front_map.create_sons()
    
    def create_reduced_matrix(self,ODm):
        ODmat = ODm['mat']
        origins = ODm['origins']
        destinations = ODm['destinations']
        N = self.front_map.columns*self.front_map.rows
        self.reduced_matrix = [[ 0 for i in range(N)] for i in range(N)]
        for o in range(len(origins)):
            for d in range(len(destinations)-1):
                i = self.find_box(origins[o])
                j = self.find_box(destinations[d])
                value = ODmat[o][d]
                self.reduced_matrix[i][j] += value
        self.front_map.r_mat = self.reduced_matrix
        self.front_map.max_flow = matrix_max(self.reduced_matrix)
        self.front_map.create_sons()
        
    def find_box(self,PT):
        (x,y) = scl(PT)
        n = self.front_map.columns
        m = self.front_map.rows
        wi = w/n
        hi = h/m
        a = x//wi
        b = y//hi
        i=int(a*m + b)
        return i
        

class OMap:
    
    def __init__(self,n,p,reduced_matrix):
        self.columns = n
        self.rows = p
        self.attribs = []
        self.is_last_depth = False
        self.r_mat = reduced_matrix
        self.max_flow = matrix_max(reduced_matrix)

    
    def create_sons(self):
        for dests in self.r_mat:
            dest_map = DMap(self.columns,self.rows,dests,self.max_flow)
            dest_map.set_colors()
            self.attribs.append(dest_map)
    
    def display(self):
        dims = (Xmin,Xmax,Ymin,Ymax)
        for j in range(self.rows):                  # problem might be here
            for i in range(self.columns):
                x1 = int(i*w/self.columns)
                x2 = int((i+1)*w/self.columns)
                y1 = int(j*h/self.rows)
                y2 = int((j+1)*h/self.rows)
                ind = i * self.rows + j
                self.attribs[ind].display(x1,x2,y1,y2)
        for j in range(self.rows):                  # problem might be here
            for i in range(self.columns):
                x1 = int(i*w/self.columns)
                x2 = int((i+1)*w/self.columns)
                y1 = int(j*h/self.rows)
                y2 = int((j+1)*h/self.rows)
                ind = i * self.rows + j
                if not is_all_blank(self.attribs[ind].attribs):
                    Trace_carte.trace(draw,h,w,dims,(x1,x2,y1,y2),1)
        Trace_carte.trace(draw,h,w,dims,(0,w,0,h),3)
        self.draw_lines()
        
    def draw_lines(self):
        wi = w/self.columns
        hi = h/self.rows
        for i in range(self.columns):
            x = i*wi
            y1 = 0
            y2 = h
            draw.line((x,y1,x,y2),fill = 'black')
            draw.line((x+1,y1,x+1,y2),fill = 'black')
            draw.line((x-1,y1,x-1,y2),fill = 'black')
        for i in range(self.rows):
            y = i*hi
            x1 = 0
            x2 = w
            draw.line((x1,y,x2,y),fill = 'black')
            draw.line((x1,y+1,x2,y+1),fill = 'black')
            draw.line((x1,y-1,x2,y-1),fill = 'black')
                

class DMap:
    
    def __init__(self,n,p,destinations,max_flow):
        self.columns = n
        self.rows = p
        self.attribs = []
        self.is_last_depth = False
        self.dests = destinations
        self.max_flow = max_flow
    
    def set_colors(self):
        for dest in self.dests:
            alpha = dest/self.max_flow
            if alpha <0.2:
                r = int((255)*alpha/0.15)
                v = 255
                b = 100
            else:
                r = 255
                v = int(255 - (255/0.85)*(alpha-0.15))
                b = 100
            self.attribs.append((r,v,b,transp))
    
    def display(self,xmin,xmax,ymin,ymax):
        #print(ymax)
        for i in range(self.columns):
            for j in range(self.rows):
                x1 = int(xmin + i*w/self.columns**2)
                x2 = int(xmin + (i+1)*w/self.columns**2)
                y1 = int(ymin + j*h/self.rows**2)
                y2 = int(ymin + (j+1)*h/self.rows**2)
                ind = i*self.rows + j
                colorize(im,x1,x2,y1,y2,self.attribs[ind])
        

def colorize(imag,xmin,xmax,ymin,ymax,color):
    for y in range(ymin,ymax):
        #print(y)
        for x in range(xmin,xmax):
            imag.putpixel((x, y), color)

def matrix_max(mat):
    m=-1e30
    for i in mat:
        for j in i:
            if j > m:
                m=j
    return m

def is_all_blank(l):
    for e in l:
        if e[:-1] != (255,255,255):
            return False
    else:
        return True

def scl(pt):
    X,Y = pt
    eps = 1
    Xmin,Xmax,Ymin,Ymax = (842872.935922 - eps, 844593.286 + eps, 6519780.692- eps, 6521456.1002+ eps)
    x = int((X-Xmin)/(Xmax-Xmin)*w)
    y = int((Ymax-Y)/(Ymax-Ymin)*h)
    return (x,y)

def main(n):
    global w
    global h
    global Xmin
    global Xmax
    global Ymin
    global Ymax
    global transp
    transp = 55
    Xmin,Xmax,Ymin,Ymax = (842872.935922, 844593.286, 6519780.692, 6521456.1002)
    w,h = (1800,1200)
    color = (255,255,255,255)
    global im
    global draw
    im = Image.new('RGBA', (w,h), color)
    draw = ImageDraw.Draw(im)
    odmap = ODMap('Bulle',n,n,[[]])
    odmap.create_reduced_matrix(ExtractODMat.main())
    # print(odmap.reduced_matrix)
    odmap.display()
    im.save('ODmap {}x{}'.format(n,n),'JPEG')







    