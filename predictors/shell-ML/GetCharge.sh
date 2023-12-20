#!/bin/bash
cd $1
for i in *.log
do
   Charge=`grep 'Charge = ' $i | head -1 | awk '{print $3}'`
   echo "$i:$Charge" >> Charge.log
done
