from pyb import I2C
import char_lcd
import binascii
from pyb import Pin, ADC

#i2c = I2C(2, I2C.MASTER, baudrate=20000)
#d = char_lcd.HD44780(i2c)
i2c = I2C(1, I2C.MASTER, baudrate=50000)
#d.set_line(0)
#d.set_string("Light:")
#d.set_line(1)
#d.set_string("Bar")
while True:
	#39
	#i2c.scan()
	i2c.send(0x43, 0x39)
	asd = i2c.recv(1, 0x39)
	#valo = binascii.hexlify(asd)
	test = asd[0]
	step = test & 0x0F
	chordnr = (test >> 4) & 0x07
	
	#d.set_line(1)
	#d.set_string( asd )
	#print("chan1", asd[0])
	i2c.send(0x83, 0x39)
	kanava2 = i2c.recv(1, 0x39)
	test2 = kanava2[0]
	step2 = test2 & 0x0F
	chordnr2 = (test2 >> 4) & 0x07
	#valo2 = binascii.hexlify(kanava2)
	#print("chan2", kanava2[0])
	#print(chordnr)
	#print(step)
	countvalue2 = int(16.5 * (2**chordnr2 -1) + (step2 * (2**chordnr2)))
	countvalue = int(16.5 * (2**chordnr -1) + (step * (2**chordnr)))
	r = (countvalue2/countvalue)
	lux = countvalue * 0.46 * (2.718281828**(-3.13*r))
	print(lux)
	#print(countvalue)
	#print(countvalue2)
	pyb.delay(1000)