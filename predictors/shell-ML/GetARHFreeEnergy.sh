#!/bin/bash
:> ARHFreeEnergy
cd $1
for i in *.xyz
do 
   FN=`sed -n '2p' $i | awk '{print $4}'`
   echo "$i: $FN" >> ARHFreeEnergy
done
