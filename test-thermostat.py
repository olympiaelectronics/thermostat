import time
import Spanner
from Testboard import Testboard
import urllib.request

HEATER = "D2"
FAN = "D4"
ROUTER = "D3"
THERMO2 = "D6"
THERMO_ON = "D5"
RELAY = "A3"
TEMPERATURE = "A4"

testboard = Testboard("testboard_name")

#get the current temperature.
def get_temperature():
    value = testboard.analogRead(TEMPERATURE)
    voltage = (3.3 * value) / 4096
    return (voltage - 0.5) * 100

def is_relay_on():
    value = testboard.digitalRead(RELAY)
    if value == 0:
        return 1
    else:
        return 0

def set_temp_low():
    time.sleep(10)
    print("Switch Thermostat ON", flush=True)
    testboard.digitalWrite(THERMO_ON, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(THERMO_ON, 'LOW')

    print("Set Temperature Low...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempLow").read()
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)
	
    value = is_relay_on()
    print("Is relay OFF?", flush=True)
    if value == 0:
        print("Not yet", flush=True)   
    cnt=0
    while value != 0:
        value = is_relay_on()
        print("Is relay OFF?", flush=True)
        if value == 0:
            print("Not yet", flush=True)    
        cnt = cnt + 1
        if cnt == 10:
            print("Ok Thermoastat is OFF", flush=True)
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        Spanner.assertTrue(1)
        
    print("get the temperature...", flush=True)
    temperature = get_temperature()
    print("current temperature = ","%.1f" % temperature)
    
    print("Cooling things down...", flush=True)
    testboard.digitalWrite(HEATER, 'LOW')

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
            
    #check whether relay is ON
    value = is_relay_on()
    print("Is relay ON?", flush=True)
    if value == 1:
        print("Not yet", flush=True)   
	
    cnt=0
    while value != 1:
        value = is_relay_on()
        print("Is relay ON?", flush=True)
        if value == 1:
            print("Not yet", flush=True)      
        cnt = cnt + 1
        if cnt == 3:
            Spanner.assertTrue(0)
            break
        time.sleep(2)
    if cnt == 3:
        Spanner.assertTrue(0)
    else:
        Spanner.assertTrue(1)
        
        
def set_temp_high():
    print("Set Temperature High...", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=change_setTempHigh").read()
    
    print("Wait 15 seconds...", flush=True)
    time.sleep(15)
    
    value = is_relay_on()
    print("Is relay ON?", flush=True)
    if value == 1:
        print("Not yet", flush=True)   
	
    cnt=0
    while value != 1:
        value = is_relay_on()
        print("Is relay ON?", flush=True)
        if value == 1:
            print("Not yet", flush=True)      
        cnt = cnt + 1
        if cnt == 10:
            Spanner.assertTrue(0)
            break
        time.sleep(2)
    if cnt == 10:
        Spanner.assertTrue(0)
    else:
        Spanner.assertTrue(1)
  
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
            
    #check whether relay is turned on        
    value = is_relay_on()
    print("Is relay OFF?", flush=True)
    if value == 0:
        print("Not yet", flush=True)   
    cnt=0
    while value != 0:
        value = is_relay_on()
        print("Is relay OFF?", flush=True)
        if value == 0:
            print("Not yet", flush=True)    
        cnt = cnt + 1
        if cnt == 3:
            print("Ok Thermoastat is OFF", flush=True)
            break
        time.sleep(2)
    if cnt == 3:
        Spanner.assertTrue(0)
    else:
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
	
    set_temp_high()
    set_temp_low()
    set_temp_high()
    
    testboard.digitalWrite(THERMO_ON, 'LOW')
    testboard.digitalWrite(ROUTER, 'LOW')
    testboard.digitalWrite(THERMO2, 'LOW')	
    testboard.digitalWrite(FAN, 'LOW')
    testboard.digitalWrite(HEATER, 'LOW') 
 
    Spanner.assertTrue(1)
