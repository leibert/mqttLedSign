#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import paho.mqtt.client as mqtt
import time

line1 = "Test Line 1"
line2 = "Test Line 2"

mqttBroker ="albany.local"
client = mqtt.Client("LED Sign")
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S")


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    if topic == "ledsign/line1":
        
        line1 = msg.payload.decode()
        print("updated line1 to: "+ line1)

    if topic == "ledsign/line2":
        line2 = msg.payload.decode()
        print("updated line1 to: "+ line2)

    # if topic == "ledsign/color":
    #     line2 = msg.payload.decode()
    #     print("updated line1 to: "+ line2)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("ledsign/#")





class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        global line1
        global line2
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 0)
        # pos = offscreen_canvas.width
        # my_text = self.args.text

        while True:
            #check for mqtt updates
            rc = client.loop()

            offscreen_canvas.Clear()
            # len = graphics.DrawText(offscreen_canvas, font, 20, 10, textColor, "ABBB")
            # pos -= 1
            # if (pos + len < 0):
            #     pos = offscreen_canvas.width
            graphics.DrawText(offscreen_canvas, font, 42, 6, textColor,line1)
            graphics.DrawText(offscreen_canvas, font, 72, 13, textColor,line2)
            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883)

    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
