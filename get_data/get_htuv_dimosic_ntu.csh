#!/bin/csh -f
#SBATCH -J get_htuv
#SBATCH -n 1
#SBATCH -t 12:00:00
#SBATCH -A gfdl_w
#SBATCH -o /home/Tyler.Barbero/STDO/%x.o%j
#SBATCH -D /home/Tyler.Barbero/STDO
#SBATCH -p batch
#SBATCH --export=date=20180901,hour=00,AL

set echo

source /usr/local/Modules/default/init/csh
module load ncarg/6.2.1

set out_file_dir = "/archive/Jan-Huey.Chen/DATA/NCEP_GFS_fore"


set date = dddddd
set hour = hhhhhh

ncl date=$date utct='"'$hour'"' out_file_dir='"'$out_file_dir'"' /home/Tyler.Barbero/scripts/get_hgt_for_dimosic_ntu_nemsio.ncl
ncl date=$date utct='"'$hour'"' out_file_dir='"'$out_file_dir'"' /home/Tyler.Barbero/scripts/get_t_for_dimosic_ntu_nemsio.ncl
ncl date=$date utct='"'$hour'"' out_file_dir='"'$out_file_dir'"' /home/Tyler.Barbero/scripts/get_u_for_dimosic_ntu_nemsio.ncl
ncl date=$date utct='"'$hour'"' out_file_dir='"'$out_file_dir'"' /home/Tyler.Barbero/scripts/get_v_for_dimosic_ntu_nemsio.ncl


# change ff for hour on directory
set ff = 06

foreach file ( `ls $TMPDIR/${date}${ff}/* | xargs -n 1 basename` )
        
	# if file already exists in archive, skip to next file 
	if ( -f /archive/twb/GFS/${date}${ff}/$file ) then
		echo "$file already exists in archive"
		continue
	
	# otherwise download file from TMP to archive
	else if ( ! -d /arhchive/Tyler.Barbero/GFS/${date}${ff} ) then 
		mkdir -p /archive/Tyler.Barbero/GFS/${date}${ff}
		cp -f $TMPDIR/${date}${ff}/$file /archive/Tyler.Barbero/GFS/${date}${ff}/

	endif

end
