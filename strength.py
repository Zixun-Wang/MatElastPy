#!/usr/bin/python
# MatElastpy
# for calculating ideal strength
# lhy@calypso.cn(Hanyu Liu)
# 1st version May 24, 2023

import os
import math
import sys
import numpy as np

def writepos(pos,strength,strain):#write the position after rotating
  f = open(pos) 
  a = []
  for line in f:
    a.append(line)
  f.close()

  f = open("POSCAR_new",'w')
  for i in range(0,2):
    f.write(a[i])
  b = []
  btmp = []
  #c is the atomic coordinate
  for i in range(2,5):
    c = a[i]
    b.append(list(map(float,c.split())))
    btmp.append(list(map(float,c.split())))
# tensile 
  if strength == "1":
    b[0][0]=b[0][0]*(1.0+float(strain))
    b[1][0]=b[1][0]*(1.0+float(strain))
    b[2][0]=b[2][0]*(1.0+float(strain))
# shear
  if strength == "2":
    b[0][0]=btmp[0][0]+btmp[0][2]*float(strain)
    b[0][2]=btmp[0][2]+btmp[0][0]*float(strain)
    b[1][0]=btmp[1][0]+btmp[1][2]*float(strain)
    b[1][2]=btmp[1][2]+btmp[1][0]*float(strain)
    b[2][0]=btmp[2][0]+btmp[2][2]*float(strain)
    b[2][2]=btmp[2][2]+btmp[2][0]*float(strain)
# indentation
  if strength == "3":
    b[0][2]=btmp[0][2]+btmp[0][0]*float(strain)
    b[1][2]=btmp[1][2]+btmp[1][0]*float(strain)
    b[2][2]=btmp[2][2]+btmp[2][0]*float(strain)
  

  for i in range(len(b)):
     f.write(str(b[i][0])+'\t'+str(b[i][1])+'\t'+str(b[i][2])+'\n')
  for i in range(5,len(a)):
    f.write(a[i])
  f.close()

def rotate(pos,alpha,beta,gamma): #rotate the crystal
  f = open(pos)
  pi = float(3.1415926)
  a = []
  for line in f:
    a.append(line)
  f.close()
  f = open("POSCAR_rotate",'w')
  for i in range(0,2):
     f.write(a[i])
  b = []
  vecb = []
  vecc = []
  vecd = []
  for i in range(2,5):
    c = a[i]
    b.append(list(map(float,c.split())))
    vecb.append(list(map(float,c.split())))
    vecc.append(list(map(float,c.split())))
    vecd.append(list(map(float,c.split())))

  
  alpha = float(alpha)
  beta = float(beta)
  gamma = float(gamma)
  #rotate x
  vecb[0][0] = b[0][0]*math.cos(alpha/180.0*pi)+b[0][1]*math.sin(alpha/180.0*pi)*(-1.0)
  vecb[0][1] = b[0][0]*math.sin(alpha/180.0*pi)+b[0][1]*math.cos(alpha/180.0*pi)
  vecb[0][2] = b[0][2]
  vecb[1][0] = b[1][0]*math.cos(alpha/180.0*pi)+b[1][1]*math.sin(alpha/180.0*pi)*(-1.0)
  vecb[1][1] = b[1][0]*math.sin(alpha/180.0*pi)+b[1][1]*math.cos(alpha/180.0*pi)  
  vecb[1][2] = b[1][2]
  vecb[2][0] = b[2][0]*math.cos(alpha/180.0*pi)+b[2][1]*math.sin(alpha/180.0*pi)*(-1.0)
  vecb[2][1] = b[2][0]*math.sin(alpha/180.0*pi)+b[2][1]*math.cos(alpha/180.0*pi)
  vecb[2][2] = b[2][2]

