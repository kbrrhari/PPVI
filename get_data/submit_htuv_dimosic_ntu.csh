#!/bin/csh -f

#set echo

#foreach date ( 20180901 20180904 20180907 20180910 20180913 20180916 20180919 20180922 20180925 20180928 20181001 20181004 20181007 20181010 ) 

# Hurricane Irma (6) and Maria (10) Dates
foreach date ( 20170827 )
#foreach date ( `seq 20170828 20170831` `seq 20170901 20170912` `seq 20170914 20170930` )



# For analysis data
set hour = ( "00" )

# For forecast data
#set hour = ( "00" \
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


foreach dd ( $date )
		echo $dd
         foreach hh ( $hour )
		sed "s#dddddd#$dd#g   \
                      s#hhhhhh#$hh#g " \
                get_htuv_dimosic_ntu.csh >! get_htuv_dimosic_ntu_tmp.csh
                chmod 755 get_htuv_dimosic_ntu_tmp.csh
                sbatch --export=date=$date,hour=$hh,ALL get_htuv_dimosic_ntu_tmp.csh
                rm -f get_htuv_dimosic_ntu_tmp.csh
         end
end
end
