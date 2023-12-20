#!/bin/bash
cd $1
for i in *.xyz
do
   VAR1=${i%.*}
   VAR2=$2
   if [[ $VAR2 == 'Sc' ]] || [[ $VAR2 == 'Y' ]]; then
      VAR3='IIIB'
   elif [[ $VAR2 == 'Ti' ]] || [[ $VAR2 == 'Zr' ]] || [[ $VAR2 == 'Hf' ]]; then
      VAR3='IVB'
   elif [[ $VAR2 == 'V' ]] || [[ $VAR2 == 'Nb' ]] || [[ $VAR2 == 'Ta' ]]; then
      VAR3='VB'
   elif [[ $VAR2 == 'Cr' ]] || [[ $VAR2 == 'Mo' ]] || [[ $VAR2 == 'W' ]]; then
      VAR3='VIB'
   elif [[ $VAR2 == 'Mn' ]] || [[ $VAR2 == 'Tc' ]] || [[ $VAR2 == 'Re' ]]; then
      VAR3='VIIB'
   elif [[ $VAR2 == 'Fe' ]] || [[ $VAR2 == 'Co' ]] || [[ $VAR2 == 'Ni' ]] || [[ $VAR2 == 'Ru' ]] || [[ $VAR2 == 'Rh' ]] || [[ $VAR2 == 'Pd' ]] || [[ $VAR2 == 'Os' ]] || [[ $VAR2 == 'Ir' ]] || [[ $VAR2 == 'Pt' ]]; then
      VAR3='VIII'
   elif [[ $VAR2 == 'Cu' ]] || [[ $VAR2 == 'Ag' ]] || [[ $VAR2 == 'Au' ]]; then
      VAR3='IB'
   elif [[ $VAR2 == 'Zn' ]] || [[ $VAR2 == 'Cd' ]] || [[ $VAR2 == 'Hg' ]]; then
      VAR3='IIB'
   fi
   pprefix=${VAR1%.*}
   echo "Group of $pprefix is:$VAR3 " >> Group.log
done
