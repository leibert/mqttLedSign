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






textColor = graphics.Color(0, 0, 255)


def on_message(client, userdata, msg):
    global textColor
    

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    if topic == "ledSign/line1":
        run_text.line1 = msg.payload.decode()
        print("updated line1 to: "+ line1)

    elif topic == "ledSign/line2":
        run_text.line2 = msg.payload.decode()
        print("updated line2 to: "+ line2)

    elif topic == "ledSign/line3":
        run_text.line2 = msg.payload.decode()
        print("updated line3 to: "+ line3)

    elif topic == "ledSign/color":
        color = msg.payload.decode()
        print("updated color to: "+ line2)
        a,b,c = color.split(',')
        print(a)
        print(b)
        print(c)
        textColor = graphics.Color(a, b, c)
    elif topic == "ledSign/mode":
        run_text.mode = msg.payload.decode()
    elif topic == "ledSign/message/type":
        run_text.messageType=msg.payload.decode()
    elif topic == "ledSign/message/sender":
        run_text.messageSender=msg.payload.decode()
    elif topic == "ledSign/message/text":
        run_text.messageText=msg.payload.decode()
    
    
    run_text.newCommand=True


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("ledSign/#")



    

class RunSign(SampleBase):
    
    offscreen_canvas=None
    scrollCounter=0

    mode = "clock"
    messageType = ""
    messageSender = ""
    messageText = ""

    newCommand= False


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
            # if datetime.now().second % 5 == 0:
            #     print(self.mode)
            #     print(self.messageType)
            time.sleep(0.1)
            self.offscreen_canvas.Clear()
            # self.offscreen_canvas.Clear()
            if self.mode == "clock":
                # time.sleep(0.15)
                self.clockLine()
            elif self.mode == "bigClock":
                self.bigClock()
            elif self.mode == "message":
                if self.newCommand:
                    print("FLSH")
                    print(self.messageType)
                    print(self.messageSender)
                    self.line1=self.messageType
                    self.line2=self.messageSender
                    self.line3=self.messageText
                    print(self.line1+"/"+self.line2+"/"+self.line3)
                    self.newCommand=False
                self.staticLine1()
                self.staticLine2()
                self.staticLine3()
            elif self.mode == "static":
                self.staticLine1()
                self.staticLine2()
                self.staticLine3()
            elif self.mode == "scroll":
                self.scrollCounter +=1 
                self.scrollLine1()
            
            offscreen_canvas=self.matrix.SwapOnVSync(self.offscreen_canvas)
    
    def bigClock(self):   
        graphics.DrawText(self.offscreen_canvas, font46, 17, 5, textColor, datetime.now().strftime('%A %b %d'))
        graphics.DrawText(self.offscreen_canvas, font714, 15, 16, textColor, datetime.now().strftime('%H:%M:%S'))

    def clockLine(self):
        graphics.DrawText(self.offscreen_canvas, font46, 6, 5, textColor, datetime.now().strftime('%a %m/%d   %H:%M:%S'))
        
    def staticLine1(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 5, textColor,(self.line1 or ""))

    def staticLine2(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 10, textColor,(self.line2 or ""))

    def staticLine3(self):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 15, textColor,(self.line3 or ""))

    def scrollLine1(self, delay=100, reset=False):
        self.line1pos, self.line1len
        if reset:
            self.line1pos = self.offscreen_canvas.width
        if self.scrollCounter % delay ==0:
            self.line1pos -= 1
            if (self.line1pos + self.line1len < 0):
                self.line1pos = self.offscreen_canvas.width

        self.line1len = graphics.DrawText(self.offscreen_canvas, font46, self.line1pos, 5, textColor, self.line1)
        
# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883)
    mqttLoop=client.loop_start()

    run_text = RunSign()
    if (not run_text.process()):
        run_text.print_help()
