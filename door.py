import RPi.GPIO as GPIO
import time
import random
import json
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class Actions:
    def __init__(self,gpio:int) -> None:
        self.gpio:int = gpio
        self.init:bool = False

class GdoorControl:
    def __init__(self):
        self.open = Actions(17)
        self.close = Actions(27)
        self.switch1 = Actions(22)
        self.switch2 = Actions(10)
        self.actie_time = 5
        self.safe_time:float  = 1/10
        self.safe_time_limit = int( self.actie_time / self.safe_time ) # 5 seconds
        self.panic_button = False
        self.counter_for_safe_limit = 5000
        GPIO.setup(self.switch2.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.switch1.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.switch1.gpio, GPIO.OUT)
        GPIO.output(self.switch1.gpio, 0)       # set an output port/pin value to 1/HIGH/True           
        GPIO.setup(self.switch2.gpio, GPIO.OUT)
        GPIO.output(self.switch2.gpio, 0)       # set an output port/pin value to 1/HIGH/True          
        self.actions = {"open":self.open.gpio,"close":self.close.gpio}

    def reinit(self):
        GPIO.setup(self.switch1.gpio, GPIO.OUT)
        GPIO.output(self.switch1.gpio, 0)       # set an output port/pin value to 1/HIGH/True           
        GPIO.setup(self.switch2.gpio, GPIO.OUT)
        GPIO.output(self.switch2.gpio, 0)       # set an output port/pin value to 1/HIGH/True    
    

    def any_sw(self):
        return   (self.switch_state(self.switch1.gpio) or self.switch_state(self.switch2.gpio))

    def calibration_routine(self,pin,switchpin,action):
        on_time = 1/10
        fz = .9
        while( not self.switch_state(self.switch1.gpio) and  not self.switch_state(self.switch2.gpio)):
            self.turn_on_pin(pin)
            time.sleep(on_time)
            if self.any_sw():
                self.turn_off_pin(pin)
                break
            self.turn_off_pin(pin)
            time.sleep(fz)
            if self.any_sw():
                self.turn_off_pin(pin)
                break
        self.setstate(action)   

    def deaceleration_routine(self,pin,switchpin):
        on_time = 1/10
        fz = .1
        while(fz <= 1):   
            if self.getstate()['state'] == 'panic':
                self.turn_off_pin(pin)         
                break
            if self.switch_state(switchpin) == True:
                break    
            self.turn_on_pin(pin)
            time.sleep(on_time)
            self.turn_off_pin(pin)
            time.sleep(fz)
            if self.switch_state(switchpin) == True:
                break               
            fz+=.1


    def toggle_door(self,action = "open"):
        if self.getstate()['state'] == 'lock':
            return
        self.setstate("lock")
        divisor = 1000
        seconds = 3.5
        self.panic_button = False
        
        action_pin = self.actions[action]
        switchpin =self.switch2.gpio
        # when it aproximate the end will slow down the door until hitting the switch
        counter_for_safe = 0
        getout = False
         #make sure pind closed is closed
        if action == "open":
            self.turn_off_pin(self.close.gpio)
            switchpin =self.switch2.gpio
        elif action == "close":
            self.turn_off_pin(self.open.gpio)
            switchpin =self.switch1.gpio

        self.turn_on_pin(action_pin)
        
        while(True):
            if self.getstate()['state'] == 'panic':
                self.turn_off_pin(action_pin)
                time.sleep(1)
 
                break
            if self.switch_state(switchpin) == True or counter_for_safe > divisor * seconds :
                self.deaceleration_routine(action_pin,switchpin)
                self.turn_off_pin(action_pin)
       
                break        
            counter_for_safe+=1   
            time.sleep(1/divisor)


        self.setstate(action)
        return

    
    
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

    def switch_state(self,gpio):
        if GPIO.input(gpio) == GPIO.HIGH:
            return True
        return False

    def setstate(self,state):
        f = open("state.json","w+")
        f.write(json.dumps({"state":state}))
        f.close()

    def getstate(self):

        try:
            f = open("state.json", "r")
            return json.loads(f.read())
        except Exception as e:
            self.setstate("na")
            return self.getstate()
            
    def panic_button_on(self):
        GPIO.setup(self.switch1.gpio, GPIO.OUT)
        GPIO.output(self.switch1.gpio, 1)       # set an output port/pin value to 1/HIGH/True  
        GPIO.setup(self.switch2.gpio, GPIO.OUT)
        GPIO.output(self.switch2.gpio, 1)       # set an output port/pin value to 1/HIGH/True  

    def calibrate_sequence(self):
        if self.getstate()['state'] == 'open':
            self.calibration_routine(pin = self.actions["close"],switchpin=self.switch2.gpio,action = 'close')
        elif self.getstate()['state'] == 'close':
             self.calibration_routine(pin = self.actions["open"],switchpin=self.switch2.gpio,action = 'open')
        else:
            self.calibration_routine(pin = self.actions["open"],switchpin=self.switch2.gpio,action = 'open')   

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
    GPIO.setup(gdc.switch2.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(gdc.switch1.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True: # Run forever
        if GPIO.input(gdc.switch2.gpio) == GPIO.HIGH:
            print("closed!")

        if GPIO.input(gdc.switch1.gpio) == GPIO.HIGH:
            print("opened!")

    
        
