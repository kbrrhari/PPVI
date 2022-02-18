#!/bin/csh -f

# create list of initialization times to use in python
#
# change dates 
set lst = `seq  20170901 20170912`
echo "[ " 
foreach date ( $lst )
echo "'""$date"00"'","'""$date"12"'"","
end
echo " ]"

# or another way: printf and/or awk
