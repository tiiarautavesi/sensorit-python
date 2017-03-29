from pyb import I2C
import char_lcd
import binascii
from pyb import UART
from pyb import Pin, ADC
#keycolons,lcd
i2c2 = I2C(2, I2C.MASTER, baudrate=20000)
i2c2.mem_write(0xFF, 0x20, 0x0C) #Enable pull-ups
i2c2.mem_write(0xFF, 0x20, 0x00) #Set pins as inputs
i2c2.mem_write(0x00, 0x20, 0x14) #Drive outputs low
d = char_lcd.HD44780(i2c2)

#light sensor,temperature,uart
i2 = I2C(1, I2C.MASTER, baudrate=50000)
ser = UART(6, 115200)
ser.init(115200, bits=8, parity=None, stop=1)
adc = ADC(Pin('X1'))
temp1 = 0
#buzzer/alarm
spk = Pin('X5', pyb.Pin.OUT_PP)


text = ""
aika = ""
x = ""
typing = False	
kaksoispiste = False
buttonpressed = False
lux = 300
spk.low()

#Measures temperature, shows it on display and turns on the buzzer
def Wakeup():
	temp1 = adc.read()
	jannite = (temp1/4095) * 3.3
	vastus = (jannite * 1780) / (3.3 - jannite)
	lampo = int(((vastus - 1922) / 78) * 5 + 20)
	celsius= "Temp: " + str(lampo)+" C"
	print("ALARM!!! ")	
	d.set_line(0)
	d.set_string("Good morning!")
	d.set_line(1)
	d.set_string(celsius)
	spk.high()
	pyb.delay(25)
	spk.low()	
	
#Measures and calculates lux value
def Light():
	i2.send(0x43, 0x39)
	asd = i2.recv(1, 0x39)
	test = asd[0]
	step = test & 0x0F
	chordnr = (test >> 4) & 0x07
	i2.send(0x83, 0x39)
	chanel2 = i2.recv(1, 0x39)
	test2 = chanel2[0]
	step2 = test2 & 0x0F 
	chordnr2 = (test2 >> 4) & 0x07
	countvalue2 = int(16.5 * (2**chordnr2 -1) + (step2 * (2**chordnr2)))
	countvalue = int(16.5 * (2**chordnr -1) + (step * (2**chordnr)))
	r = (countvalue2/countvalue)
	lux = countvalue * 0.46 * (2.718281828**(-3.13*r))
	lux =  round(lux)
	lux = int(lux)
	
	x = ser.readline().decode('ascii').strip()
	print(x)
	aika = x[5:10]
	print(aika)
	print(text)
	alarm = False
	
	#Check for wakeup call
	if aika == text:
		Wakeup()
		alarm = True
	if typing == False and alarm == False:		
		d.set_line(0)
		d.set_string("Date and time:")
		d.set_line(1)
		d.set_string(x)
		
	return lux
	

while True:
	#keyboard defined
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
		luxit = Light()
	


	buttonpressed = False
	colon = False
	if c1==35 and buttonpressed == False:
			print("*")			
			if typing == False:
				typing = True				
				buttonpressed = True
			elif typing == True:
				typing = False
				buttonpressed = True
			pyb.delay(200)	
	if typing == True:
		if c1==11 and buttonpressed == False:		
			text += "1"
			buttonpressed = True
		elif c1==42 and buttonpressed == False:
			text += "4"			
			buttonpressed = True
		elif c1==41 and buttonpressed == False:
			print("7")
			text += "7"			
			buttonpressed = True
		else:
			buttonpressed = False
		
		if c2==11 and buttonpressed == False:
			print("2")
			text += "2"
			buttonpressed = True
		elif c2==42 and buttonpressed == False:
			print("5")
			text += "5"
			buttonpressed = True
		elif c2==41 and buttonpressed == False:
			print("8")
			text += "8"
			buttonpressed = True
		elif c2==35 and buttonpressed == False:
			print("0")
			text += "0"
			buttonpressed = True
		else:
			buttonpressed = False
		
		if c3==11 and buttonpressed == False:
			print("3")
			text += "3"
			buttonpressed = True
		elif c3==42 and buttonpressed == False:
			print("6")
			text += "6"
			buttonpressed = True
		elif c3==41 and buttonpressed == False:
			print("9")
			text += "9"
			
			buttonpressed = True
		elif c3==35 and buttonpressed == False:
			print("#")
			
			if len(text) == 3:
				text = text[:-2]
			else:
				text = text[:-1]
			colon == True
			buttonpressed = True
		else:
			buttonpressed = False
	
	#Automatically adds a colon at 2 numbers and limit number of digits to 4 
	if typing == True:
		if(len(text) == 2) and colon == False:
			text += ":"
			colon = True
		if(len(text) > 5):
			text = text[:-1]
	
		d.set_line(0)
		d.set_string("Set alarm:")
		d.set_line(1)
		d.set_string(text)	
	
	print(luxit)
	#Delete wakeup time at a certain lux treshold
	if luxit > 250:
		text = text[:-5]
		print("off")
		spk.low()		
		alarm = False	
			