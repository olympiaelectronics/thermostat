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
RELAY = "A3"

testboard = Testboard("testboard_name")

def cool_heatup():
    cnt=0
    while cnt < 5:
        testboard.digitalWrite(FAN, 'HIGH')
        testboard.digitalWrite(HEATER, 'HIGH')
        time.sleep(15)
        testboard.digitalWrite(FAN, 'LOW') 
        testboard.digitalWrite(HEATER, 'LOW')
        time.sleep(5)
        cnt=cnt+1
        value = testboard.digitalRead(RELAY)
        print("value=","%.3f" % value, flush=True) 	
        if value==1:
            break
    
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
	
    time.sleep(1) 
    print("Set Temperature Low...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLow").read()
    print("Wait 30 seconds...", flush=True)
    time.sleep(30)

    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHigh").read()
    print("Wait 30 seconds...", flush=True)
    time.sleep(30)
	
    cool_heatup()
    testboard.digitalWrite(HEATER, 'LOW')
    testboard.digitalWrite(FAN, 'LOW')	
    
    value = testboard.digitalRead(RELAY)
    print("Is relay ON? value=","%.3f" % value, flush=True)    
    cnt=0
    while value != 1:
        print("Waiting...", flush=True)
        time.sleep(20)
        value = testboard.digitalRead(RELAY)
        print("Is relay ON? value=","%.3f" % value, flush=True)    	
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
   
