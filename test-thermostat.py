import time
import Spanner
from Testboard import Testboard
import urllib.request

ROUTER = "D3"
THERMO2 = "D6"
THERMO_ON = "D5"
RELAY = "A3"

testboard = Testboard("testboard_name")

def is_relay_on():
    value = testboard.digitalRead(RELAY)
    if value == 0:
        return 1
    else:
        return 0

def set_temp_low():
    print("Set Temperature Low...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLowest").read()
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)
	
    value = is_relay_on()
    print("Is relay OFF?", flush=True)
    if value != 0:
        print("Not yet", flush=True)   
    cnt=0
    while value != 0:
        value = is_relay_on()
        print("Is relay OFF?", flush=True)
        if value != 0:
            print("Not yet", flush=True)    
        cnt = cnt + 1
        if cnt == 10:
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        print("OK", flush=True) 	
        Spanner.assertTrue(1)

def set_temp_high():
    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHighest").read()
    
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)
    
    value = is_relay_on()
    print("Is relay ON?", flush=True)
    if value != 1:
        print("Not yet", flush=True)   
	
    cnt=0
    while value != 1:
        value = is_relay_on()
        print("Is relay ON?", flush=True)
        if value != 1:
            print("Not yet", flush=True)      
        cnt = cnt + 1
        if cnt == 10:
            Spanner.assertTrue(0)
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        print("OK", flush=True) 
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
	
    set_temp_low()
    set_temp_high()
    set_temp_low()
    
    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
    Spanner.assertTrue(1)
