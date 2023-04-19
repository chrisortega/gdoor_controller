import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class GdoorControl:
    def __init__(self):
        pass

    def turn_off_pin(self,gpio):
        led_pin = gpio
        GPIO.setup(led_pin,GPIO.OUT)
        GPIO.output(led_pin,GPIO.HIGH)

    def turn_on_pin(self,gpio):
        led_pin = gpio
        GPIO.setup(led_pin,GPIO.OUT)
        GPIO.output(led_pin,GPIO.LOW)

    def pin_state(self,gpio):
        GPIO.setup(gpio,GPIO.OUT)
        state = GPIO.input(gpio)
        return state | False
    
    def toggle_pin(self,gpio):
        if self.pin_state(gpio=gpio):
            self.turn_on_pin(gpio=gpio)
        else:
            self.turn_off_pin(gpio=gpio)

if __name__ == "__main__":
    gdc = GdoorControl()
    gdc.toggle_pin(17)
    gdc.toggle_pin(22)

