#!/usr/bin/env python
# Display a runtext with double-buffering.
from .samples.samplebase import SampleBase
from rgbmatrix import graphics
import time
import paho.mqtt.client as mqtt

mqttBroker ="albany.local"
client = mqtt.Client("LED Sign")
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S")
client.connect(mqttBroker, 1883)
client.loop_start()
line1 = "Line 1"
line2 = "line 2"


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def setup():
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../fonts/4x6.bdf")
        textColor = graphics.Color(255, 122, 0)
        pos = offscreen_canvas.width
#        my_text = self.args.text

    def run():
#        while True:
        offscreen_canvas.Clear()
        graphics.DrawText(offscreen_canvas, font, 42, 6, textColor,line1)
        graphics.DrawText(offscreen_canvas, font, 72, 13, textColor,line2)
#            pos -= 1
#            if (pos + len < 0):
 #               pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)



def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    if topic == "ledsign/line1":
        print("updating line")
        line1 = msg.payload.decode()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("ledsign/#")

# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
#    client.connect(mqttBroker, 1883)
    client.subscribe("ledsign/#")
    print("subscribed")
    run_test = RunText()
    run_text = RunText().setup()
    if (not run_text.process()):
        while(1):
            rc = client.loop()
            run_text.run(run_text)
