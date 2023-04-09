import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class GdoorControl:
    def __init__(self):
        self.door_state_gpio = {
            "open":17,
            "close":18,
            "sensor_open":4,
            "sensor_close":5
        }

    def turn_off_pin(self,gpio = 17):
        led_pin = gpio
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.output(led_pin, GPIO.HIGH)
        

    def turn_on_pin(self,gpio = 17):
        led_pin = gpio
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.output(led_pin, GPIO.LOW)

    def pin_state(self,gpio = 17):
        GPIO.setup(gpio, GPIO.OUT)
        state = GPIO.input(gpio)
        return state | False
    
    def toggle_pin(self,gpio = 17):
        if self.pin_state(gpio=gpio):
            self.turn_on_pin(gpio=gpio) 
        else:
            self.turn_off_pin(gpio=gpio)
            
if __name__ == "__main__":
    gdc = GdoorControl()
    gdc.toggle_pin(gpio=17)
    
    #led_pin = 17
    #GPIO.setup(led_pin, GPIO.OUT)

    #while True:
    #    GPIO.output(led_pin, GPIO.HIGH) # turn on the LED
    #    time.sleep(1/10)                   # wait for 1 second
    #    GPIO.output(led_pin, GPIO.LOW)  # turn off the LED
    #    time.sleep(1/10)                   # wait for 1 second
