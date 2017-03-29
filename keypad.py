from pyb import Pin
from pyb import I2C


i2c2 = I2C(2, I2C.MASTER, baudrate=20000)

i2c2.mem_write(0xFF, 0x20, 0x0C) #Enable pull-ups
i2c2.mem_write(0xFF, 0x20, 0x00) #Set pins as inputs
i2c2.mem_write(0x00, 0x20, 0x14) #Drive outputs low

#row1 DF, row2 FE, row3 FD, row4 F7 
#Reading COL1.. ???
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
	
	
	

# 1=11
# 4=42
# 7=41
# *=35
	if c1==11:
		print("1")
		pyb.delay(200)
	elif c1==42:
		print("4")
		pyb.delay(200)
	elif c1==41:
		print("7")
		pyb.delay(200)
	elif c1==35:
		print("*")
		pyb.delay(200)
		
	if c2==11:
		print("2")
		pyb.delay(200)
	elif c2==42:
		print("5")
		pyb.delay(200)
	elif c2==41:
		print("8")
		pyb.delay(200)
	elif c2==35:
		print("0")
		pyb.delay(200)
		
	if c3==11:
		print("3")
		pyb.delay(200)
	elif c3==42:
		print("6")
		pyb.delay(200)
	elif c3==41:
		print("9")
		pyb.delay(200)
	elif c3==35:
		print("#")
		pyb.delay(200)