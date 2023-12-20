#!/bin/bash
arr_Ele=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg" "H" "B" "C" "N" "O" "F" "Si" "Ge" "Sn" "P" "As" "Sb" "S" "Se" "Te" "Cl" "Br" "I")
CovalRadius=(1.70 1.60 1.53 1.39 1.50 1.42 1.38 1.24 1.32 1.22 1.90 1.75 1.64 1.54 1.47 1.46 1.42 1.39 1.45 1.44 1.75 1.70 1.62 1.51 1.44 1.41 1.36 1.36 1.32 0.31 0.84 0.73 0.71 0.66 0.57 1.11 1.20 1.39 1.07 1.19 1.39 1.05 1.20 1.38 1.02 1.20 1.39)
arr_NM=("H" "B" "C" "N" "O" "F" "Si" "P" "S" "Cl")
arr_COUNTNM=(0 0 0 0 0 0 0 0 0 0)
NUM=${#arr_Ele[*]}
NUM_NM=${#arr_NM[*]}
cd $1
for i in *.xyz
do
   echo $i
   Ele=`sed -n '3p' $i | awk '{print $1}'`
   XM=`sed -n '3p' $i | awk '{print $2}'`
   YM=`sed -n '3p' $i | awk '{print $3}'`
   ZM=`sed -n '3p' $i | awk '{print $4}'`
   for((m=0;m<$NUM;m++))
   do
      if [[ $Ele == ${arr_Ele[m]} ]]; then
         R1=${CovalRadius[m]}
         break
      fi
   done  
   iLine=0
   while read myline
   do
      iLine=$((iLine+1))
      if [ $iLine -gt 3 ];then
         Ele2=`echo $myline | awk '{print $1}'`
         X2=`echo $myline | awk '{print $2}'`
         Y2=`echo $myline | awk '{print $3}'`
         Z2=`echo $myline | awk '{print $4}'`
         for((k=0;k<$NUM;k++))
         do
            if [[ $Ele2 == ${arr_Ele[k]} ]]; then
               R2=${CovalRadius[k]}
               break
            fi
         done
         DIST=`echo "sqrt(($XM - $X2)^2 + ($YM - $Y2)^2 + ($ZM - $Z2)^2)" | bc` 
         R3=$(echo "$R1*1.35+$R2*1.35"|bc) 
         if [ $(echo "$DIST < $R3"|bc) = 1 ] && [ $(echo "$DIST < 2.8"|bc) = 1 ]; then
            echo $Ele2
            echo "$Ele2 " >> CoordinationAtoms3
         fi        
      fi
   done < $i
   for((m=0;m<6;m++))
   do
      arr_COUNTNM[m]=`grep "${arr_NM[m]} " CoordinationAtoms3|wc -l`
   done
   VARSi=`grep "Si " CoordinationAtoms3|wc -l`
   VARGe=`grep "Ge " CoordinationAtoms3|wc -l`
   VARSn=`grep "Sn " CoordinationAtoms3|wc -l`
   arr_COUNTNM[6]=$((VARSi+VARGe+VARSn))
   VARP=`grep "P " CoordinationAtoms3|wc -l`
   VARAs=`grep "As " CoordinationAtoms3|wc -l`
   VARSb=`grep "Sb " CoordinationAtoms3|wc -l`
   arr_COUNTNM[7]=$((VARP+VARAs+VARSb))
   VARS=`grep "S " CoordinationAtoms3|wc -l`
   VARSe=`grep "Se " CoordinationAtoms3|wc -l`
   VARTe=`grep "Te " CoordinationAtoms3|wc -l`
   arr_COUNTNM[8]=$((VARS+VARSe+VARTe))
   VARCl=`grep "Cl " CoordinationAtoms3|wc -l`
   VARBr=`grep "Br " CoordinationAtoms3|wc -l`
   VARI=`grep "I " CoordinationAtoms3|wc -l`
   arr_COUNTNM[9]=$((VARCl+VARBr+VARI))
   rm $1/CoordinationAtoms3
   prefix=${i%.*}
   pprefix=${prefix%.*}
   echo "Number of Coordination Atoms(H,B,C,N,O,F,Si,P,S and Cl) of $pprefix:${arr_COUNTNM[@]}" >> NumberOfCoordinationAtoms.log
done
