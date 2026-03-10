#finish
from tabulate import tabulate
import pandas as pd
import numpy as np
from sgp4.api import Satrec, jday
from skyfield.api import EarthSatellite, wgs84, load
from datetime import datetime, date, timedelta

def pos():
  L_Name = "EGYPTSAT 1"
  L1 = "1 31117U 07012A   22357.10969075  .00001066  00000-0  17051-3 0  9999"
  L2 = "2 31117  97.8961 307.0979 0004304 231.5410 128.5413 14.73761846842563"

  sat = EarthSatellite(L1, L2,L_Name)
  satellite = Satrec.twoline2rv(L1, L2)
  ts = load.timescale()
  start_date = "2022-12-24 9:00:00 UTC"
  t1 = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S UTC')
  end_date = "2022-12-24 10:00:00 UTC"
  t2 = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S UTC')
  
  time = pd.date_range(start=t1, end=t2, freq="1T")
  for i in range(len(time)):
    year = int(time[i].strftime("%Y"))
    month = int(time[i].strftime("%m"))
    day = int(time[i].strftime("%d"))
    hour = int(time[i].strftime("%H"))
    minute = int(time[i].strftime("%M"))
    second = int(time[i].strftime("%S"))
    jd, fr = jday(year, month, day, hour, minute, second)
    e, r, v = satellite.sgp4(jd, fr)
    rx, ry, rz = r[0], r[1], r[2]
    pos = [rx,ry,rz]
    t= ts.utc(year, month, day, hour, minute, second)

    geocentric = sat.at(t)
    lat, lon = wgs84.latlon_of(geocentric)
    last_data = [rx, ry, rz, lat, lon, time[i]]
    file = [["rx", "ry", "rz", "lat", "lon", "time"], last_data]
    # return data

    print(tabulate(file, headers = "firstrow", tablefmt="double_grid"))
  
pos()