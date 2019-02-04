import time
import Spanner
from Testboard import Testboard
import urllib.request

HEATER = "D2"
FAN = "D4"
ROUTER = "D3"
THERMO2 = "D6"
THERMO_ON = "D5"
TEMPERATURE = "A4"

testboard = Testboard("testboard_name")

def cool_down():
    time.sleep(10)
   
    testboard.digitalWrite(FAN, 'HIGH')
    time.sleep(240)
    Spanner.assertTrue(1)

def cool_heatup():
    cnt=0
    while cnt < 5:
        testboard.digitalWrite(FAN, 'HIGH')
        testboard.digitalWrite(HEATER, 'HIGH')
        time.sleep(10)
        testboard.digitalWrite(FAN, 'LOW') 
        testboard.digitalWrite(HEATER, 'LOW')
        time.sleep(10)
        cnt=cnt+1	
    Spanner.assertTrue(1)
    
if __name__ == "__main__":
    print("Starting Access Point...", flush=True)
    testboard.digitalWrite(ROUTER, 'HIGH')
    time.sleep(40)
    print("Starting Thermostat...", flush=True)
    testboard.digitalWrite(THERMO2, 'HIGH')
    time.sleep(10)
    print("Switch Thermostat ON", flush=True)
    testboard.digitalWrite(THERMO_ON, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(THERMO_ON, 'LOW')
	
    cool_heatup()
    testboard.digitalWrite(HEATER, 'LOW')
    testboard.digitalWrite(FAN, 'LOW')	
    time.sleep(100)
	
    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
    
    Spanner.assertTrue(1)
