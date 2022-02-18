#!/bin/csh -f
#SBATCH -J ncrcat_files
#SBATCH -n 1
#SBATCH -t 16:00:00
#SBATCH -A gfdl_w
#SBATCH -o /home/Tyler.Barbero/STDO/%x.o%j
#SBATCH -D /home/Tyler.Barbero/STDO
#SBATCH -p batch
#SBATCH --export=ini_date=20070101,year=2007,ens=e1,AL

set echo

source $MODULESHOME/init/tcsh
module unload fre netcdf ncarg nco
module load fre/bronx-15 netcdf ncarg nco
#foreach ini_date (20170827)
#foreach ini_date ( `seq 20170828 20170831` `seq 20170901 20170912` `seq 20170914 20170930` )

foreach ini_hour ( 12 )
set in_file_path = /archive/Tyler.Barbero/GFS/${ini_date}${ini_hour}
set out_file_path = /archive/Tyler.Barbero/GFS/${ini_date}${ini_hour}

foreach var ( h t u v )


  cd $in_file_path
	#if ( ! -f $in_file_path/${ini_date}_${ini_hour}Z_${var}_360x180.nc )  break 
  # Change dimension "time" to a record dimension
  #
  foreach hh ( 06 `seq 12 6 240` )
  ncks -m -O --mk_rec_dmn time ${ini_date}_${ini_hour}Z${hh}_${var}_360x180.nc ${out_file_path}/${ini_date}_${ini_hour}Z${hh}_${var}_360x180.nc
  end

  cd ${out_file_path}


  ncrcat -O  \
     ${ini_date}_${ini_hour}Z06_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z12_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z18_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z24_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z30_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z36_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z42_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z48_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z54_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z60_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z66_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z72_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z78_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z84_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z90_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z96_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z102_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z108_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z114_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z120_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z126_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z132_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z138_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z144_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z150_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z156_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z162_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z168_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z174_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z180_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z186_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z192_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z198_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z204_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z210_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z216_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z222_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z228_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z234_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z240_${var}_360x180.nc \
     ${ini_date}_${ini_hour}Z_${var}_360x180.nc

end
end
end
