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
import urllib.request

testboard = Testboard("testboard_name")

THERMO_ON = "D5"
THERMO2 = "D6"

def perform_test():
    print("Starting Thermostat...", flush=True)
    testboard.digitalWrite(THERMO2, 'HIGH')
    
    ###### POWER CONSUMPTION ######
    print("Measuring Power Consumption for 40 seconds keeping LCD off...", flush=True)
    # Start measuring power consumption
    testboard.startPowerMeasurement()
    # Measure for 40 seconds
    time.sleep(40)
    # Stop measuring power consumption
    testboard.stopPowerMeasurement()
    power = testboard.measuredPowerConsumption()
    print("power consumption (mA) = ","%.3f" % power, flush=True)
    Spanner.assertTrue(1)
    
    testboard.startPowerMeasurement()
    for x in range(8):
        print("Switch Thermostat ON "+str(x), flush=True)
        testboard.digitalWrite(THERMO_ON, 'HIGH')
        time.sleep(1)
        testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.stopPowerMeasurement()
    power = testboard.measuredPowerConsumption()
    print("power consumption (mA) = ","%.3f" % power, flush=True)
    Spanner.assertTrue(1)
# run test
if __name__ == "__main__":
    perform_test()
