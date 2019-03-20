#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:54:16 2018

@author: fabienduranson
"""

path_to_network = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml'
path_to_saving_location = "/Users/fabienduranson/Desktop/Pougne/PAr/Results/Static/ligne_droite.jpg"


import Trace_carte
import ExtractODMat
from math import sqrt
from PIL import Image,ImageDraw
import random

def trace_n(draw,pt1,pt2,n):
    for _ in range(n):
        r = random.random()
        a = int(-10+10*r)
        p1,p2 = (pt1[0]+a,pt1[1]),(pt2[0]+a,pt2[1])
        draw.line(p1+p2,fill = 'red')
        #line(im,p1,p2,(255,0,0))

def line(im,p1,p2,color):
    x1,y1 = p1
    x2,y2 = p2
    N = 1000
    for i in range(N):
        x = int(x1 + i/N*(x2-x1))
        y = int(y1 + i/N*(y2-y1))
        print(x)
        if valide((x,y)):
            im.putpixel((x,y),color)

def scl(pt):
    X,Y = pt
    Xmin,Xmax,Ymin,Ymax = (842872.935922, 844593.286, 6519780.692, 6521456.1002)
    x = int((X-Xmin)/(Xmax-Xmin)*w)
    y = int((Ymax-Y)/(Ymax-Ymin)*h)
    return (x,y)

def valide(pt):
    x,y = pt
    return (0<x and x<w and 0<y and y<h)

global w
global h
w,h = 1800,1200
Lyon6x3 = Trace_carte.Network('Lyon mamene')
Lyon6x3.from_XML(path_to_network)
im = Image.new('RGBA',(w+600,h), (255,255,255,0))
draw = ImageDraw.Draw(im)
lim = Lyon6x3.limits()
l = 2
Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

ODm = ExtractODMat.ODMatFromTxt('ODmat.txt')

ODmat = ODm['mat']
origins = ODm['origins']
destinations = ODm['destinations']

for i in range(len(ODmat)):
    for j in range(len(ODmat[i])):
        pt1 = scl(origins[i])
        pt2 = scl(destinations[j])
        trace_n(draw,pt1,pt2,ODmat[i][j])

Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

im.save(path_to_saving_location,"JPEG")

im.show()
