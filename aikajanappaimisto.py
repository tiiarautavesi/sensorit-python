from pyb import I2C
import char_lcd
import binascii
from pyb import UART
from pyb import Pin, ADC

i2c2 = I2C(2, I2C.MASTER, baudrate=20000)

i2c2.mem_write(0xFF, 0x20, 0x0C) #Enable pull-ups
i2c2.mem_write(0xFF, 0x20, 0x00) #Set pins as inputs
i2c2.mem_write(0x00, 0x20, 0x14) #Drive outputs low
d = char_lcd.HD44780(i2c2)
#row1 DF, row2 FE, row3 FD, row4 F7 
#Reading COL1.. ???
#VALO JUTTUJA
i2 = I2C(1, I2C.MASTER, baudrate=50000)
ser = UART(6, 115200)
ser.init(115200, bits=8, parity=None, stop=1)
adc = ADC(Pin('X1'))
temp1 = 0

text = ""
typing = False	

def Valolampo():
	#i2.send(0x43, 0x39)
	#asd = i2.recv(1, 0x39)
	#test = asd[0]
	#step = test & 0x0F
	#chordnr = (test >> 4) & 0x07
	#i2.send(0x83, 0x39)
	#kanava2 = i2.recv(1, 0x39)
	#test2 = kanava2[0]
	#step2 = test2 & 0x0F 
	#chordnr2 = (test2 >> 4) & 0x07
	#countvalue2 = int(16.5 * (2**chordnr2 -1) + (step2 * (2**chordnr2)))
	#countvalue = int(16.5 * (2**chordnr -1) + (step * (2**chordnr)))
	#r = (countvalue2/countvalue)
	#lux = countvalue * 0.46 * (2.718281828**(-3.13*r))
	#lux =  round(lux)
	#print(lux)	
	#lux=str(lux)
	#d.set_line(0)
	#d.set_string("Light:")
	#d.set_line(1)
	#d.set_string(lux + " lux")
	#pyb.delay(2000)
	#ser.write(bytes(lux.encode('ascii')))
	x = ser.readline().decode('ascii').strip()
	print(x)
	if typing == False:
		d.set_line(0)
		d.set_string("Date and time:")
		d.set_line(1)
		d.set_string(x)
	#pyb.delay(100)
	#temp1 = adc.read()
	#jannite = (temp1/4095) * 3.3
	#vastus = (jannite * 1780) / (3.3 - jannite)
	#lampo = int(((vastus - 1922) / 78) * 5 + 20)
	#celsius= str(lampo)+" C"
	#if typing == False:
		#d.set_line(0)
		#d.set_string("Temperature:")
		#d.set_line(1)
		#d.set_string(celsius)

	

while True:
	i2c2.mem_write(0xEF, 0x20, 0x00) #0xEF == col1
	k1 = i2c2.mem_read(1, 0x20, 0x12)
	c1 = k1[0] & 0x2B

	i2c2.mem_write(0xBF, 0x20, 0x00) #0xBF == col2
	k2 = i2c2.mem_read(1, 0x20, 0x12)
	c2 = k2[0] & 0x2B

	i2c2.mem_write(0xFB, 0x20, 0x00) #0xFB == col3
	k3 = i2c2.mem_read(1, 0x20, 0x12)
	c3 = k3[0] & 0x2B
	
	if typing == False:
		Valolampo()
	

# 1=11
# 4=42
# 7=41
# *=35
	if c1==35:
			print("*")
			if typing == False:
				typing = True
				pyb.delay(100)
			elif typing == True:
				typing = False
				pyb.delay(100)
	
	if typing == True:
		if c1==11:		
			text += "1"
			pyb.delay(100)
		elif c1==42:
			text += "4"
			pyb.delay(100)
		elif c1==41:
			print("7")
			text += "7"
			pyb.delay(100)
		
		
		if c2==11:
			print("2")
			text += "2"
			pyb.delay(100)
		elif c2==42:
			print("5")
			text += "5"
			pyb.delay(100)
		elif c2==41:
			print("8")
			text += "8"
			pyb.delay(100)
		elif c2==35:
			print("0")
			text += "0"
			pyb.delay(100)
		
		if c3==11:
			print("3")
			text += "3"
			pyb.delay(100)
		elif c3==42:
			print("6")
			text += "6"
			pyb.delay(100)
		elif c3==41:
			print("9")
			text += "9"
			pyb.delay(100)
		elif c3==35:
			print("#")
			text = text[:-1]
	
	if typing == True:
		
		if(len(text) > 4):
			text = text[:-1]
	#if(int(text[:1]) > 2):
	#	text[:1] = "2"
		d.set_line(0)
		d.set_string("Set alarm:")
		d.set_line(1)
		d.set_string(text)	
		