load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"

begin
        fname = "/archive/twb/GFS/"+date+hh+"/"+date+"_"+hh+"Z"+ff+"_T1534_h.nc"
	system("dmget -v "+fname)
        filin = addfile(fname,"r")

        time      = filin->time
        latitude  = filin->lat
        longitude = filin->lon

        lat = fspan(-89.5,89.5,180)
        lon = fspan(0.5,359.5,360)

        lat!0         = "lat"
        lat@long_name = latitude@long_name
        lat@units     = latitude@units
        lat&lat       = lat

        lon!0         = "lon"
        lon@long_name = longitude@long_name
        lon@units     = longitude@units
        lon&lon       = lon

        t  = area_conserve_remap_Wrap(longitude,latitude,filin->hgt(:,:,:,:),lon,lat,False)

	fname = "/archive/Tyler.Barbero/GFS/"+date+hh+"/"+date+"_"+hh+"Z"+ff+"_h_360x180.nc"
        system("rm -f "+fname)
        filou = addfile(fname,"c")
        filou->time      = time
        filou->latitude  = lat
        filou->longitude = lon
        filou->hgt       = t



end

