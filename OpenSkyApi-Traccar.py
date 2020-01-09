
from opensky_api import OpenSkyApi
from datetime import datetime
import urllib
import time
import csv
import json
import sys
import requests


###Settings####
TCurl = 'http://localhost'
TCportU = ':5055'             #URL voor API (= website url  traccar: normal:. <ip>:8082
TCportR = ''
Traccar_user = ''                     #User for traccar (with devices for interface)
Traccar_password = ''                  #User pass
OpenSky_user = ''
OpenSky_Password = ''                 #Can be Empty (update max 1x 10 sec, with user 1x 5 sec)
update  = 15                                #seconds
s = None
### read TC devices.
TCupdate = 0
def tcdev():   #De API voor Traccar Devices
        payload = {}
        response = requests.get(TCurl + '/api/devices', auth=(Traccar_user, Traccar_password), params=payload, timeout=1.000)
#        print (response.status_code)
        if not str(response.status_code) == '200': #geef foutmelding als geen HTML 200 = OK
                print ("Serverstatus: " + str(response.status_code) + " Server: "+ TCurl + "  Account: " + Traccar_user)
        else:
#               data = json.loads(response.content)[0]
                gevonden = response.json()
                uitvraag = []
                for d in gevonden: #Lees Reccords & strip AIR-  ivm transpondergoede van OpenSky
                        uniqueId = d['uniqueId']
                        transponder = uniqueId.strip('AIR-')+','
                        uitvraag.append(transponder)
                return uitvraag
def listtostring(s):   #Omzetten van JSON naar String
        # initialize an empty string
        str1 = ""
        if not s == None:
                for ele in s:
                        str1 += ele
        else:
                str1 = "Geen items gevonden"
        # return string
        return str1
#tcdev()
while True:
        nu = int(datetime.utcnow().timestamp())
        if nu > TCupdate:
                query = listtostring(tcdev())
                TCupdate= nu # evt vertraagd met X seconde +60
                query = query.lower() #letop opensky werkt alleen met kleine letters!), hierom de query geforceerd klein
                print ("Aanvraag naar OpenSky: "+ query)
        try: #probeer openski te benaderen
                api = OpenSkyApi(OpenSky_user, OpenSky_Password)
                states = api.get_states(icao24=query)
                for s in states.states:
                        c_icao24 =  str(s.icao24)
                        try: #If fight online,  there is a time Position
                                tp = int(s.time_position)
                        except: #No Time, for error it is 1
                                tp = 1
                                print ("no time")
                        try: #If fight online,  there is a time Contact
                                tc = int(s.last_contact)
                        except: #No Time, for error it is 1
                                tc = 1
                                print ("no time")

                        if tc == 1: #If no time, no update
                                c_status  = False
                        else:
                                c_status = True

#ga alleen verder als het nuttig is, mogelijk overbodig omdat OpenSky geen calls doorgeeft als geen data
                        if c_status == True:
                                c_TC_id  =  'AIR-'+str(c_icao24)  #Identifier for Traccar
                                c_timestampPOS = datetime.utcfromtimestamp(tp).isoformat()
                                c_timestampCON = datetime.utcfromtimestamp(tc).isoformat()
                                c_longitude = s.longitude
                                c_latitude = s.latitude
                                c_heading = s.heading
                                c_rescount = s.position_source
                                c_ground = s.on_ground
                                if s.velocity == None: #snelheid bekend?
                                        c_speed = 0
                                else:
                                        c_speed = int(s.velocity)*1.94384449 #Snelheid omrekenen van M/s naar KN

                                if s.baro_altitude == None:  #Is Baro hoogte beschikbaar
                                        if s.geo_altitude == None: #Indien geen Baro dan GEO beschikbaar?
                                                c_altitude = 0 #Niets beschikbaar, dan 0
                                        else:
                                                c_altitude = int(s.geo_altitude)
                                else:
                                        c_altitude = int(s.baro_altitude)
                                TC_urlU = str(TCurl)+str(TCportU)+'/?id='+str(c_TC_id)+'&lat='+str(c_latitude)+'&lon='+str(c_longitude)+'&timestamp='+str(c_timestampPOS)+'Z&altitude='+str(c_altitude)+'&speed='+str(c_speed)+'&heading='+s$
                                print(str(c_TC_id)+' '+str(s.callsign)+'        '+str(c_latitude)+'     '+str(c_longitude)+'    '+str(c_timestampCON)+' '+str(c_timestampPOS)+' '+str(c_altitude)+'     '+str(c_speed)+'        '+str(c_head$
#                               print(TC_urlU)
                                try:
                                        urllib.request.urlopen(TC_urlU)
                                except Exception as e:
                                        print(str(e) + " A " + str(s.callsign))
                        else:
                                print ("Flight offline "+ str(s.icao24))
        except Exception as e:
                print(str(e))
        time.sleep(update)
