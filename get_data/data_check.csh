#!/bin/csh -f


# foreach directory in archive see if there are 164 files (fully downloaded)
#
cd /archive/twb/GFS
#
#echo "These directories are missing files:"
#foreach dirr ( `ls -d 2017*12` )
#	
#	if (`ls "$dirr" | wc -l` < 164) echo $dirr
#end
#
#echo "These directories have not been regridded:"
#foreach dirr ( `ls -d  2017*12` )
#	
#	if ( `ls "$dirr" | wc -l` >= 164  && `ls "$dirr" | wc -l` < 328 ) echo $dirr
#end 
#  
#echo "These directories have finished regridding:"
#foreach dirr ( `ls -d  2017*12` )
#
#        if ( `ls "$dirr" | wc -l` == 328 ) echo $dirr
#end

foreach dirr ( `ls -d 2017*12` )
ls "$dirr" | wc -l
end 
