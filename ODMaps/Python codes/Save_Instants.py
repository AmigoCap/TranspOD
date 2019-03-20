#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 15:31:49 2019

@author: fabienduranson
"""

path = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/SymuviaOut_000000_010000_traf_SO_median.xml'



import xml.etree.ElementTree as ET
import numpy as np
import time

def instantsFromXML(path):
    input_xml = path
    input_tree = ET.parse(input_xml)
    input_root = input_tree.getroot()
    
    # Loading the basic information for links (troncons)
    list_instants = input_tree.findall(".//SIMULATION/INSTANTS/INST")
    temps = len(list_instants)
    
    #print('Importé')
    
    instants = []
    for i in list_instants:
        inst = i.attrib
        identifiant = int(float(inst['val']))
        l = []
        vehs = i.getchildren()[2].getchildren()
        for veh in vehs:
            vehicule = veh.attrib
            ident = float(vehicule['id'])
            x,y = scl((float(vehicule['abs']),float(vehicule['ord'])))
            v = float(vehicule['vit'])
            tronc = vehicule['tron']
            l.append({'id' : ident, 'x' : x, 'y' : y, 'tron' : tronc, 'vit' : v})
        instants.append({'id' : identifiant, 'vehs' : l})
    return instants


def save(instants,name):         #pas encore fonctionnel, on fait sans
    file = open(name,"w")
    for inst in instants:
        s = str(inst['id']) + ' '
        for ve in inst['vehs']:
            s += str(ve['id'])+';'+str(ve['x'])+';'+str(ve['y'])+';'+ve['tron']+';'+str(ve['vit'])
            s += ','
        file.write(s)
        file.write("\n")
    file.close()

def instantsFromtxt(path):
    file = open(path,'r')
    insts = file.readlines()
    instants = []
    for i in insts:
        instant = i.split(' ')
        identifiant = int(float(instant[0]))
        l=[]
        if instant[1] != '\n':
            vehs = instant[1].split(',')
            vehs.pop(-1)
            for v in vehs:
                veh = v.split(';')
                ident,x,y,tronc,v = veh
                l.append({'id' : ident, 'x' : int(float(x)), 'y' : int(float(y)), 'tron' : tronc, 'vit' : int(float(v))})
        instants.append({'id' : identifiant, 'vehs' : l})
    return instants


                
def scl(pt):
    w,h = 1800,1200
    X,Y = pt
    Xmin,Xmax,Ymin,Ymax = (842872.935922, 844593.286, 6519780.692, 6521456.1002)
    x = int((X-Xmin)/(Xmax-Xmin)*w)
    y = int((Ymax-Y)/(Ymax-Ymin)*h)
    return (x,y)


def main():
    return instantsFromXML(path)
