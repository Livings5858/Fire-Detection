import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "image_data"
DONE_TOPIC = "image_send_done"
CHUNK_SIZE = 64

image_data = {}
def on_message(client, userdata, msg):
    if msg.topic == TOPIC:
        # 接收数据并解析分段ID
        chunk_id = int(msg.payload[:4])
        data = msg.payload[5:]

        # 存储图像数据
        image_data[chunk_id] = data
    elif msg.topic == DONE_TOPIC:
        with open("received_image.jpg", "wb") as file:
            for i in sorted(image_data.keys()):
                file.write(image_data[i])
        print("Image received and saved as 'received_image.jpg'")
        image_data.clear()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)
    client.subscribe(DONE_TOPIC)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()