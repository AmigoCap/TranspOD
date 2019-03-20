#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 17:01:57 2019

@author: fabienduranson
"""

import Trace_carte
import ExtractODMat
from math import sqrt
from PIL import Image,ImageDraw
import xml.etree.ElementTree as ET
import random

path = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/SymuviaOut_000000_010000_traf_SO_median.xml'

def TrajListFromXML(path):
    input_xml = path
    input_tree = ET.parse(input_xml)
    input_root = input_tree.getroot()
    
    # Loading the basic information for links (troncons)
    list_vehs = input_tree.findall(".//VEHS/VEH")
    nbr_vehs = len(list_vehs) # total number of links
    list_troncons = input_tree.findall(".//RESEAU/TRONCONS/TRONCON")
    
    L = []
    
    for i in range(nbr_vehs):
        veh = list_vehs[i].attrib
        l=[]
        if 'itineraire' in veh.keys():
            itineraire = veh['itineraire'].split()
            for tr in itineraire:
                depart_str = find_origin(tr,list_troncons).split()
                arrivee_str = find_end(tr,list_troncons).split()
                depart = (float(depart_str[0]),float(depart_str[1]))
                arrivee = (float(arrivee_str[0]),float(arrivee_str[1]))
                l.append((depart,arrivee))
        L.append(l)
    return L

def trace_n(draw,pt1,pt2,n):
    for _ in range(n):
        r = random.random()
        a = int(-10+10*r)
        p1,p2 = (pt1[0]+a,pt1[1]),(pt2[0]+a,pt2[1])
        draw.line(p1+p2,fill = 'red')
        #line(im,p1,p2,(255,0,0))

def trace(draw,pt1,pt2):
    r1 = random.random()
    a = int(-10+10*r1)
    r2 = random.random()
    b = int(-10+10*r2)
    p1,p2 = (pt1[0]+a,pt1[1]+b),(pt2[0]+a,pt2[1]+b)
    draw.line(p1+p2,fill = 'red')

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
Lyon6x3.from_XML('/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml')
im = Image.new('RGBA',(w,h), (255,255,255,0))
draw = ImageDraw.Draw(im)
lim = Lyon6x3.limits()
l = 2
Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

trajList = TrajListFromXML(path)

for traj in trajList:
    for trons in traj:
        pt1 = scl(trons[0])
        pt2 = scl(trons[1])
        trace(draw,pt1,pt2)

Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

im.save("/Users/fabienduranson/Desktop/Pougne/PAr/Resulsts/Static/voies.jpg","JPEG")

im.show()
