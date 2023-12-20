#!/bin/bash
#Get metal element
cd $1
for k in *.xyz
do
   iLine=0
   while read myline
   do
      iLine=$((iLine+1))
      if [ $iLine -eq 3 ]; then
         XM=`echo $myline | awk '{print $2}'`
         YM=`echo $myline | awk '{print $3}'`
         ZM=`echo $myline | awk '{print $4}'`
      fi
      if [[ $iLine -eq 4 ]]; then
         XH=`echo $myline | awk '{print $2}'`
         YH=`echo $myline | awk '{print $3}'`
         ZH=`echo $myline | awk '{print $4}'`
         DIST=`echo "sqrt(($XM - $XH)^2 + ($YM - $YH)^2 + ($ZM - $ZH)^2)" | bc`
      fi
   done < $k
   echo "M-H Bond Length of $k:$DIST" >> M-H_BondLength.log
done

