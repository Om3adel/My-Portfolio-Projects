from tabulate import tabulate
import pandas as pd
import numpy as np
from skyfield.timelib import Timescale 
from sgp4.api import jday, Satrec
from skyfield.api import EarthSatellite, wgs84, load , Topos
from datetime import datetime, date, timedelta
import re 

def topocentic():
    L_Name = "EGYPTSAT 1"
    L1 = "1 31117U 07012A   22357.10969075  .00001066  00000-0  17051-3 0  9999"
    L2 = "2 31117  97.8961 307.0979 0004304 231.5410 128.5413 14.73761846842563"

    ts = load.timescale()
    sat = EarthSatellite(L1, L2)
    
    loc = Topos('29.08287 N', '31.10208 E')
    satellite = Satrec.twoline2rv(L1, L2)
    start_date = sat.epoch.utc_strftime()
    date1 = datetime.strptime("2022-12-24 11:15:31.605 UTC", '%Y-%m-%d %H:%M:%S.%f UTC')
    end_date = "2022-12-24 11:29:10.399 UTC"
    date2 = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f UTC')

    azimuth_arr = []
    elevation_arr = []
    range_arr = []
    time = pd.date_range(start=date1, end=date2, freq="1T")
    for i in range(len(time)):
        year = int(time[i].strftime("%Y"))
        month = int(time[i].strftime("%m"))
        day = int(time[i].strftime("%d"))
        hour = int(time[i].strftime("%H"))
        minute = int(time[i].strftime("%M"))
        second = int(time[i].strftime("%S"))

    #----------time transform to utc date format----------
        t= ts.utc(year, month, day, hour, minute, second)
        

    #----------define satellite at this time to know lat&lon----------
        geocentric = sat.at(t)


        difference = sat - loc
        topocentric = difference.at(t)
        ele, az, rang = topocentric.altaz()
        ele = str(ele)
        az = str(az)
        ele_deg =  re.split('["deg"\'\"]', ele)[0]
        ele_minutes =  re.split('["deg"\'\"]', ele)[3]
        ele_seconds =  re.split('["deg"\'\"]', ele)[4]
        ele_decimal = (float(ele_deg) + float(ele_minutes)/60 + float(ele_seconds)/(60*60))
        az_deg =  re.split('["deg"\'\"]', az)[0]
        az_minutes =  re.split('["deg"\'\"]', az)[3]
        az_seconds =  re.split('["deg"\'\"]', az)[4]
        az_decimal = (float(az_deg) + float(az_minutes)/60 + float(az_seconds)/(60*60))
        ele_dec = round(ele_decimal,3)
        az_dec = round(az_decimal,3)

        azimuth_arr.append(az_dec)
        elevation_arr.append(ele_dec)
        range_arr.append(rang.km)
        # if ele.degrees > 0:

        #     print('The Satellite is above the horizon')

        #     print('Elevation:', ele)
        #     print('Azimuth:', az)
        #     print('Range: {:.1f} km'.format(distance.km))

    

    #---------- data in object to display in table----------
    azi_ele_range = {
    "Time": time,
    "Azimuth(deg)": azimuth_arr,
    "Elevation(deg)": elevation_arr,
    "Range(km)":range_arr
    }

    pd.set_option('display.colheader_justify', 'center')
    az_ele = pd.DataFrame(azi_ele_range).to_string(index=False)
    return az_ele


print(topocentic())






# from skyfield.api import EarthSatellite

# ts = load.timescale()
# L1 = "1 24793U 97020B   22350.62556775  .00000329  00000-0  10943-3 0  9992"
# L2 = "2 24793  86.3988 199.3675 0001901  89.6886 270.4528 14.34601242340861"

# satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
# print(satellite)
# t = ts.utc(2014, 1, 23, 11, 18, 7)

# days = t - satellite.epoch
# print('{:.3f} days away from epoch'.format(days))

# if abs(days) > 14:
#     satellites = load.tle_file(stations_url, reload=True)
# bluffton = wgs84.latlon(+40.8939, -83.8917)
# t0 = ts.utc(2014, 1, 23)
# t1 = ts.utc(2014, 1, 24)
# t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=30.0)
# for ti, event in zip(t, events):
#     name = ('rise above 30°', 'culminate', 'set below 30°')[event]

# lat, lon = wgs84.latlon_of(geocentric)
# elevation_m = 123.0
# subpoint = wgs84.latlon(lat.degrees, lon.degrees, elevation_m)
# difference = satellite - bluffton
# topocentric = difference.at(t)
# alt, az, distance = topocentric.altaz()

# if alt.degrees > 0:
#     print('The ISS is above the horizon')

# print('Altitude:', alt)
# print('Azimuth:', az)
# print('Distance: {:.1f} km'.format(distance.km))
