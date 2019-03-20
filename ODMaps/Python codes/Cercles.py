#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 16:40:44 2018

@author: fabienduranson
"""

import Trace_carte
import ExtractODMat
from math import sqrt
from PIL import Image,ImageDraw,ImageFont

path_to_network = '/Users/fabienduranson/Desktop/Pougne/PAr/Data/networkLyon6.xml'
path_to_saving_location = "/Users/fabienduranson/Desktop/Pougne/PAr/Results/Static/OD-Map/circles.jpg"

def cercle(im,centre,rayon,couleur):
    w,h = im.size
    for x in range(w):
        for y in range(h):
            if x**2+y**2<rayon:
                im.putpixel((x,y),couleur)

def carre(im,centre,largeur,couleur):
    for i in range(largeur//2):
        for j in range(largeur//2):
            pt1 = (centre[0]+i,centre[1]+j)
            pt2 = (centre[0]-i,centre[1]+j)
            pt3 = (centre[0]+i,centre[1]-j)
            pt4 = (centre[0]-i,centre[1]-j)
            pts = (pt1,pt2,pt3,pt4)
            for pt in pts:
                if valide(pt):
                    im.putpixel(pt,couleur)

def circle(im, centre, rayon, couleur):
    x0y0 = (centre[0]-rayon/2,centre[1]-rayon/2)
    x1y1 = (centre[0]+rayon/2,centre[1]+rayon/2)
    draw.ellipse(x0y0+x1y1, fill = couleur)

def rayon(i,m):
    return int(3*sqrt(i))+3

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
#Lyon6x3 = Trace_carte.Network('Lyon mamene')
#Lyon6x3.from_XML(path_to_network)
#im = Image.new('RGBA',(w+600,h), (255,255,255,0))
#draw = ImageDraw.Draw(im)
#lim = Lyon6x3.limits()
#l = 2
#Trace_carte.trace(draw,h,w,lim,(0,w,0,h),l)

im,draw = basic_frame(w,h,"circles",[])

ODm = ExtractODMat.ODMatFromTxt('ODmat.txt')

ODmat = ODm['mat']
origins = ODm['origins']
destinations = ODm['destinations']

nbr_origin = []
nbr_dest = []


for i in range(len(ODmat)):
    nbr_origin.append((sum(ODmat[i]),origins[i]))
for i in range(len(ODmat[0])):
    d = [ODmat[j][i] for j in range(len(ODmat))]
    nbr_dest.append((sum(d),destinations[i]))


max_o = max([i[0] for i in nbr_origin])
max_d = max([i[0] for i in nbr_dest])

for ori in nbr_origin:
    n,Centre = ori
    centre = scl(Centre)
    r = rayon(n,max_o)
    couleur = (0,0,255)
    circle(im,centre,r,couleur)

for dest in nbr_dest:
    n,Centre = dest
    centre = scl(Centre)
    r = rayon(n,max_d)
    couleur = (255,0,0)
    circle(im,centre,r,couleur)
    
#Legende

#c1 = (int(2/3*w),int(1/15*h))
#c2 = (int(2/3*w),int(2/15*h))
#size = int(w/36)
#p1 = (int(2/3*w)+int(1/30*w),int(1/15*h)-int(size/2))
#p2 = (int(2/3*w)+int(1/30*w),int(2/15*h)-int(size/2))
#r = rayon(max_o/2,max_o)
#circle(im,c1,r,(0,0,255))
#circle(im,c2,r,(255,0,0))
#font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size = size)
#txt1 = 'Origins'
#txt2 = 'Destinations'
#draw.text( p1, txt1,font = font, fill = (0,0,0))
#draw.text( p2, txt2, font = font, fill = (0,0,0))
#l1 = (int(2/3*w)-int(r),int(1/15*h)-int(r))
#l2 = (int(7/8*w),int(1/15*h)-int(r))
#l3 = (int(7/8*w),int(2/15*h)+int(r))
#l4 = (int(2/3*w)-int(r),int(2/15*h)+int(r))
#draw.line(l1+l2, fill = 128 , width = 5)
#draw.line(l2+l3, fill = 128 , width = 5)
#draw.line(l3+l4, fill = 128 , width = 5)
#draw.line(l4+l1, fill = 128 , width = 5)

im.save(path_to_saving_location,"JPEG")
im.show()
    
