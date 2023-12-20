#!/bin/bash
arr_Ele=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg" "H" "B" "C" "N" "O" "F" "Si" "Ge" "Sn" "P" "As" "Sb" "S" "Se" "Te" "Cl" "Br" "I") 
CovalRadius=(1.70 1.60 1.53 1.39 1.50 1.42 1.38 1.24 1.32 1.22 1.90 1.75 1.64 1.54 1.47 1.46 1.42 1.39 1.45 1.44 1.75 1.70 1.62 1.51 1.44 1.41 1.36 1.36 1.32 0.31 0.84 0.73 0.71 0.66 0.57 1.11 1.20 1.39 1.07 1.19 1.39 1.05 1.20 1.38 1.02 1.20 1.39) 
NUM=${#arr_Ele[*]}
cd $1
for i in *.xyz
do
   echo $i
   COORDNUM=0
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
            COORDNUM=$((COORDNUM+1)) 
            echo $myline >> CoordAtoms.txt
         fi        
      fi
   done < $i 
   rm CoordAtoms.txt
   prefix=${i%.*}
   pprefix=${prefix%.*}
   echo "Coordination number of $pprefix:$COORDNUM" >> CoordinationNumber.log 
done
