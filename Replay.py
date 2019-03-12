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
import numpy as np



path_to_XML = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/SymuviaOut_000000_010000_traf_SO_median.xml'
path_to_network = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml'
saving_path ='/Users/fabienduranson/Desktop/Pougne/PAr/Results/Dynamic/Replays/'

def create_blanc():
    w,h = 1800,1200
    couleur = (255,0,0)
    txt = 'Vehicule'
    im,draw = Trace_carte.basic_frame(w,h,"carre",[couleur,txt])
    im.save('Blanc.jpg','JPEG')
    return im
#    Lyon6x3 = Trace_carte.Network('Lyon mamene')
#    Lyon6x3.from_XML(path_to_network)
#    im = Image.new('RGBA',(w+600,h), (255,255,255,0))
#    draw = ImageDraw.Draw(im)
#    lim = Lyon6x3.limits()
#    l = 2
#    Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

def frame(ind,video,instant):
    im = Image.open('Blanc.jpg')
    vehs = instant['vehs']
    for veh in vehs:
        place(veh,im)
    a = np.array(im)
#    name = 'frame{}.jpg'.format(ind)
#    im.save(name,'JPEG')
#    i = cv2.imread(name)
    video.write(a)
    #os.remove(name)

def place(veh,im):
    x,y = veh['x'],veh['y']
    for i in range(-2,3):
        for j in range(-2,3):
            im.putpixel((max(0,min(x+i,1799)),max(0,min(y+j,1199))),(255,0,0))

def temps(t):
    h = t//3600
    m = (t%3600)//60
    s = t%60
    return '{} h {} min et {} secondes'.format(h,m,s)

def play(fact):     #1 = normal speed; 10 = x10 speed
    est_time = int(10+20000/fact)
    print('\nTemps de calcul estimé : ' + temps(est_time) + '\n')
    global t
    t = time.time()
    create_blanc()
    n = cv2.VideoWriter_fourcc(*'XVID')
    fps = min(24,fact)
    video = cv2.VideoWriter(saving_path+'Replay x{}.avi'.format(fact),n,fps,(1800,1200))
    print("Waiting for XML file to be decoded...  ~ 10 secondes\n")
    #instants = Save_Instants.instantsFromXML(path_to_XML)
    instants = Save_Instants.instantsFromtxt('Instants.txt')  #path_to_txt+
    for k in range(int(fps*3600/fact)):
        i = int(k*fact/fps)
        s = ("\rAvancement : {}%  //  Temps écoulé : "+temps(int(time.time()-t))).format(int(100*i/3600))
        sys.stdout.write(s)
        sys.stdout.flush()  
        sys.stdout.write("\r")
        instant = instants[i]
        frame(k,video,instant)
    cv2.destroyAllWindows()
    video.release()
    s = '\rAvancement : 100%  //  Temps de calcul réel : ' + temps(int(time.time()-t))
    sys.stdout.write(s)
    sys.stdout.flush() 
    return video