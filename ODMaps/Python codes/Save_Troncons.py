#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:14:38 2019

@author: fabienduranson
"""

path = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/SymuviaOut_000000_010000_traf_SO_median.xml'

import xml.etree.ElementTree as ET
import numpy as np
import time

def tronconsFromXML(path):
    input_xml = path
    input_tree = ET.parse(input_xml)
    input_root = input_tree.getroot()
    
    # Loading the basic information for links (troncons)
    list_troncons = input_tree.findall(".//RESEAU/TRONCONS/TRONCON")
    
    troncons = []
    for i in list_troncons:
        troncon = i.attrib
        identifiant = troncon['id']
        x1s,y1s = troncon['extremite_amont'].split()
        x2s,y2s = troncon['extremite_aval'].split()
        x1,y1 = int(float(x1s)),int(float(y1s))
        x2,y2 = int(float(x2s)),int(float(y2s))
        troncons.append({'id' : identifiant, 'x1' : x1, 'x2' : x2, 'y1' : y1, 'y2' : y2})
    return troncons

def save(troncons,name):         #pas encore fonctionnel, on fait sans
    file = open(name,"w")
    for tr in troncons:
        s = tr['id'] +' '+ str(tr['x1']) +' '+ str(tr['x2']) +' '+ str(tr['y1']) +' '+ str(tr['y2']) + '\n'
        file.write(s)
    file.close()

def tronconsFromtxt(path):
    file = open(path,'r')
    f = file.readlines()
    trs = []
    for i in f:
        tr = i.split()
        identifiant = tr[0]
        x1 = int(float(tr[1]))
        x2 = int(float(tr[2]))
        y1 = int(float(tr[3]))
        y2 = int(float(tr[4]))
        trs.append({'id' : identifiant, 'x1' : x1, 'x2' : x2, 'y1' : y1, 'y2' : y2})
    return trs
                
def scl(pt):
    w,h = 1800,1200
    X,Y = pt
    Xmin,Xmax,Ymin,Ymax = (842872.935922, 844593.286, 6519780.692, 6521456.1002)
    x = int((X-Xmin)/(Xmax-Xmin)*w)
    y = int((Ymax-Y)/(Ymax-Ymin)*h)
    return (x,y)


def main():
    return tronconsFromXML(path)
