import paho.mqtt.client as mqtt
from fireDetection import detect_fire

BROKER = "localhost"
TOPIC = "image_data"
DONE_TOPIC = "image_send_done"
CHUNK_SIZE = 64

BASE_PATH = "D:\\code\\weihai\\code\\springboot-vue\\ui\\public\\"
imglist = ["nofire2.png", "fire2.png"]
index = 1

def publish_image_msg(client, fileName):
    msg_image_info = client.publish("image_path", fileName, qos=1)
    imageFullPath = BASE_PATH + fileName
    print (imageFullPath)
    if detect_fire(imageFullPath):
        msg_image_detect_info = client.publish("image_dectected", "fire", qos=1)
    else:
        msg_image_detect_info = client.publish("image_dectected", "nofire", qos=1)


image_data = {}
def on_message(client, userdata, msg):
    global index
    if msg.topic == TOPIC:
        # 接收数据并解析分段ID
        chunk_id = int(msg.payload[:4])
        data = msg.payload[5:]

        # 存储图像数据
        image_data[chunk_id] = data
    elif msg.topic == DONE_TOPIC:
        imgName = f"received_image_{index}.jpg"
        with open(BASE_PATH + imgName, "wb") as file:
            for i in sorted(image_data.keys()):
                file.write(image_data[i])
        print("Image received and saved as " + imgName)
        image_data.clear()
        publish_image_msg(client, imgName)
        index += 1

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe(TOPIC)
    client.subscribe(DONE_TOPIC)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER, 1883, 60)
client.loop_forever()
