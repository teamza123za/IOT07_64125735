from flask import Flask, jsonify, render_template
import requests
from paho.mqtt import client as mqtt_client

broker = "192.168.110.104"
port = 1883

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("server")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

app = Flask(__name__)
server_ip = "http://192.168.110.104:4000"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thingspeak")
def thingspeak():
    headers = {'Accept': 'application/json'}
    url = "https://thingspeak.com/channels/1871825/field/1.json"
    r = requests.get(url, headers=headers)
    return jsonify(r.json())

@app.route("/nodemcu/last")
def nodemcu():
    headers = {'Accept': 'application/json'}
    r = requests.get(server_ip+'/sensors?_sort=id&_order=desc&_limit=1', headers=headers)
    return jsonify(r.json())

@app.route("/nodemcu/led/on")
def led_on():
    client = connect_mqtt()
    client.loop_start()
    result = client.publish("led", "0")
    client.loop_stop()
    return "OK"

@app.route("/nodemcu/led/off")
def led_off():
    client = connect_mqtt()
    client.loop_start()
    result = client.publish("led", "1")
    client.loop_stop()
    return "OK"

if __name__ == "__main__":
    client = connect_mqtt()
    app.run(host='0.0.0.0', debug=True)
