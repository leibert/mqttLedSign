#!/usr/bin/env python
# Display a runtext with double-buffering.
from cgitb import text
from samplebase import SampleBase
from rgbmatrix import graphics
import paho.mqtt.client as mqtt
import time
from datetime import datetime

mqttBroker ="albany.local"
client = mqtt.Client("LED Sign")
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S")



#led sign setup
font46 = graphics.Font()
font46.LoadFont("../../../fonts/4x6.bdf")
font714 = graphics.Font()
font714.LoadFont("../../../fonts/7x14.bdf")

#led sign properties
line1 = "Test Line 1"
line1pos=0
line1len=0
line2 = "Test Line 2"
line2pos=0
line2len=0
line3 = "Test Line 3"
line3pos=0
line3len=0

#mqtt variables
mode = "clock"
messageType = None
messageSender = None
messageText = None

newCommand = False


textColor = graphics.Color(0, 0, 255)


def on_message(client, userdata, msg):
    global mode
    global line1, line2, line3, textColor
    global messageType, messageSender, messageText

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    if topic == "ledsign/line1":
        line1 = msg.payload.decode()
        print("updated line1 to: "+ line1)

    elif topic == "ledsign/line2":
        line2 = msg.payload.decode()
        print("updated line2 to: "+ line2)

    elif topic == "ledsign/line3":
        line2 = msg.payload.decode()
        print("updated line3 to: "+ line3)

    elif topic == "ledsign/color":
        color = msg.payload.decode()
        print("updated color to: "+ line2)
        a,b,c = color.split(',')
        print(a)
        print(b)
        print(c)
        textColor = graphics.Color(a, b, c)
    elif topic == "ledsign/mode":
        mode = msg.payload.decode()
    elif topic == "ledsign/messageType":
        messageType=msg.payload.decode()
    elif topic == "ledsign/messageSender":
        messageSender=msg.payload.decode()
    elif topic == "ledsign/messageText":
        messageText=msg.payload.decode()
    


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("ledsign/#")



    

class RunSign(SampleBase):
    offscreen_canvas=None
    scrollCounter=0

    def __init__(self, *args, **kwargs):
        super(RunSign, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        print("A2")
        line1_pos = self.offscreen_canvas.width
        line2_pos = self.offscreen_canvas.width
        line3_pos = self.offscreen_canvas.width
        print("A3")
        # my_text = self.args.text

        while True:
            self.offscreen_canvas.Clear()

            if mode == "clock":
                self.clockLine()
            elif mode == "bigClock":
                self.bigClock()
            # if mode == "message"
            if mode == "static":
                self.staticLine1()
                self.staticLine2()
                self.staticLine3()
            if mode == "scroll":
                self.scrollLine1()
            
            self.scrollCounter +=1 
            offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            time.sleep(0.01)
    
    def bigClock(self):   
        graphics.DrawText(self.offscreen_canvas, font46, 17, 5, textColor, datetime.now().strftime('%A %b %d'))
        graphics.DrawText(self.offscreen_canvas, font714, 15, 16, textColor, datetime.now().strftime('%H:%M:%S'))

    def clockLine(self):
        graphics.DrawText(self.offscreen_canvas, font46, 6, 5, textColor, datetime.now().strftime('%a %m/%d   %H:%M:%S'))
        
    def staticLine1(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 5, textColor,line1)

    def staticLine2(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 10, textColor,line2)

    def staticLine3(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 15, textColor,line3)

    def scrollLine1(self, delay=100, reset=False):
        global line1pos, line1len
        if reset:
            line1pos = self.offscreen_canvas.width
        if self.scrollCounter % delay ==0:
            line1pos -= 1
            if (line1pos + line1len < 0):
                line1pos = self.offscreen_canvas.width

        line1len = graphics.DrawText(self.offscreen_canvas, font46, line1pos, 5, textColor, line1)
        
# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883)
    mqttLoop=client.loop_start()

    run_text = RunSign()
    if (not run_text.process()):
        run_text.print_help()
