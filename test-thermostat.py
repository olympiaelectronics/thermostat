import time
import Spanner
from Testboard import Testboard
import urllib.request

testboard = Testboard("testboard_name")

def perform_test():
    print("Set wrong password", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=login_wrong").read()
    time.sleep(15)
    Spanner.assertTrue(1)	
    print("Set correct password", flush=True)
    urllib.request.urlopen("https://wismart.io/sendgcmrequest.php?message=login_correct").read()
    time.sleep(15)	
    Spanner.assertTrue(1)
#start test   
if __name__ == "__main__":
    perform_test()
