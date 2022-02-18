load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"

begin
	print("begin: "+get_cpu_time())

;	out_file_dir = "/archive/Linjiong.Zhou/NGGPS/NCEP_fore"
;	tmp_dir      = "/archive/Linjiong.Zhou/NGGPS/NCEP_fore"
	tmp_dir      = systemfunc("echo $TMPDIR")

;	date = 20150903

;	utct = (/ "00", "06", "12", "18", "24",\
;			  "30", "36", "42", "48",\
;			  "54", "60", "66", "72",\
;			  "78", "84", "90", "96",\
;			 "102","108","114","120",\
;			 "126","132","138","144",\
;			 "150","156","162","168",\
;			 "174","180","186","192",\
;			 "198","204","210","216",\
;			 "222","228","234","240"/)

	setfileoption("nc","Format","LargeFile")
        
        grav  = 9.80665 
   
        lev = (/1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0, 50.0, 70.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0, 900.0, 925.0, 950.0, 975.0, 1000.0/)
	lev!0 = "lev"
	lev@long_name = "level"
	lev@units = "hPa"
	lev&lev = lev
    
	print("date = "+date+", utct = "+utct)

        ;fname = out_file_dir+"/"+date+"00/ori/"+date+"_00Z"+utct+"_T1534_3d.nc"
   	;fname = out_file_dir+"/"+date+"06/"+date+"_06Z"+utct+"_T1534_3d.nc"
        fname = out_file_dir+"/"+date+"12/ori/"+date+"_12Z"+utct+"_T1534_3d.nc"
        ;fname = out_file_dir+"/"+date+"18/"+date+"_18Z"+utct+"_T1534_3d.nc"


	system("dmget -v "+fname)


    ;time = cd_inv_calendar(toint(str_get_cols(date,0,3)),toint(str_get_cols(date,4,5)),toint(str_get_cols(date,6,7)),0,0,0,"days since 1970-01-01 00:00:00",0) + toint(utct) / 24.0
    time = cd_inv_calendar(toint(str_get_cols(date,0,3)),toint(str_get_cols(date,4,5)),toint(str_get_cols(date,6,7)),12,0,0,"days since 1970-01-01 00:00:00",0) + toint(utct) / 24.0
	time@units = "days since 1970-01-01 00:00:00"
	time@long_name = "simulation time"
	time@calendar = "julian"

	if (fileexists(fname)) then

		;system("dmget -v "+fname)

		filin = addfile(fname,"r")
    
		print("readin data: "+get_cpu_time())
    
		lat   = filin->latitude(::-1)
		lon   = filin->longitude
		level = filin->level
		hyai  = filin->ak(::-1) / 1.E5
		hybi  = filin->bk(::-1)
		hyam  = (hyai(0:dimsizes(hyai)-2) + hyai(1:dimsizes(hyai)-1)) / 2.0
		hybm  = (hybi(0:dimsizes(hybi)-2) + hybi(1:dimsizes(hybi)-1)) / 2.0
		ps    = conform_dims((/dimsizes(time),dimsizes(lat),dimsizes(lon)/),filin->ps(::-1,:),(/1,2/))
		zs    = conform_dims((/dimsizes(time),dimsizes(lat),dimsizes(lon)/),filin->zs(::-1,:) * grav,(/1,2/))
		t     = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),filin->temp(::-1,::-1,:),(/1,2,3/))
		u     = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),filin->ugrd(::-1,::-1,:),(/1,2,3/))
		v     = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),filin->vgrd(::-1,::-1,:),(/1,2,3/))
    
		print("compute u: "+get_cpu_time())

		vwind = (/vinth2p_ecmwf(v,hyam,hybm,lev,ps,2,1000.0,1,True,0,t(:,dimsizes(level)-1,:,:),zs)/)
    
		vwind!0 = "time"
		vwind!1 = "lev"
		vwind!2 = "lat"
		vwind!3 = "lon"
		vwind@long_name = "v-wind"
		vwind@units = "m/s"
		vwind&time = time
		vwind&lev = lev
		vwind&lat = lat
		vwind&lon = lon
    
		print("output data: "+get_cpu_time())
    

                ;system("mkdir -p "+tmp_dir+"/"+date+"00")
                ;fname = tmp_dir+"/"+date+"00/"+date+"_00Z"+utct+"_T1534_v.nc"
	        ;fname = tmp_dir+"/"+date+"00/"+date+"_00Z_T1534_v_10day.nc"     ; for 2nd method of dling files
	        ;system("mkdir -p "+tmp_dir+"/"+date+"06")
                ;fname = tmp_dir+"/"+date+"06/"+date+"_06Z"+utct+"_T1534_v.nc"
                system("mkdir -p "+tmp_dir+"/"+date+"12")
                fname = tmp_dir+"/"+date+"12/"+date+"_12Z"+utct+"_T1534_v.nc"
                ;system("mkdir -p "+tmp_dir+"/"+date+"18")
                ;fname = tmp_dir+"/"+date+"18/"+date+"_18Z"+utct+"_T1534_v.nc"
		system("rm -f "+fname)
		filou = addfile(fname,"c")
		filou->vwind = vwind

	end if

	print("end: "+get_cpu_time())

end
