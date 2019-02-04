import time
import Spanner
from Testboard import Testboard
import urllib.request

ROUTER = "D3"


testboard = Testboard("testboard_name")

def perform_test():
    print("Starting Access Point and wait for a minute...", flush=True)
    testboard.digitalWrite(ROUTER, 'HIGH')
    time.sleep(120)
   
    Spanner.assertTrue(1)
    	
if __name__ == "__main__":
    perform_test()
