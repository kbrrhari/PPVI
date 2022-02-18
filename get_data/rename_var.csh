#!/bin/csh -f

# rename variables from h to respective hgt, temp, uwind, vwind in regridded nc files
#
#

set root_dir = "/archive/twb/"

module load nco

foreach dd ( `ls -d  $root_dir/2017*`)
	echo "Moving into: " "$dd"
	cd $dd
	
	foreach tt ( `ls *t_360x180.nc` )	
		ncrename -v h,temp $tt
	end
	
	foreach hh ( `ls *h_360x180.nc` )
	        ncrename -v h,hgt $hh
        end

	foreach uu ( `ls *u_360x180.nc` ) 
	        ncrename -v h,uwind $uu
        end

	foreach vv ( `ls *v_360x180.nc` ) 
	        ncrename -v h,vwind $vv
        end









end
