#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 14:37:33 2018

@author: fabienduranson
"""

path = '/Users/fabienduranson/Desktop/Pougne/PAr/DataForECLproject2A/SymuviaOut_000000_010000_traf_SO_median.xml'



import xml.etree.ElementTree as ET
import numpy as np

def ODMatFromXML(path):
    input_xml = path
    input_tree = ET.parse(input_xml)
    input_root = input_tree.getroot()
    
    # Loading the basic information for links (troncons)
    list_vehs = input_tree.findall(".//VEHS/VEH")
    nbr_vehs = len(list_vehs) # total number of links
    list_troncons = input_tree.findall(".//RESEAU/TRONCONS/TRONCON")
    
    #print('Importé')
    
    dList = []
    aList = []
    
    for i in range(nbr_vehs):
        veh = list_vehs[i].attrib
        if 'itineraire' in veh.keys():
            itineraire = veh['itineraire'].split()
            troncon_depart = itineraire[0]
            troncon_arrivee = itineraire[-1]
            depart_str = find_origin(troncon_depart,list_troncons).split()
            arrivee_str = find_end(troncon_arrivee,list_troncons).split()
            depart = (float(depart_str[0]),float(depart_str[1]))
            arrivee = (float(arrivee_str[0]),float(arrivee_str[1]))
            dList.append(depart)
            aList.append(arrivee)
    
    #print('Départs et arrivées ok')
    
    D = np.eye(len(dList))
    
    departs = []
    arrivees = []
    
    for d in dList:
        if d not in departs:
            departs.append(d)
    for a in aList:
        if a not in arrivees:
            arrivees.append(a)
    
    #print(len(departs))
    #print(len(arrivees))
    #print('Plus que la matrice à avoir !')
    
    ODmat = [[0 for _ in range(len(arrivees))] for _ in range(len(departs))]
    
    for depart in departs:
        for i in range(len(dList)):
            if dList[i]==depart:
                a = find_index(aList[i],arrivees)
                d = find_index(dList[i],departs)
                ODmat[d][a]+=1
    #print('Youpi !')
    return {'mat' : ODmat, 'origins' : departs, 'destinations' : arrivees}


def save(ODm,name):
    ODmat = ODm['mat']
    origins = ODm['origins']
    destinations = ODm['destinations']
    file = open(name,"w")
    for l in ODmat:
        s=""
        for e in l:
            s+=str(e)
            s+=" "
        s+="\n"
        file.write(s)
    file.write("\n")
    for o in origins:
        s = str(o[0]) + " " + str(o[1]) + "\n"
        file.write(s)
    file.write("\n")
    for d in destinations:
        s = str(d[0]) + " " + str(d[1]) + "\n"
        file.write(s)
    file.write("\n")
    file.close()

def ODMatFromTxt(name):
    file = open(name)
    f = file.readlines()
    ODm_s,origins_s,destinations_s = split_l(f)
    ODmat = []
    origins = []
    destinations = []
    for l in ODm_s:
        lp = []
        lf = l.split()
        lf.pop(-1)
        for e in lf:
            lp.append(int(e))
        ODmat.append(lp)
    for o in origins_s:
        origin = o.split()
        origins.append((float(origin[0]),float(origin[1])))
    for d in destinations_s:
        dest = d.split()
        destinations.append((float(dest[0]),float(dest[1])))
    return {'mat' : ODmat, 'origins' : origins, 'destinations' : destinations}
                

def split_l(l):
    ans = []
    ind = 0
    for i in range(len(l)):
        if l[i] == "\n":
            ans.append(l[ind:i])
            ind = i+1
    return ans

def find_origin(nom_troncon,list_troncons):
    for tr in list_troncons:
        t = tr.attrib
        if t['id'] == nom_troncon:
            return t['extremite_amont']

def find_end(nom_troncon,list_troncons):
    for tr in list_troncons:
        t=tr.attrib
        if t['id'] == nom_troncon:
            return t['extremite_aval']

def find_index(elem,l):
    for i in range(len(l)):
        if elem==l[i]:
            return i

def main():
    return ODMatFromTxt('/Users/fabienduranson/Desktop/Pougne/PAr/ODmat.txt')
    return ODMatFromXML(path)
