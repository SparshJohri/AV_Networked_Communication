import requests
import time

# replace with server IP if remote
SERVER_URL = "http://127.0.0.1:5000"  

def send_message(sender, text):
    payload = {
        "sender": sender,
        "text": text
    }
    r = requests.post(f"{SERVER_URL}/send", json=payload)
    print("Server response:", r.json())

def get_messages():
    r = requests.get(f"{SERVER_URL}/messages")
    return r.json()

if __name__ == "__main__":
    car_num = 0
    while True:
        send_message("car_"+str(car_num), "Hello from the client!")
        print("All messages:", get_messages())
        time.sleep(5)
        car_num += 1
