import time
import Spanner
from Testboard import Testboard
import urllib.request

ROUTER = "D3"
THERMO2 = "D6"
THERMO_ON = "D5"
RELAY = "A3"

testboard = Testboard("testboard_name")

def perform_test():
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

    print("Set Temperature Low...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLowest").read()
    print("Wait 20 seconds...", flush=True)
    time.sleep(20)
	
    value = testboard.digitalRead(RELAY)
    cnt=0
    while value != 1.000:
        value = testboard.digitalRead(RELAY)
        print("Is relay ON? value=","%.3f" % value, flush=True)
        cnt = cnt + 1
        if cnt == 10:
            print("Ok Thermoastat is OFF", flush=True)
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
			
    print("Power off Access Point...", flush=True)
    testboard.digitalWrite(ROUTER, 'LOW')	
	
    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHighest").read()
    
    print("Wait 20 seconds...", flush=True)
    time.sleep(15)
    
    print("Power on Access Point...", flush=True)
    testboard.digitalWrite(ROUTER, 'HIGH')	
    time.sleep(40)
    
    value = testboard.digitalRead(RELAY)
    cnt=0
    while value != 0:
        value = testboard.digitalRead(RELAY)
        print("Is relay ON? value=","%.3f" % value, flush=True)
        cnt = cnt + 1
        if cnt == 30:
            Spanner.assertTrue(0)
            break
        time.sleep(2)
		
    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
    Spanner.assertTrue(1)
    	
if __name__ == "__main__":
    perform_test()