#rotate y
  vecc[0][0] = vecb[0][0]*math.cos(beta/180.0*pi)+vecb[0][2]*math.sin(beta/180.0*pi)
  vecc[0][2] = vecb[0][0]*math.sin(beta/180.0*pi)*(-1.0)+vecb[0][2]*math.cos(beta/180.0*pi)
  vecc[2][0] = vecb[2][0]*math.cos(beta/180.0*pi)+vecb[2][2]*math.sin(beta/180.0*pi)
  vecc[2][2] = vecb[2][0]*math.sin(beta/180.0*pi)*(-1.0)+vecb[2][2]*math.cos(beta/180.0*pi)
  vecc[0][1] = vecb[0][1]
  vecc[1][0] = vecb[1][0]*math.cos(beta/180.0*pi)+vecb[1][2]*math.sin(beta/180.0*pi)
  vecc[1][1] = vecb[1][1]
  vecc[1][2] = vecb[1][0]*math.sin(beta/180.0*pi)*(-1.0)+vecb[1][2]*math.cos(beta/180.0*pi)
  vecc[2][1] = vecb[2][1]

#rotate z
  vecd[0][0] = vecc[0][0]
  vecd[0][1] = vecc[0][1]*math.cos(gamma/180.0*pi)+vecc[0][2]*math.sin(gamma/180.0*pi)*(-1.0)
  vecd[0][2] = vecc[0][1]*math.sin(gamma/180.0*pi)+vecc[0][2]*math.cos(gamma/180.0*pi)
  vecd[1][0] = vecc[1][0]
  vecd[1][1] = vecc[1][1]*math.cos(gamma/180.0*pi)+vecc[1][2]*math.sin(gamma/180.0*pi)*(-1.0)
  vecd[1][2] = vecc[1][1]*math.sin(gamma/180.0*pi)+vecc[1][2]*math.cos(gamma/180.0*pi)
  vecd[2][0] = vecc[2][0]
  vecd[2][1] = vecc[2][1]*math.cos(gamma/180.0*pi)+vecc[2][2]*math.sin(gamma/180.0*pi)*(-1.0)
  vecd[2][2] = vecc[2][1]*math.sin(gamma/180.0*pi)+vecc[2][2]*math.cos(gamma/180.0*pi)

  for i in range(len(b)):
    f.write(str(vecd[i][0])+'\t'+str(vecd[i][1])+'\t'+str(vecd[i][2])+'\n')
  for i in range(5,len(a)):
    f.write(a[i])
  f.close()
  

strain=0.02
#check if the input.dat exists
try:
  fin = open("input.dat")
except:
  print ("no input.dat\n input.dat format as below:")
  print ("POSCAR")
  print ("0.02  #strain")
  print ("20    #step")
  print ("-45.0 -35.26439028430031 0.0     # alpha beta gamma (degree)")
  print ("2                   # 1 tensile, 2 shear")
  print ("mpiexec -np 6 ~/bin/vasp_shear")
  sys.exit()


fin_tmp = []
cmd = []
for line in fin:
  fin_tmp.append(line.split())
  cmd.append(line)
print(cmd[5])
pos = fin_tmp[0][0]
strain = fin_tmp[1][0]
step = fin_tmp[2][0]
alpha = fin_tmp[3][0]
beta = fin_tmp[3][1]
gamma = fin_tmp[3][2]
strength = fin_tmp[4][0]

rotate(pos,alpha,beta,gamma)

os.system("cp POSCAR_rotate POSCAR_0")
os.system("cp POSCAR_rotate POSCAR")
ften = open("strength.dat",'w')
ften.write("0.0"+'\t'+"0.0"+'\n')
tmp2 = 0.0

for i in range(0,int(step)):
  writepos("POSCAR",strength,strain)
  os.system("cp POSCAR_new POSCAR") #update POSCAR
  os.system(cmd[5]) #run vasp 
  os.system(f"cp OUTCAR OUTCAR_{i}")
  os.system("cp CONTCAR POSCAR")
  os.system(f"cp CONTCAR CONTCAR_{i}")
  os.system(f"cp vasp.log vasp.log_{i}")
  os.system("rm OUTCAR")
ften.close()


