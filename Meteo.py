#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 00:10:36 2019

@author: fabienduranson
"""
#from __future__ import print_function
import sys
import Trace_carte
import Save_Instants
import cv2
from PIL import Image, ImageDraw
import time
import os
from math import exp,sqrt,cos,sin
import numpy as np



path_to_XML = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/SymuviaOut_000000_010000_traf_SO_median.xml'
path_to_network = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml'
saving_path ='/Users/fabienduranson/Desktop/Pougne/PAr/Results/Dynamic/Replays/'
path_to_txt = '/Users/fabienduranson/Desktop/Pougne/PAr/Dynamic_visualisation/'

def create_blanc():
    w,h = 1800,1200
    couleur1, couleur2 = (255,0,0),(0,0,255)
    txt1,txt2 = "oui","non"
    im,draw = Trace_carte.basic_frame(w,h,"vertical scale",[couleur1,couleur2,txt1,txt2])
    im.save('Blanc.jpg','JPEG')
    return im

def frame(ind,video,instant):
    w,h = 1800,1200
    im = Image.open('Blanc.jpg')
    vehs = instant['vehs']
    for x in range(w):
        for y in range(h):
            colore(x,y,vehs,im)
    name = 'frame{}.jpg'.format(ind)
    im.save(name,'JPEG')
    video.write(cv2.imread(name))
    os.remove(name)

def frame2(ind,video,instant):
    w,h = 1800,1200
    im = Image.open('Blanc.jpg')
    vehs = instant['vehs']
    T = [[ 0 for _ in range(h)] for _ in range(w)]
    for veh in vehs:
        chaleur(veh,T)
    Tmax = max(max(T))
    if Tmax!=0:
        for x in range(w):
            for y in range(h):
                colore2(T,x,y,Tmax,im)
    video.write(np.array(im))
    Trace_carte.trace(ImageDraw.Draw(im),h,w,(0,w,0,h),(0,w,0,h),2)

def chaleur(veh,T):
    w,h = 1800,1200
    x,y = veh['x'],veh['y']
    limite = 100
    d = 60
    for i in range(limite):
        for theta in range(4*(i+1)):
            xn = int(x + i*cos(theta))
            yn = int(y + i*sin(theta))
            if xn<w and xn>=0 and yn<h and yn>=0:
                T[xn][yn] += exp(-i/d)

def colore(x,y,vehs,im):
    ftxy = ft(x,y,vehs)
    f0 = 70
    a = ftxy/f0
    if a < 1/2:
        color = (255,int(255*2*a),int(255*2*a))
    else:
        color = (int(255*2*(1-a)),255*2*int((1-a)),255)
    im.putpixel((x,y),color)

def colore2(T,x,y,Tmax,im):
    a = 1 - T[x][y]/Tmax
    if a < 1/2:
        color = (255,int(255*2*a),int(255*2*a))
    else:
        color = (int(255*2*(1-a)),255*2*int((1-a)),255)
    im.putpixel((x,y),color)

def ft(x,y,vehs):
    alpha = 1/50
    S = 0
    for veh in vehs:
        d = sqrt((x-veh['x'])**2 + (y-veh['y'])**2)
        S += exp(-alpha*d)
    return S

def temps(t):
    h = t//3600
    m = (t%3600)//60
    s = t%60
    return '{} h {} min et {} secondes'.format(h,m,s)

def meteo(fact):     #1 = normal speed; 10 = x10 speed
    est_time = int(10+20000/fact)
    print('\nTemps de calcul estimé : ' + temps(est_time) + '\n')
    global t
    t = time.time()
    create_blanc()
    n = cv2.VideoWriter_fourcc(*'XVID')
    fps = min(24,fact)
    video = cv2.VideoWriter(saving_path+'Meteo x{}.avi'.format(fact),n,fps,(1800,1200))
    print("Waiting for XML file to be decoded...  ~ 10 secondes\n")
    #instants = Save_Instants.instantsFromXML(path_to_XML)
    instants = Save_Instants.instantsFromtxt(path_to_txt+'Instants.txt')
    for k in range(int(fps*3600/fact)):
        i = int(k*fact/fps)
        s = ("\rAvancement : {}%  //  Temps écoulé : "+temps(int(time.time()-t))).format(int(100*i/3600))
        sys.stdout.write(s)
        sys.stdout.flush()  
        sys.stdout.write("\r")
        instant = instants[i]
        frame2(k,video,instant)
    cv2.destroyAllWindows()
    video.release()
    s = '\rAvancement : 100%  //  Temps de calcul réel : ' + temps(int(time.time()-t))
    sys.stdout.write(s)
    sys.stdout.flush() 
    return video