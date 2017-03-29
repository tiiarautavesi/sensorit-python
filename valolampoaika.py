from pyb import I2C
import char_lcd
import binascii
from pyb import UART
from pyb import Pin, ADC
ser = UART(6, 115200)
ser.init(115200, bits=8, parity=None, stop=1)
i2c = I2C(2, I2C.MASTER, baudrate=20000)
d = char_lcd.HD44780(i2c)
i2 = I2C(1, I2C.MASTER, baudrate=50000)

adc = ADC(Pin('X1'))
temp1 = 0
#d.set_line(1)
#d.set_string("Bar")



while True:
	
	i2.send(0x43, 0x39)
	asd = i2.recv(1, 0x39)
	test = asd[0]
	step = test & 0x0F
	chordnr = (test >> 4) & 0x07
	i2.send(0x83, 0x39)
	kanava2 = i2.recv(1, 0x39)
	test2 = kanava2[0]
	step2 = test2 & 0x0F
	chordnr2 = (test2 >> 4) & 0x07
	countvalue2 = int(16.5 * (2**chordnr2 -1) + (step2 * (2**chordnr2)))
	countvalue = int(16.5 * (2**chordnr -1) + (step * (2**chordnr)))
	r = (countvalue2/countvalue)
	lux = countvalue * 0.46 * (2.718281828**(-3.13*r))
	lux =  round(lux)
	print(lux)	
	lux=str(lux)
	d.set_line(0)
	d.set_string("Light:")
	d.set_line(1)
	d.set_string(lux + " lux")
	pyb.delay(2000)
	#ser.write(bytes(lux.encode('ascii')))
	x = ser.readline().decode('ascii').strip()
	print(x)
	d.set_line(0)
	d.set_string("Date and time:")
	d.set_line(1)
	d.set_string(x)
	pyb.delay(2000)
	temp1 = adc.read()
	jannite = (temp1/4095) * 3.3
	vastus = (jannite * 1780) / (3.3 - jannite)
	lampo = int(((vastus - 1922) / 78) * 5 + 20)
	celsius= str(lampo)+" C"
	d.set_line(0)
	d.set_string("Temperature:")
	d.set_line(1)
	d.set_string(celsius)
	pyb.delay(2000)
	
	
	