#!/bin/bash
cd $1
for i in *.xyz
do
   sed -n '3p' $i | awk '{print $1}' >> Metal
done
