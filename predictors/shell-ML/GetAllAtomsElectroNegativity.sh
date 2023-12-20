#!/bin/bash
#Get electronegativity of metal and all coordination atoms
arr_Ele=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg" "H" "B" "C" "N" "O" "F" "Si" "Ge" "Sn" "P" "As" "Sb" "S" "Se" "Te" "Cl" "Br" "I")
CovalRadius=(1.70 1.60 1.53 1.39 1.50 1.42 1.38 1.24 1.32 1.22 1.90 1.75 1.64 1.54 1.47 1.46 1.42 1.39 1.45 1.44 1.75 1.70 1.62 1.51 1.44 1.41 1.36 1.36 1.32 0.31 0.84 0.73 0.71 0.66 0.57 1.11 1.20 1.39 1.07 1.19 1.39 1.05 1.20 1.38 1.02 1.20 1.39)
arr_M=("Sc" "Ti" "V" "Cr" "Mn" "Fe" "Co" "Ni" "Cu" "Zn" "Y" "Zr" "Nb" "Mo" "Tc" "Ru" "Rh" "Pd" "Ag" "Cd" "Hf" "Ta" "W" "Re" "Os" "Ir" "Pt" "Au" "Hg")
arr_NM=("H" "B" "C" "N" "O" "F" "Si" "Ge" "Sn" "P" "As" "Sb" "S" "Se" "Te" "Cl" "Br" "I")
arr_ElectroNegM=(1.40 1.50 1.60 1.70 1.60 1.80 1.90 1.90 1.40 1.50 1.20 1.30 1.50 2.20 2.30 2.30 2.30 2.20 1.40	1.40 1.30 1.40 2.30 2.20 2.20 2.20 2.30 2.50 2.00)
arr_ElectroNegNM=(2.17 1.88 2.45 2.93 3.61 4.14 2.12 2.14 2.12 2.46 2.25 2.15 2.64 2.46 2.29 3.05 2.83 2.57)
cd $1
NUM=${#arr_Ele[*]}
NUM_M=${#arr_M[*]}
NUM_NM=${#arr_NM[*]}
for i in *.xyz
do
   echo $i
   Ele=`sed -n '3p' $i | awk '{print $1}'`
   XM=`sed -n '3p' $i | awk '{print $2}'`
   YM=`sed -n '3p' $i | awk '{print $3}'`
   ZM=`sed -n '3p' $i | awk '{print $4}'`
   StrEle=''
   StrElectroNeg=''
   for((j=0;j<$NUM_M;j++))
   do
      if [[ $Ele == ${arr_M[j]} ]] ; then
         StrEle=''$StrEle' '${arr_M[j]}''
         StrElectroNeg=''$StrElectroNeg' '${arr_ElectroNegM[j]}''
         break
      fi
   done
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
            echo "$Ele2 " >> CoordinationAtoms1
         fi        
      fi
   done < $i
   for((j=0;j<6;j++))
   do
      VAR=`grep "${arr_NM[j]} " CoordinationAtoms1`
      StrEle=''$StrEle' '${arr_NM[j]}''
      if [[ $VAR != '' ]] ; then
         StrElectroNeg=''$StrElectroNeg' '${arr_ElectroNegNM[j]}''
      else 
         StrElectroNeg=''$StrElectroNeg' '0.00''
      fi
   done
   VARSi=`grep "${arr_NM[6]} " CoordinationAtoms1`
   VARGe=`grep "${arr_NM[7]} " CoordinationAtoms1`
   VARSn=`grep "${arr_NM[8]} " CoordinationAtoms1`
   if [[ $VARSi != '' ]] ; then
      CoeffSi=1.00
   else
      CoeffSi=0.00
   fi
   if [[ $VARGe != '' ]] ; then
      CoeffGe=1.00
   else
      CoeffGe=0.00
   fi
   if [[ $VARSn != '' ]] ; then
      CoeffSn=1.00
   else
      CoeffSn=0.00
   fi
   Coeff=`echo "$CoeffSi+$CoeffGe+$CoeffSn" | bc`
   d=${arr_ElectroNegNM[6]}
   e=${arr_ElectroNegNM[7]}
   f=${arr_ElectroNegNM[8]}
   if [ $(echo "$Coeff > 0.00"|bc) = 1 ]; then
      ElectroNegSiGeSn=`echo "scale=2;($CoeffSi*$d + $CoeffGe*$e + $CoeffSn*$f)/($CoeffSi+$CoeffGe+$CoeffSn)"|bc`
   else
      ElectroNegSiGeSn='0.00'
   fi
   VARP=`grep "${arr_NM[9]} " CoordinationAtoms1`
   VARAs=`grep "${arr_NM[10]} " CoordinationAtoms1`
   VARSb=`grep "${arr_NM[11]} " CoordinationAtoms1`
   if [[ $VARP != '' ]] ; then
      CoeffP=1.00
   else
      CoeffP=0.00
   fi
   if [[ $VARAs != '' ]] ; then
      CoeffAs=1.00
   else
      CoeffAs=0.00
   fi
   if [[ $VARSb != '' ]] ; then
      CoeffSb=1.00
   else
      CoeffSb=0.00
   fi
   Coeff2=`echo "$CoeffP+$CoeffAs+$CoeffSb" | bc`
   d2=${arr_ElectroNegNM[9]}
   e2=${arr_ElectroNegNM[10]}
   f2=${arr_ElectroNegNM[11]}
   if [ $(echo "$Coeff2 > 0.00"|bc) = 1 ]; then
      ElectroNegPAsSb=`echo "scale=2;($CoeffP*$d2 + $CoeffAs*$e2 + $CoeffSb*$f2)/($CoeffP+$CoeffAs+$CoeffSb)"|bc`
   else
      ElectroNegPAsSb='0.00'
   fi
   VARS=`grep "${arr_NM[12]} " CoordinationAtoms1`
   VARSe=`grep "${arr_NM[13]} " CoordinationAtoms1`
   VARTe=`grep "${arr_NM[14]} " CoordinationAtoms1`
   if [[ $VARS != '' ]] ; then
      CoeffS=1.00
   else
      CoeffS=0.00
   fi
   if [[ $VARSe != '' ]] ; then
      CoeffSe=1.00
   else
      CoeffSe=0.00
   fi
   if [[ $VARTe != '' ]] ; then
      CoeffTe=1.00
   else
      CoeffTe=0.00
   fi
   Coeff3=`echo "$CoeffS+$CoeffSe+$CoeffTe" | bc`
   d3=${arr_ElectroNegNM[12]}
   e3=${arr_ElectroNegNM[13]}
   f3=${arr_ElectroNegNM[14]}
   if [ $(echo "$Coeff3 > 0.00"|bc) = 1 ]; then
      ElectroNegSSeTe=`echo "scale=2;($CoeffS*$d3 + $CoeffSe*$e3 + $CoeffTe*$f3)/($CoeffS+$CoeffSe+$CoeffTe)"|bc`
   else
      ElectroNegSSeTe='0.00'
   fi
   VARCl=`grep "${arr_NM[15]} " CoordinationAtoms1`
   VARBr=`grep "${arr_NM[16]} " CoordinationAtoms1`
   VARI=`grep "${arr_NM[17]} " CoordinationAtoms1`
   if [[ $VARCl != '' ]] ; then
      CoeffCl=1.00
   else
      CoeffCl=0.00
   fi
   if [[ $VARBr != '' ]] ; then
      CoeffBr=1.00
   else
      CoeffBr=0.00
   fi
   if [[ $VARI != '' ]] ; then
      CoeffI=1.00
   else
      CoeffI=0.00
   fi
   Coeff4=`echo "$CoeffCl+$CoeffBr+$CoeffI" | bc`
   d4=${arr_ElectroNegNM[15]}
   e4=${arr_ElectroNegNM[16]}
   f4=${arr_ElectroNegNM[17]}
   if [ $(echo "$Coeff4 > 0.00"|bc) = 1 ]; then
      ElectroNegClBrI=`echo "scale=2;($CoeffCl*$d4 + $CoeffBr*$e4 + $CoeffI*$f4)/($CoeffCl+$CoeffBr+$CoeffI)"|bc`
   else
      ElectroNegClBrI='0.00'
   fi
   StrElectroNeg=''$StrElectroNeg' '$ElectroNegSiGeSn' '$ElectroNegPAsSb' '$ElectroNegSSeTe' '$ElectroNegClBrI''   
   StrEle=''$StrEle' 'Si' 'P' 'S' 'Cl''
   rm CoordinationAtoms1
   prefix=${i%.*}
   pprefix=${prefix%.*}
   echo "Electronegativity of metal and coordination atoms of $pprefix:$StrEle:$StrElectroNeg" >> ElectroNegativity.log 
done
