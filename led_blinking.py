from time import sleep
from gpiozero import LED, Button

led = LED(25)
button = Button(24)

while True:
	if button.is_pressed:
		for i in range (3):
        		led.on()
        		sleep(0.2)
        		led.off()
        		sleep(0.2)
