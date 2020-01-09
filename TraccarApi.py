print(str(c_TC_id)+' '+str(s.callsign)+'        '+str(c_latitude)+'     '+str(c_longitude)+'    '+str(c_timestampCON)+' '+str(c_timestampPOS)+' '+str(c_altitude)+'     '+str(c_speed)+'        '+str(c_head$
print(TC_urlU)
try:
urllib.request.urlopen(TC_urlU)
except Exception as e:
print(str(e) + " A " + str(s.callsign))
