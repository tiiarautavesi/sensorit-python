from pyb import Pin, ADC

while True:
	adc = ADC(Pin('X3'))
	adc.read()
	testi = adc.read()
	print(testi)
	pyb.delay(1000)