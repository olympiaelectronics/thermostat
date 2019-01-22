# This example will set one of our Testboard's outputs, first to HIGH, and then
# to LOW.
#
# The goal of this example is to show you how you can drive a digital input on
# your device from the Testboard.
#
# In our particular example, we are only setting value and not asserting
# anything. Of course this would never be a real world example, it's only for
# educational purposes

import time
import Spanner
from Testboard import Testboard

testboard = Testboard("testboard_name")

# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
FAN = "D3"
HEATER = "D2"
ROUTER = "D4"
TEMPERATURE = "A4"

#get the current temperature
def get_temperature():
    value = testboard.analogRead(TEMPERATURE)
    voltage = (3.3 * value) / 4096
    return (voltage - 0.5) * 100
    
def perform_test():
    print("Starting Access Point...", flush=True)
    testboard.digitalWrite(ROUTER, 'HIGH')
    
    print("get the temperature...", flush=True)
    temperature = get_temperature()
    print("current temperature = ","%.1f" % temperature)
    
    print("Heating things up...", flush=True)
    highTemperature = temperature + 2
    # set PIN state
    testboard.digitalWrite(HEATER, 'HIGH')
    time.sleep(2)
    testboard.digitalWrite(FAN, 'HIGH')
    cnt=0
    while temperature < highTemperature:
        time.sleep(2)
        temperature = get_temperature()
        print("temperature = ","%.1f" % temperature, flush=True)
        cnt=cnt+1
        if(cnt>20):
            print("exited due to timeout")
            break
    
    testboard.digitalWrite(HEATER, 'LOW')
    
    print("Cooling things down...", flush=True)
    lowTemperature = temperature - 2
    cnt=0
    while temperature > lowTemperature:
        time.sleep(2)
        temperature = get_temperature()
        print("temperature = ","%.1f" % temperature, flush=True)
        cnt=cnt+1
        if(cnt>20):
            print("exited due to timeout")
            break
            
    testboard.digitalWrite(FAN, 'LOW')
    
    Spanner.assertTrue(1)

if __name__ == "__main__":
    perform_test()
