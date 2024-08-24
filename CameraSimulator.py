import time
import paho.mqtt.client as mqtt
import random
from fireDetection import detect_fire

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect("localhost")

BASE_PATH = "D:\\code\\weihai\\code\\springboot-vue\\ui\\public\\"

imglist = ["nofire2.png", "fire2.png"]
index = 0
while True:
    mqttc.loop_start()

    # sensor
    # temperature = round(random.uniform(10, 50))
    # x = round(random.uniform(10, 50))
    # y = round(random.uniform(10, 50))
    # msg = f"{temperature},{x},{y}"
    # msg_sensor_info = mqttc.publish("sensor", msg, qos=1)
    # unacked_publish.add(msg_sensor_info.mid)
    # msg_sensor_info.wait_for_publish()

    # image
    msg_image_info = mqttc.publish("image_path", imglist[index], qos=1)
    unacked_publish.add(msg_image_info.mid)
    imageFullPath = BASE_PATH + imglist[index]
    print (imageFullPath)
    if detect_fire(BASE_PATH + imglist[index]):
        msg_image_detect_info = mqttc.publish("image_dectected", "fire", qos=1)
        unacked_publish.add(msg_image_detect_info.mid)
        msg_image_detect_info.wait_for_publish()
    else:
        msg_image_detect_info = mqttc.publish("image_dectected", "nofire", qos=1)
        unacked_publish.add(msg_image_detect_info.mid)
        msg_image_detect_info.wait_for_publish()
    index += 1
    if index >= len(imglist):
        index = 0
    msg_image_info.wait_for_publish()

    mqttc.loop_stop()
    time.sleep(5)

mqttc.disconnect()