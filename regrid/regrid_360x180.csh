#!/bin/csh 
#PBS -N regrid_360x180_dddddd.csh
#tPBS -l size=1
#PBS -l walltime=1:00:00
#PBS -r y
#PBS -j oe
#PBS -A gfdl_w
#PBS -o /home/Tyler.Barbero/STDO
#PBS -d /home/Tyler.Barbero/STDO
#PBS -q batch
##PBS -m abe

set echo

source /usr/local/Modules/default/init/csh
module load ncarg/6.2.1

#foreach date ( 20170827 )
#foreach date ( `seq 20170828 20170831` `seq 20170901 20170912` `20170914 20170930`)
foreach date ( `seq 20170914 20170930` )
# Lead time variable
set ff = ( "00" \
                         "06"  "12"  "18"  "24" \
                         "30"  "36"  "42"  "48" \
                         "54"  "60"  "66"  "72" \
                         "78"  "84"  "90"  "96" \
                        "102" "108" "114" "120" \
                        "126" "132" "138" "144" \
                        "150" "156" "162" "168" \
                        "174" "180" "186" "192" \
                        "198" "204" "210" "216" \
                        "222" "228" "234" "240" ) 
# Init time variable
set hh = 12


foreach dd ( $date )
		echo $dd
	foreach ltime ( $ff )
		ncl date='"'$dd'"' hh='"'$hh'"' ff='"'$ltime'"' regrid_360x180_t.ncl
		ncl date='"'$dd'"' hh='"'$hh'"' ff='"'$ltime'"' regrid_360x180_u.ncl
		ncl date='"'$dd'"' hh='"'$hh'"' ff='"'$ltime'"' regrid_360x180_v.ncl
		ncl date='"'$dd'"' hh='"'$hh'"' ff='"'$ltime'"' regrid_360x180_hgt.ncl

	end
end
end
