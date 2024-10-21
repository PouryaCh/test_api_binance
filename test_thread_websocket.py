import websocket
import json
import threading
import time

# Number of requests
num_requests = 500
received_messages = 0
lock = threading.Lock()  # Lock to prevent race conditions

# Function to process messages
def on_message(ws, message):
    global received_messages
    with lock:
        received_messages += 1  # Increment the count of received messages
        print(f"Received message {received_messages}: {message}")

# Function to handle errors
def on_error(ws, error):
    print(f"Error: {error}")

# Function to handle connection closure
def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

# Function to start the connection
def on_open(ws):
    print("Connection opened")
    # Send subscription message to receive trade data
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@trade",  # Example of a currency pair
        ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

# Binance WebSocket URL
socket_url = "wss://stream.binance.com:9443/ws"

# Start time
start_time = time.time()

# Create WebSocket
ws = websocket.WebSocketApp(socket_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Start connection
ws.on_open = on_open

# Run WebSocket in a separate thread
ws_thread = threading.Thread(target=ws.run_forever)
ws_thread.start()

# Wait until the number of requests is received
while received_messages < num_requests:
    time.sleep(0.1)  # Short sleep to check the message count

# Close the WebSocket
ws.close()

# End time and calculate total time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time for {num_requests} messages: {elapsed_time:.2f} seconds")
