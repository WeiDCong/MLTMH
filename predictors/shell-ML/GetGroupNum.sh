#!/bin/bash
cd $1
for i in *.xyz
do
   VAR1=${i%.*}
   VAR2=$2
   if [[ $VAR2 = 'Sc'  ||  $VAR2 = 'Y' ]]; then
      VAR3=3
   elif [[ $VAR2 = 'Ti'  ||  $VAR2 = 'Zr'  ||  $VAR2 = 'Hf' ]]; then
      VAR3=4
   elif [[ $VAR2 = 'V'  ||  $VAR2 = 'Nb'  ||  $VAR2 = 'Ta' ]]; then
      VAR3=5
   elif [[ $VAR2 = 'Cr'  ||  $VAR2 = 'Mo'  ||  $VAR2 = 'W' ]]; then
      VAR3=6
   elif [[ $VAR2 = 'Mn'  ||  $VAR2 = 'Tc'  ||  $VAR2 = 'Re' ]]; then
      VAR3=7
   elif [[ $VAR2 = 'Fe'  ||  $VAR2 = 'Ru'  ||  $VAR2 = 'Os' ]]; then
      VAR3=8
   elif [[ $VAR2 = 'Co'  ||  $VAR2 = 'Rh'  ||  $VAR2 = 'Ir' ]]; then
      VAR3=9
   elif [[ $VAR2 = 'Ni'  ||  $VAR2 = 'Pd'  ||  $VAR2 = 'Pt' ]]; then
      VAR3=10
   elif [[ $VAR2 = 'Cu'  ||  $VAR2 = 'Ag'  ||  $VAR2 = 'Au' ]]; then
      VAR3=11
   elif [[ $VAR2 = 'Zn'  ||  $VAR2 = 'Cd'  ||  $VAR2 = 'Hg' ]]; then
      VAR3=12
   fi
   pprefix=${VAR1%.*}
   echo "Group of $pprefix is:$VAR3 " >> GroupNum.log
done
