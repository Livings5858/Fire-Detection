import paho.mqtt.client as mqtt
import base64

# MQTT 配置
broker = "192.168.3.100"  # 替换为你的MQTT broker地址
port = 1883
topic = "image/topic"

# 读取并编码图片
with open("image.jpg", "rb") as image_file:
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')

# 发布图片
def publish_image():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    client.publish(topic, encoded_image)
    client.disconnect()

publish_image()
