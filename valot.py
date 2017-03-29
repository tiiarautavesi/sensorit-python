# main.py -- put your code here!
import pyb
from pyb import LED
from pyb import Switch

sw = pyb.Switch()
led = LED(1) 
led2 = LED(2)
led3 = LED(3)
led4 = LED(4)

print("LED")

punainen = True
keltainen = False
vihrea = False
keltainen2 = False

#pyb.delay(5000)



while True:

	if sw() and punainen:
		led.on()
		led3.off()
		punainen = False
		keltainen = True
        pyb.delay(200)
	if sw() and keltainen:
		led.on()
		led3.on()
		
		keltainen = False
		vihrea = True
		pyb.delay(200)
	if sw() and vihrea:
		led2.on()
		led.off()
		led3.off()
		vihrea = False
		keltainen2 = True		
		pyb.delay(200)
	if sw() and keltainen2:
		led2.off()
		led3.on()
		keltainen2 = False
		punainen = True
		pyb.delay(200)