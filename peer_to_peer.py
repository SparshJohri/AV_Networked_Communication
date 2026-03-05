#Required libraries (imported)
import socket
import threading
import json
import time

#Constants
BROADCAST_PORT = 5005
BUFFER_SIZE = 4096
NODE_NAME = input("Enter node name (e.g. car_001): ") #So that I can distinguish between different nodes

#1) Set up the socket for the outgoing connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#2) Bind the socket to the port for the outgoing connection
sock.bind(("", BROADCAST_PORT))


#3) Function that the listener thread has to run
def listen():
    
    #3a) Infinite loop to keep listening for incoming messages
    while True:

        #3a1) Receive the data from some sender
        data, (sender_ip, sender_port) = sock.recvfrom(BUFFER_SIZE)
        #We need "decode" to turn bytes into strings; json.loads converts strings to dictionaries (assuming we get a JSON object)
        msg = json.loads(data.decode())
        sender = msg.get("sender") #Use this instead of msg["sender"] to avoid KeyError if key not found
        text = msg.get("text") #Use this instead of msg["text"] to avoid KeyError if key not found

        #3a2) Ignore our own broadcasts
        if sender != NODE_NAME:

            #3a3) Ignore ACK messages not meant for us
            if ("ACK" in text):
                if (f"for {NODE_NAME}" in text):
                    print(f"\n[{NODE_NAME}] Received ACK from {sender}")
                
            #3a4) We got a regular message, so we should acknowledge it
            else:
                print(f"\n[{NODE_NAME}] Received broadcast from {sender}: {text}")
                response = {
                    "sender": NODE_NAME,
                    "text": f"ACK from {NODE_NAME} for {sender}",
                    "timestamp": time.time()
                }
                #Convert the response dictionary to a JSON string, encode it to bytes, and send it back to the original sender
                sock.sendto(json.dumps(response).encode(), (sender_ip, sender_port))


#4) Start the listener thread
threading.Thread(target=listen, daemon=True).start()

# ---------------------------------------------------------------------
print(f"[{NODE_NAME}] Type a message and press ENTER to broadcast it.")
print("Type 'exit' to quit.\n")
# ---------------------------------------------------------------------

#5) Loop to broadcast messages
while True:
    text = input("\n\n>> ")

    if text.lower() in ["exit", "quit"]:
        break
    elif ("ack" in text.lower()):
        print("This message has the word 'ack' in it; that is not allowed for user messages. Please try again.")
        continue

    message = {
        "sender": NODE_NAME,
        "text": text,
        "timestamp": time.time()
    }

    # Broadcast to LAN
    sock.sendto(json.dumps(message).encode(), ("<broadcast>", BROADCAST_PORT))
