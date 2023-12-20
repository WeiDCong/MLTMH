#!/bin/bash
arr_Ele=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg" "H" "B" "C" "N" "O" "F" "Si" "Ge" "Sn" "P" "As" "Sb" "S" "Se" "Te" "Cl" "Br" "I")
CovalRadius=(1.70 1.60 1.53 1.39 1.50 1.42 1.38 1.24 1.32 1.22 1.90 1.75 1.64 1.54 1.47 1.46 1.42 1.39 1.45 1.44 1.75 1.70 1.62 1.51 1.44 1.41 1.36 1.36 1.32 0.31 0.84 0.73 0.71 0.66 0.57 1.11 1.20 1.39 1.07 1.19 1.39 1.05 1.20 1.38 1.02 1.20 1.39)
arr_AN=("21" "22" "23" "24" "25" "26" "27" "28" "29" "30" "39" "40" "41" "42" "43" "44" "45" "46" "47" "48" "72" "73" "74" "75" "76" "77" "78" "79" "80" "1" "5" "6" "7" "8" "9" "14" "32" "50" "15" "33" "51" "16" "34" "52" "17" "35" "53")
NUM=${#arr_Ele[*]}
cd $1
for i in *.xyz
do
   echo $i
   Ele=`sed -n '3p' $i | awk '{print $1}'`
   XM=`sed -n '3p' $i | awk '{print $2}'`
   YM=`sed -n '3p' $i | awk '{print $3}'`
   ZM=`sed -n '3p' $i | awk '{print $4}'`
   XH=`sed -n '4p' $i | awk '{print $2}'`
   YH=`sed -n '4p' $i | awk '{print $3}'`
   ZH=`sed -n '4p' $i | awk '{print $4}'`
   LA=`echo "sqrt(($XM - $XH)^2 + ($YM - $YH)^2 + ($ZM - $ZH)^2)" | bc`
   for((m=0;m<$NUM;m++))
   do
      if [[ $Ele == ${arr_Ele[m]} ]]; then
         R1=${CovalRadius[m]}
         break
      fi
   done
   iLine=0
   iPara=0
   AN=0
   while read myline
   do
      iLine=$((iLine+1))
      if [ $iLine -gt 4 ];then
         EleA=`echo $myline | awk '{print $1}'`
         XA=`echo $myline | awk '{print $2}'`
         YA=`echo $myline | awk '{print $3}'`
         ZA=`echo $myline | awk '{print $4}'`
         for((k=0;k<$NUM;k++))
         do
            if [[ $EleA == ${arr_Ele[k]} ]]; then
               R2=${CovalRadius[k]}
               break
            fi
         done
         LB=`echo "sqrt(($XM - $XA)^2 + ($YM - $YA)^2 + ($ZM - $ZA)^2)" | bc`
         LC=`echo "sqrt(($XH - $XA)^2 + ($YH - $YA)^2 + ($ZH - $ZA)^2)" | bc`
         # 150 degrees
         #VAR=`echo "$LA*$LA+$LB*$LB+sqrt(3)*$LA*$LB"|bc` 
         # 170 degrees
         VAR=`echo "$LA*$LA+$LB*$LB+1.970*$LA*$LB"|bc`
         R3=$(echo "$R1*1.35+$R2*1.35"|bc)
         if [ $(echo "$LB < $R3"|bc) = 1 ] && [ $(echo "$LB < 2.8"|bc) = 1 ] && [ $(echo "$VAR < $LC*$LC"|bc) = 1 ]; then
            for((m=0;m<$NUM;m++))
            do
               if [[ $EleA == ${arr_Ele[m]} ]]; then
                  AN=${arr_AN[m]}
                  iPara=1
                  prefix=${i%.*}
                  pprefix=${prefix%.*}
                  echo "$i:$AN" >> LTrans.log
                  break
               fi
            done
         fi
      fi
   done < $i
   if [ $iPara -eq 0 ];then
      prefix=${i%.*}
      pprefix=${prefix%.*}
      echo "$i:0" >> LTrans.log
   fi
done
