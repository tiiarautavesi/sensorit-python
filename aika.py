import datetime
import time
import serial

ser = serial.Serial('/dev/ttyAMA0',115200, timeout = 0.5)  # open serial port
print(ser.name)
while True:
	localtime = time.localtime()
	d =str( localtime.tm_mday)
	mon = str(localtime.tm_mon)
	h = str( localtime.tm_hour)
	m = str( localtime.tm_min).zfill(2)
	now = datetime.datetime.now()
	aika = (d+"."+mon+" "+h+":"+m+"\n")
	ser.write(bytes(aika.encode('ascii')))	
	time.sleep(0.5)
	print(now.hour)  
