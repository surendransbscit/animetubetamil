import threading
import time
import requests

def auto_get_request():
    while True:
        try:
            print("Auto GET calling /hello ...")
            res = requests.get("http://127.0.0.1:8000/hello/")
            print("Response:", res.text)
        except Exception as e:
            print("Error:", e)

        time.sleep(600)  # 10 minutes = 600 seconds

def start_auto_call():
    t = threading.Thread(target=auto_get_request)
    t.daemon = True
    t.start()
