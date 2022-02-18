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
    
	rvgas = 461.50
	rdgas = 287.05
	grav  = 9.80665
	zvir  = rvgas / rdgas - 1.
    
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
	print("fname = "+fname)

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
		q     = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),filin->spfh(::-1,::-1,:),(/1,2,3/))
    
		print("compute pi: "+get_cpu_time())
    
		hyai3d = conform_dims((/dimsizes(time),dimsizes(level)+1,dimsizes(lat),dimsizes(lon)/),hyai,1)
		hybi3d = conform_dims((/dimsizes(time),dimsizes(level)+1,dimsizes(lat),dimsizes(lon)/),hybi,1)
		psi3d  = conform_dims((/dimsizes(time),dimsizes(level)+1,dimsizes(lat),dimsizes(lon)/),ps,(/0,2,3/))
    
		pi   = hyai3d * 1E5 + hybi3d * psi3d
    
		print("compute delp and delz: "+get_cpu_time())
    
		delp = pi(:,0:dimsizes(level)-1,:,:) - pi(:,1:dimsizes(level),:,:)
		logdelp = log(pi(:,0:dimsizes(level)-1,:,:)) - log(pi(:,1:dimsizes(level),:,:))
		delz = - logdelp * t * (1 + zvir * q) * rdgas / grav
    
		print("compute pm: "+get_cpu_time())
    
		hyam3d = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),hyam,1)
		hybm3d = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),hybm,1)
		psm3d  = conform_dims((/dimsizes(time),dimsizes(level),dimsizes(lat),dimsizes(lon)/),ps,(/0,2,3/))
    
		pm   = hyam3d * 1E5 + hybm3d * psm3d
    
		print("compute zi: "+get_cpu_time())
    
		zi = new((/dimsizes(time),dimsizes(level)+1,dimsizes(lat),dimsizes(lon)/),"float")
		zi(:,dimsizes(level),:,:) = zs / grav
		do k = 0, dimsizes(level) - 1
			zi(:,k,:,:) = dim_sum_n(delz(:,k:dimsizes(level)-1,:,:),1) + zs / grav
		end do
    
		print("compute zm: "+get_cpu_time())
    
		pi!0 = "time"
		pi!1 = "lev"
		pi!2 = "lat"
		pi!3 = "lon"
    
		zi!0 = "time"
		zi!1 = "lev"
		zi!2 = "lat"
		zi!3 = "lon"
    
		pm!0 = "time"
		pm!1 = "lev"
		pm!2 = "lat"
		pm!3 = "lon"
    
		zmr = int2p(log(pi(time|:,lat|:,lon|:,lev|:)),zi(time|:,lat|:,lon|:,lev|:),log(pm(time|:,lat|:,lon|:,lev|:)),1)
    
		zmr!0 = "time"
		zmr!1 = "lat"
		zmr!2 = "lon"
		zmr!3 = "lev"
    
		zm = zmr(time|:,lev|:,lat|:,lon|:)
    
		print("compute hgt : "+get_cpu_time())
    
		hgt = (/vinth2p_ecmwf(zm,hyam,hybm,lev,ps,2,1000.0,1,True,-1,t(:,dimsizes(level)-1,:,:),zs)/)
    
		hgt!0 = "time"
		hgt!1 = "lev"
		hgt!2 = "lat"
		hgt!3 = "lon"
		hgt@long_name = "height"
		hgt@units = "m"
		hgt&time = time
		hgt&lev = lev
		hgt&lat = lat
		hgt&lon = lon
    
		print("output data: "+get_cpu_time())
    
		;system("mkdir -p "+tmp_dir+"/"+date+"00")
		;fname = tmp_dir+"/"+date+"00/"+date+"_00Z"+utct+"_T1534_h.nc"
		;fname = tmp_dir+"/"+date+"00/"+date+"_00Z_T1534_h_10day.nc"     ; for 2nd method of dling files
		;system("mkdir -p "+tmp_dir+"/"+date+"06")
		;fname = tmp_dir+"/"+date+"06/"+date+"_06Z"+utct+"_T1534_h.nc"
	  	system("mkdir -p "+tmp_dir+"/"+date+"12")
		fname = tmp_dir+"/"+date+"12/"+date+"_12Z"+utct+"_T1534_h.nc"
		;system("mkdir -p "+tmp_dir+"/"+date+"18")
		;fname = tmp_dir+"/"+date+"18/"+date+"_18Z"+utct+"_T1534_h.nc"
		system("rm -f "+fname)
		filou = addfile(fname,"c")
		filou->hgt = hgt

	end if

	print("end: "+get_cpu_time())

end
