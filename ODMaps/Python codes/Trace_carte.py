#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:37:17 2018

@author: fabienduranson
"""
import csv
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import math
import wx

path_to_network = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml'

class Network:
    
    def __init__(self,name):
        self.name = name
        self.paths = []
        self.intersecs = []
    
    def add_path(self,path):
        self.paths.append(path)
        
    def add_intersec(self,intersec):
        self.intersecs.append(intersec)
        
    def colorize_by_speed(self,h,w,luminosite):
        # make a blank image for the text, initialized to transparent text color
        # h = 1440
        # w = 2048
        im = Image.new('RGBA',(w,h), (255,255,255,0))
        
        # get a drawing context
        draw = ImageDraw.Draw(im)
        
        (xmin,xmax,ymin,ymax) = self.limits()
        
        N=0
        for path in self.paths:
            N+=1
            v_moyenne = path.length/path.meanTravelTime
            v_max = 25
            alpha = v_moyenne/v_max
            if alpha < 0.5:
                color = (luminosite,int(2*alpha*luminosite),0)
            else:
                color = (int(2*(1-alpha)*luminosite),luminosite,0)
            L_test = []
            if N in L_test:
                color = (255,0,0)
            path.trace_path(draw,h,w,xmin,xmax,ymin,ymax,color)
            if N > 10000:
                break
        
        im.show()
    
    def reveal(self,draw,h,w,dims,limits,l):
        
        for path in self.paths:
            color = (0,0,0,255)
            path.trace_large_path(draw,h,w,dims,limits,color,l)
        
        for intersection in self.intersecs:
            intersection.trace_intersec(self.paths,draw,h,w,dims,limits)
        
    def from_CSV(self):
        file = open("/Users/fabienduranson/Desktop/Pougne/PAr/Lyon 6/Link.csv","r")
        links=csv.reader(file)
        
        b = True
        for raw in links:
            if b:
                b = False
            else:
                path = raw[0]
                path = path.split(';')
                points_list = []
                i = 6
                while i<len(path)-1 and len(path[i])>0:
                    x = float(path[i])
                    y = float(path[i+1])
                    new_p = (x,y)
                    points_list.append(new_p)
                    i+=2
                ID = path[1]
                nUI = path[2]
                nDI = path[3]
                length = float(path[4])
                mTT = float(path[5])
                self.add_path(Path(ID,nUI,nDI,length,1,mTT,points_list))
                
    def from_XML(self,path):
        input_xml = path
        input_tree = ET.parse(input_xml)
        input_root = input_tree.getroot()
        
        # Loading the basic information for links (troncons)
        list_link = input_tree.findall(".//RESEAU/TRONCONS/TRONCON")
        nbr_link = len(list_link) # total number of links
        
        for i in range(nbr_link):
            net_link = list_link[i].attrib
            ID = net_link['id']
            nodeUpIndice = net_link['id_eltamont']
            nodeDownIndice = net_link['id_eltaval']
            point1 = couple(net_link['extremite_amont'])
            point2 = couple(net_link['extremite_aval'])
            length = dist(point1,point2)
            width = int(net_link['largeur_voie'])#*int(net_link['nb_voie'])
            meanTimeTravel = 10 # inconnu
            self.paths.append(Path(ID,nodeUpIndice,nodeDownIndice,length,width,
                                   meanTimeTravel,[point1,point2]))
        
        list_repartiteur = input_tree.findall(".//RESEAU/CONNEXIONS/REPARTITEURS/REPARTITEUR")
        
        for repartiteur in list_repartiteur:
            net_rep = repartiteur.attrib
            inout = moves(repartiteur)
            self.add_intersec(Repartiteur(net_rep['id'],inout))
        
        list_carrefourafeux = input_tree.findall(".//RESEAU/CONNEXIONS/CARREFOURSAFEUX/CARREFOURAFEUX")
        
        for carrefourafeux in list_carrefourafeux:
            net_rep = carrefourafeux.attrib
            inout = moves(carrefourafeux)
            self.add_intersec(CaF(net_rep['id'],inout))
    
    def limits(self):
        X = [point[0] for path in self.paths for point in path.points]
        Y = [point[1] for path in self.paths for point in path.points]
        return (min(X),max(X),min(Y),max(Y))

class Path:
    
    def __init__(self,ID,nodeUpIndice,nodeDownIndice,length,width,meanTravelTime,points):
        self.ID = ID
        self.nodeUpIndice = nodeUpIndice
        self.nodeDownIndice = nodeDownIndice
        self.length = length
        self.width = width
        self.meanTravelTime = meanTravelTime
        self.points = points
    
    def trace_path(self,draw,h,w,dims,limits,color,bonus):
        for i in range(len(self.points)-1):
            xy = self.points[i]+self.points[i+1]
            xy = (xy[0]+bonus,xy[1]+bonus,xy[2]+bonus,xy[-1]+bonus)
            draw.line(scale(xy,h,w,dims,limits),fill = color)
    
    def trace_large_path(self,draw,h,w,dims,limits,color,l):
        for i in range(l):
            self.trace_path(draw,h,w,dims,limits,color,i)
            self.trace_path(draw,h,w,dims,limits,color,-i)

class Intersection:
    
    def __init__(self,ID,inout):
        self.ID = ID
        self.in_out = inout
    
        
class Repartiteur(Intersection):
    
    def __init__(self,ID,inout):
        Intersection.__init__(self,ID,inout)
    
    def trace_intersec(self,paths,draw,h,w,dims,limits):
        xmin,xmax,ymin,ymax = limits
        Xmin,Xmax,Ymin,Ymax = dims
        color = (0,0,0,255)
        for k in self.in_out:
            (inid,outids) = k
            p1 = find_by_id(inid,paths).points[-1]
            for out in outids:
                p2 = find_by_id(out,paths).points[0]
                draw.line(scale(p1+p2,h,w,dims,limits),fill = color)

class CaF(Intersection):
    
    def __init__(self,ID,inout):
        Intersection.__init__(self,ID,inout)
    
    def trace_intersec(self,paths,draw,h,w,dims,limits):
        xmin,xmax,ymin,ymax = limits
        Xmin,Xmax,Ymin,Ymax = dims
        color = (0,0,0,255)
        for k in self.in_out:
            (inid,outids) = k
            p1 = find_by_id(inid,paths).points[-1]
            for out in outids:
                p2 = find_by_id(out,paths).points[0]
                draw.line(scale(p1+p2,h,w,dims,limits),fill = color)

def scale(XY,height,width,dims,limits):
    xmin,xmax,ymin,ymax = limits
    Xmin,Xmax,Ymin,Ymax = dims
    X1,Y1,X2,Y2 = XY
    x1 = xmin + (X1-Xmin)*(xmax-xmin)/(Xmax-Xmin)
    y1 = ymax - (Y1-Ymin)*(ymax-ymin)/(Ymax-Ymin)
    x2 = xmin + (X2-Xmin)*(xmax-xmin)/(Xmax-Xmin)
    y2 = ymax - (Y2-Ymin)*(ymax-ymin)/(Ymax-Ymin)
    return (x1,y1,x2,y2)


def couple(s):
    s=separe(s,' ')
    c=(float(s[0]),float(s[1]))
    return c

def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def separe(string,char):
    split = []
    aux = ''
    for c in string:
        if c == char:
            split.append(aux)
            aux = ''
        else:
            aux+=c
    split.append(aux)
    return split

def moves(repartiteur):
    if len(repartiteur) == 0:
        return []
    ans = []
    for move in repartiteur[0]:
        inout = (move.attrib['id_troncon_amont'],[])
        for destination in move[0]:
            inout[1].append(destination.attrib['id_troncon_aval'])
        ans.append(inout)
    return ans

def find_by_id(ID,paths):
    for path in paths:
        if path.ID == ID:
            return path

def trace(draw,h,w,dims,limits,l):
    Lyon6x3 = Network('Lyon mamene')
    Lyon6x3.from_XML(path_to_network)
    Lyon6x3.reveal(draw,h,w,dims,limits,l)

