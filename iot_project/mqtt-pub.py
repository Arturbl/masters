import paho.mqtt.client as mqtt 
import time

broker_hostname = "localhost"
port = 1883 

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client("Client1")
# client.username_pw_set(username="user_name", password="password") # uncomment if you use password auth
client.on_connect=on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic = "idc/fitness"
msg_count = 0

msg = []
msg.append('[{"model":"fitness-KNN"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')
msg.append('[{"model":"fitness-GNB"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')
msg.append('[{"model":"fitness-SVC"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')
msg.append('[{"model":"fitness-DT"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')
msg.append('[{"model":"fitness-LR"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')
msg.append('[{"model":"fitness-LDA"},{"acceleration_x":0.2650,"acceleration_y":-0.7814,"acceleration_z":-0.0076,"gyro_x":-0.0590,"gyro_y":0.0325,"gyro_z":-2.9296}]')

try:
    while msg_count < len(msg):
        time.sleep(1)
        result = client.publish(topic, msg[msg_count])
        status = result[0]
        if status == 0:
            print("Message " + str(msg[msg_count]) + " is published to topic " + topic)
        else:
            print("Failed to send message to topic " + topic)
        msg_count += 1
finally:
    client.loop_stop()
