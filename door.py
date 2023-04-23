import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
class Actions:
    def __init__(self,gpio:int) -> None:
        self.gpio:int = gpio
        self.init:bool = False

class GdoorControl:
    def __init__(self):
        self.open = Actions(17)
        self.close = Actions(27)
        self.switch1 = Actions(22)
        self.switch2 = Actions(24)
        self.safe_time:float  = 1/10
        self.safe_time_limit = int( 5 / self.safe_time ) # 5 seconds
        self.counter_for_safe_limit = 5000

    def open_door(self):
        # when it aproximate the end will slow down the door until hitting the switch
        counter_for_safe = 0
        getout = False
         #make sure pind closed is closed
        self.turn_off_pin(self.close.gpio)
        while(True):
            self.turn_on_pin(self.open.gpio)
            if  self.pin_state(self.switch1.gpio) or getout :
                self.turn_off_pin(self.open.gpio)
                break
            time.sleep(1/1000)
            counter_for_safe += 1 

            if counter_for_safe > self.counter_for_safe_limit:
                counter_for_safe = 0
                while(True):
                    counter_for_safe += 1
                    time.sleep(self.safe_time)
                    if  self.pin_state(self.switch1.gpio):
                        self.turn_off_pin(self.open.gpio)
                        getout = True
                        break   
                    if counter_for_safe > self.safe_time_limit:                        
                        self.turn_off_pin(self.open.gpio)
                        getout = True
                        break
                    self.toggle_pin(self.open.gpio)
            self.turn_off_pin(self.open.gpio)
                

    def close_door(self):
        # when it aproximate the end will slow down the door until hitting the switch
        counter_for_safe = 0
        getout = False
        #make sure pind open is closed
        self.turn_off_pin(self.open.gpio)
        while(True):
            self.turn_on_pin(self.close.gpio)
            if  self.pin_state(self.switch2.gpio) or getout :
                self.turn_off_pin(self.close.gpio)
                break
            time.sleep(1/1000)
            counter_for_safe += 1 

            if counter_for_safe > self.counter_for_safe_limit:
                counter_for_safe = 0
                while(True):
                    counter_for_safe += 1
                    time.sleep(self.safe_time)
                    if  self.pin_state(self.switch2.gpio):
                        self.turn_off_pin(self.close.gpio)
                        getout = True
                        break   
                    if counter_for_safe > self.safe_time_limit:                        
                        self.turn_off_pin(self.close.gpio)
                        getout = True
                        break
                    self.toggle_pin(self.close.gpio)         
            self.turn_off_pin(self.close.gpio)
    
    def turn_off_pin(self,gpio):
        led_pin = gpio
        GPIO.setup(led_pin,GPIO.OUT)
        GPIO.output(led_pin,GPIO.HIGH)

    def turn_on_pin(self,gpio):
        led_pin = gpio
        GPIO.setup(led_pin,GPIO.OUT)
        GPIO.output(led_pin,GPIO.LOW)

    def pin_state(self,gpio) -> bool:
        GPIO.setup(gpio,GPIO.OUT)
        state = GPIO.input(gpio)
        return not state
    
    def toggle_pin(self,gpio):
        if not self.pin_state(gpio=gpio):
            self.turn_on_pin(gpio=gpio)
        else:
            self.turn_off_pin(gpio=gpio)

    def isOpen(self) -> bool:
        return random.choice([True, False])

    def count_the_number_of_clicks(self,gpio):
        while(True):
            state = gdc.pin_state(gpio)
            if state:
                self.clicks=+1

    
    def state_watcher(self,gpio):
        while(True):
            state = gdc.pin_state(gpio)
            # if state change to 1 , it means that the limit switch have been pressed
            if state:
                time.sleep(1/500)




if __name__ == "__main__":
    gdc = GdoorControl()
    """
    #gdc.toggle_pin(17)
    #gdc.toggle_pin(27)
    gdc.turn_off_pin(17)
    gdc.turn_off_pin(22)
    gdc.turn_off_pin(27)

    try:
        while True:
            state = gdc.pin_state(22)
            if not state:
                print(state)
            time.sleep(1/500)
    except KeyboardInterrupt:
        pass
    print("out")
    """

    """ Use case 1 
        usgin the 2 limit switchs as a way to detect that the door is opened
        will start with the door closed
        switch 1 in 0 means and switch 2 in 1 the door is closed
            proceed to activate realy conected to gpio open, deactivate when switch 1 change to 1
        switch 1 in 1 and switch 2 in 0  the door is opened
            proceed to activate realy conected to gpio open, deactivate when switch 2 change to 1
        """

    print(gdc.turn_off_pin(gdc.switch1.gpio))    
    print(gdc.pin_state(gdc.switch1.gpio))

    if not gdc.pin_state(gdc.switch1.gpio):
        # open the door, leave the pin or open the door open until siwtch1 change to true
        print("open")
        gdc.open_door()
    else:

        if gdc.pin_state(gdc.switch2.gpio):
            # open the door, leave the pin or open the door open until siwtch1 change to true
            print("close")
            gdc.close_door()

        
