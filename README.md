# MatElasticPy
 Computation prediction of ideal strength for a material
Introduction

Calculating Ideal strength of crystal structure using vasp. The original method is introduced by PRL 82,2713(1999)

Details

strength.py: calculating ideal strength
check.py : check the results and progress of the task as it progresses

First you need to modify vasp code. If you want to calculate ideal tensile strength, you should add 'FCELL(1,1)=0.0' to constr_cell_relax.F of vasp code. That means the Stress at x axis is fixed and vasp not relax the lattice at x axis. And if you choose ideal shear strength, you should add 'FCELL(1,3)= 0.0' and 'FCELL(3,1) = 0.0' to constr_cell_relax.F of vasp code. Here, you need to recompile vasp.

second, you should prepare input.dat and this file as below:
POSCAR
0.02 #strain
20 #step
-45.0 35.264390 0.0 # rotate Z, Y and X.
1 # 1 tensile, 2 shear 3 indentation
mpiexec -np  vasp

The first line is the name of POSCAR. The second line is strain of distortion. The third line is total step of distortion. The fourth line is degree of rotation. This is for calculating special orientation. We set x axis as tensile strength direction (tensile (x)). Also we set x and z axis as shear direction (shear (x)[z]). For example, if you want to calculating ideal strength of Diamond along 100, you just set 0.0 0.0 0.0. If you want to calculate 110 orientation, you need set -45.0 0.0 0.0. If you want to calculate 111 orientation, you need set -45.0 35.264390 0.0.
It is for rotating the x, y and z axis as a Right-handed helical rule. The five line is to choose tensile，shear or indentation. The sixth line is execute command.

for indentation strength, find the below part in main.F of vasp source code.

! for all DYN%ISIF greater or equal 3 cell shape optimisations will be done
        FACTSI = 0
        IF (DYN%ISIF>=3) FACTSI=10*DYN%POTIM*EVTOJ/AMTOKG/T_INFO%NIONS *1E-10_q

        DO I=1,3
        DO K=1,3
           D2SIF(I,K)=TSIF(I,K)*FACTSI
        ENDDO
        D2SIF(I,I)=D2SIF(I,I)-DYN%PSTRESS/(EVTOJ*1E22_q)*LATT_CUR%OMEGA*FACTSI
!lhy
        D2SIF(3,3)=D2SIF(3,3)-abs(D2SIF(1,3))*TAN(68.0/180.0*3.1415926)  
!lhy
        ENDDO 

where D2SIF(3,3)=D2SIF(3,3)-abs(D2SIF(1,3))*tan(68.0/180.0*3.1415926) is added.  This angle depends on the shape of indenter.

also need to modify the constr_cell_relax.F as below:
      SUBROUTINE CONSTR_CELL_RELAX(FCELL)
      USE prec
      REAL(q) FCELL(3,3)

!     just one simple example
!     relaxation in x directions only
!      SAVE=FCELL(1,1)
       FCELL(1,3)=0
       FCELL(3,1)=0
!      FCELL=0   ! F90 style: set the whole array to zero
!      FCELL(1,1)=SAVE

      RETURN
      END SUBROUTINE
where FCELL(1,3)=0 and FCELL(3,1)=0 are added.

In example, I removed the POTCAR due to vasp copyright. Where all caculations are performed
by PAW-LDA-CA 

Research highlights:

1, Miao Zhang, Mingchun Lu, Yonghui Du, Lili Gao, Cheng Lu and Hanyu Liu, "Hardness of FeB4?: Density functional theory investigation" J. Chem. Phys., 140, 174505 (2014)

2, Yinwei Li, Jian Hao, Hanyu Liu, Siyu Lu and John S. Tse "High energy density and superhard nitrogen-rich B-N compounds", Phys. Rev. Lett., 115, 105502 (2015)

3, Miao Zhang, Hanyu Liu, Quan Li, Bo Gao, Yanchao Wang, Hongdong Li, Changfeng Chen and Yanming Ma, “Superhard BC3 in cubic diamond structure” Phys. Rev. Lett., 114, 015502 (2015)

4, Quan Li, Hanyu Liu, Dan Zhou, Weitao Zheng, Zhijian Wu and Yanming Ma, "novel low compressible and superhard carbon nitride: Body-centered tetragonal CN2" Phys. Chem. Chem. Phys., 14, 13081–13087 (2012)

Dr. Hanyu Liu
Email: lhy@calypso.cn
       wangzx1120@mails.jlu.edu.cn
