import paho.mqtt.client as mqtt
import base64
from PIL import Image
import io

# MQTT 配置
broker = "192.168.3.66"
port = 1883
topic = "image/topic"

i = 0
# 处理接收到的消息
def on_message(client, userdata, message):
    global i
    encoded_image = message.payload.decode('utf-8')
    image_data = base64.b64decode(encoded_image)
    
    # 将字节数据转换为图片
    image = Image.open(io.BytesIO(image_data))
    image.show()  # 显示图片，或使用 image.save("received_image.jpg") 保存图片
    image.save("received_image"+ str(i) +".jpg")
    i+=1

# 订阅图片
def subscribe_image():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_forever()

subscribe_image()
