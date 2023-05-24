#!/usr/bin/python
# MatElastpy 
# for checking the strength
# lhy@calypso.cn(Hanyu Liu)
# 1st version May 24, 2023

import os
import math
import sys
import numpy as np
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
ften = open("strength.dat",'w')
ften.write("0.0"+'\t'+"0.0"+'\n')
tmp2 = 0.0

for i in range(1,int(step)):
  print("step"+str(i)+"finish")
  ftmp=open(f"OUTCAR_{i}")
  for line in ftmp:
    if 'in kB' in line:
     tmp1 = line.split() 
     if strength == '1':
        tmp2 = float(float(tmp1[2])/10.0*-1.0) #x 
     if strength == '2':
        tmp2 = float(float(tmp1[7])/10.0*-1.0) #zx     
     if strength == '3':
        tmp2 = float(float(tmp1[7])/10.0*-1.0) #zx    
  ftmp.close()
  ften.write(str((1.0+float(strain))**float(i)-1.0)+'\t'+str(tmp2)+'\n')
  print(str(tmp2))
ften.close()


