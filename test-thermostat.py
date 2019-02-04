import time
import Spanner
from Testboard import Testboard
import urllib.request

ROUTER = "D3"
THERMO2 = "D6"
THERMO_ON = "D5"
RELAY = "A3"

testboard = Testboard("testboard_name")

def set_temp_low():
    print("Set Temperature Low...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLowest").read()
    time.sleep(5)
    print("Wait 20 seconds...", flush=True)
    time.sleep(20)
	
    value = testboard.digitalRead(RELAY)
    cnt=0
    while value != 1.000:
        value = testboard.digitalRead(RELAY)
        print("Is relay OFF?", flush=True)
        if value == 0:
            print("Not yet", flush=True)    
        cnt = cnt + 1
        if cnt == 10:
            print("Relay is still ON - Give up", flush=True)
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        print("Relay is OFF", flush=True)	
        Spanner.assertTrue(1)

def set_temp_high():	
    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHighest").read()
    time.sleep(5)    
    print("Wait 20 seconds...", flush=True)
    time.sleep(15)
    
    print("Power on Access Point and wait for a minute", flush=True)
    testboard.digitalWrite(ROUTER, 'HIGH')	
    time.sleep(40)
    
    value = testboard.digitalRead(RELAY)
    cnt=0
    while value != 0:
        value = testboard.digitalRead(RELAY)
        print("Is relay ON?", flush=True)
        if value == 1:
            print("Not yet", flush=True)        		
        cnt = cnt + 1
        if cnt == 20:
            print("Relay is still OFF - Give up", flush=True)		
            break
        time.sleep(2)
    if cnt == 20:
        Spanner.assertTrue(0)
    else:
        print("Relay is ON", flush=True)	
        Spanner.assertTrue(1)
    	
if __name__ == "__main__":
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=login_correct").read()	
    print("Starting Access Point and wait for a minute...", flush=True)
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
    print("Power off Access Point...", flush=True)
    testboard.digitalWrite(ROUTER, 'LOW')	
    set_temp_high()

    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
