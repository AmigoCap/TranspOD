# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:52:13 2018

@author: Clement
"""


import csv
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import math
import numpy as np
from pylab import *

path='C:/Users/Clement/Desktop/PAr/Instants.txt'

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


# [i1, i2, ...]
# ik = {id:seconde, vehs:[veh1, veh2, ...]}
# vehi = {id:attrib, x:abs, y:ord, tronc:tronc, v:v}



def Hilbert_v2(n) :

	def sym(A) :
		B = np.copy(A)
		n = len(A)
		for i in range(n) :
			for j in range(n) :
				B[i][j] = A[n-j-1][n-i-1]
		return B

	def anti_sym(A) :
		B = np.copy(A)
		n = len(A)
		for i in range(n) :
			for j in range(n) :
				B[i][j] = A[j][i]
		return B

	if n == 0 :
		return np.array([[0]])
	if n == 1 :
		return np.array([[0,3],[1,2]])
	else :
		H = Hilbert_v2(n-1)
		H0 = anti_sym(np.copy(H))
		H1 = int(4**n/4)+np.copy(H)
		H2 = int(2*4**n/4)+np.copy(H)
		H3 = int(3*4**n/4)+sym(np.copy(H))
		return (np.concatenate((np.concatenate((H0,H1)),np.concatenate((H3,H2))),axis=1))


def MotionRugs( instants , n) :
	imin = 0
	while len(instants[imin]["vehs"])==0 :
		imin +=1
	xmin = instants[imin]["vehs"][0]["x"]
	xmax = instants[imin]["vehs"][0]["x"]
	ymin = instants[imin]["vehs"][0]["y"]
	ymax = instants[imin]["vehs"][0]["y"]

	for inst in instants[imin+1:] :
		for veh in inst["vehs"] :
			if veh["x"] < xmin :
				xmin = veh["x"]
			if veh["x"] > xmax :
				xmax = veh["x"]
			if veh["y"] < ymin :
				ymin = veh["y"]
			if veh["y"] > ymax :
				ymax = veh["x"]

	h = ymax-ymin
	w = xmax-xmin

	H = Hilbert_v2(n)

	M = np.zeros((4**n,len(instants)))

	for inst in instants[4:] :
		for veh in inst["vehs"] :
			M[ H[ min(2**n-1,int((veh["y"]-ymin)*n**2/h)) ][ min(2**n-1,int((veh["x"]-xmin)*n**2/w)) ] ][inst["id"]-1] += 1

	return M

instants = instantsFromtxt(path)

M = MotionRugs(instants[:100], 3 )

def post_traitement( M ) :
    i = 0
    while i < len(M) :
        if np.max(M[i]) == 0 :
            M = np.concatenate((M[:i],M[i+1:]))
        else :
            i += 1
        
    L = []
    max = np.max(M)
    for i in range(len(M)) :
        for j in range(len(M[0])) :
                L.append(M[i][j])

    L.sort()
    med = L[int(len(L)/2)]
    med = 3
    for i in range(len(M)) :
        for j in range(len(M[0])) :
            if M[i][j] >= med :
                M[i][j] = 1 + (M[i][j]-med) / (max-med)
            else :
                M[i][j] = M[i][j] / med
    
    return M
                
M_ = post_traitement( M )

plt.imshow(M_,'jet')

# [i1, i2, ...]
# ik = {id:seconde, vehs:[veh1, veh2, ...]}
# vehi = {id:attrib, x:abs, y:ord, tronc:tronc, v:v}
