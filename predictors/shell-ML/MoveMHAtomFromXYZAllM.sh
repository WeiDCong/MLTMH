#!/bin/bash
#Choose the smallest distance of all bonds
#Get metal element
cd $1
arr_M=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg")
NUM_M=${#arr_M[*]}
for k in *.xyz
do
   #VAR1=${k%.*}
   #METAL=${VAR1#*.}
   #echo $METAL
       #METAL=`sed -n '3p' $k | awk '{print $1}'`
   METAl=$2
   iLine=0
   while read myline
   do
      iLine=$((iLine+1))
      Ele=`echo $myline | awk '{print $1}'`
      if [[ $Ele == $METAL ]]; then
         sed -i ''$iLine'd' $k
         sed -i "3i $myline" $k
      fi
   done < $k
   
   #Get hydrogen element
   SMALLEST_MH_DIST=10.0
   iLine=0
   while read myline
   do
      iLine=$((iLine+1))
      if [ $iLine -eq 3 ]; then
         XM=`echo $myline | awk '{print $2}'`
         YM=`echo $myline | awk '{print $3}'`
         ZM=`echo $myline | awk '{print $4}'`
      fi
      Ele=`echo $myline | awk '{print $1}'`
      if [[ $Ele == "H" ]]; then
         XH=`echo $myline | awk '{print $2}'`
         YH=`echo $myline | awk '{print $3}'`
         ZH=`echo $myline | awk '{print $4}'`
         DIST=`echo "sqrt(($XM - $XH)^2 + ($YM - $YH)^2 + ($ZM - $ZH)^2)" | bc`
         if [ $(echo "$DIST <= $SMALLEST_MH_DIST"|bc) = 1 ]; then
            sed -i ''$iLine'd' $k
            sed -i "4i $myline" $k
            SMALLEST_MH_DIST=$DIST
         fi
      fi
   done < $k
done
