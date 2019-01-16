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
RELAY1 = "D4"
RELAY2 = "D2"
RELAY3 = "D3"
TEMPERATURE = "A4"

#gets the current temperature
def get_temperature():
    value = testboard.analogRead(TEMPERATURE)
    voltage = (3.3 * value) / 4096
    return (voltage - 0.5) * 100
    
def toggle_digital_output():
    print("get temperature...")
    temperature = get_temperature()
    print("temperature= ","%.1f" % temperature)
    
    # set PIN state
    testboard.digitalWrite(RELAY1, 'HIGH')
    time.sleep(2)
    testboard.digitalWrite(RELAY1, 'LOW')
    
    testboard.digitalWrite(RELAY2, 'HIGH')
    time.sleep(2)
    testboard.digitalWrite(RELAY2, 'LOW')
    
    testboard.digitalWrite(RELAY3, 'HIGH')
    time.sleep(2)
    testboard.digitalWrite(RELAY3, 'LOW')
    Spanner.assertTrue(1)

if __name__ == "__main__":
    toggle_digital_output()
