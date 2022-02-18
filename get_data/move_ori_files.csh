#!/bin/csh -f

# move nongridded files to separate directory within same directory
# i.e., GFS/20170901/ori/all_original_nongridded_files.nc

set root_dir = /archive/twb/GFS

foreach date ( 20170827 20170828 20170829 20170830 20170831 20170901 20170902 20170903 20170904 20170905 20170906 20170907 20170908 20170909 20170910 20170911 20170912 20170914 20170915 20170916 20170917 20170918 20170919 20170920 20170921 20170922 20170923 20170924 20170925 20170926 20170927 20170928 20170929 20170930 )

foreach hour ( 12 )

if ( ! -d ${root_dir}/${date}${hour}/ori ) then
	
	mkdir ${root_dir}/${date}${hour}/ori
	mv ${root_dir}/${date}${hour}/*T1534_*.nc ${root_dir}/${date}${hour}/ori

endif

end
end
  
