import os
import time

class PWM:
    PIN_LEFT_FORWARD = 22
    PIN_RIGHT_FORWARD = 24
    PIN_LEFT_BACKWARD = 23
    PIN_RIGHT_BACKWARD = 25
    
    def __init__(self):
        self.pins = [PWM.PIN_LEFT_FORWARD, PWM.PIN_LEFT_BACKWARD, PWM.PIN_RIGHT_FORWARD, PWM.PIN_RIGHT_BACKWARD]
        self.values = [0, 0, 0, 0]
        self.koef = [1, 1, 1, 1]

    def update( self ):
        str = '; '.join((("%d=%.2f" % (self.pins[index], self.values[index] * self.koef[index] / 100)) for index, item in enumerate(self.values)))
        cmd = 'echo "'+str+'" > /dev/pi-blaster'
        print(cmd)
        os.system(cmd)
        
    def set(self, pin, value):
        try:
            index = self.pins.index(pin)
        except:
            pass
        self.values[index] = value


led = PWM()
led.set(PWM.PIN_LEFT_FORWARD, 0)
led.set(PWM.PIN_RIGHT_FORWARD, 0)
led.set(PWM.PIN_LEFT_BACKWARD, 0)
led.set(PWM.PIN_RIGHT_BACKWARD, 0)
led.update()


#while True:
#    led.set(PWM.PIN_LEFT_FORWARD, 0)
#    led.set(PWM.PIN_RIGHT_FORWARD, 0)
#    led.set(PWM.PIN_LEFT_BACKWARD, 100)
#    led.set(PWM.PIN_RIGHT_BACKWARD, 100)
#    led.update()
#    time.sleep(1)
#    led.set(PWM.PIN_LEFT_FORWARD, 100)
#    led.set(PWM.PIN_RIGHT_FORWARD, 100)
#    led.set(PWM.PIN_LEFT_BACKWARD, 0)
#    led.set(PWM.PIN_RIGHT_BACKWARD, 0)
#    led.update()
#    time.sleep(1)
#led = PWM(24)
#led.set(100)