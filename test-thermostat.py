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
RELAY = "D7"

testboard = Testboard("testboard_name")

def cool_down():
    time.sleep(10)
   
    testboard.digitalWrite(FAN, 'HIGH')
    time.sleep(240)
    Spanner.assertTrue(1)

def cool_heatup():
    cnt=0
    while cnt < 3:
        testboard.digitalWrite(FAN, 'HIGH')
        testboard.digitalWrite(HEATER, 'HIGH')
        time.sleep(10)
        testboard.digitalWrite(FAN, 'LOW') 
        testboard.digitalWrite(HEATER, 'LOW')
        time.sleep(5)
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
 
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLowest").read()
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)

    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHigh").read()
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)
	
    cool_heatup()
    testboard.digitalWrite(HEATER, 'LOW')
    testboard.digitalWrite(FAN, 'LOW')	
    
    value = testboard.digitalRead(RELAY)
    cnt=0
    while value != 1:
         print("Waiting...", flush=True)		
        time.sleep(20)
	value = testboard.digitalRead(RELAY)		
	cnt=cnt+1
        if cnt == 10:
            break

    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        Spanner.assertTrue(1)
	
    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
   
