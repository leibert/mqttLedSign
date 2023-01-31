# sudo python mqttSign.py --led-chain=3 --led-rows=16

import sys
sys.path.append('/home/pi/rpi-rgb-led-matrix/bindings/python')

from cgitb import text

from samples.samplebase import SampleBase
from rgbmatrix import graphics


# from samplebase import SampleBase
# from rgbmatrix import graphics
import paho.mqtt.client as mqtt
import time
from datetime import datetime

mqttBroker ="albany.local"
client = mqtt.Client("LED Sign")
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S")



#led sign setup
font46 = graphics.Font()
font46.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")


font57 = graphics.Font()
font57.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x7.bdf")
font58 = graphics.Font()
font58.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

font69 = graphics.Font()
font69.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x9.bdf")

font610 = graphics.Font()
font610.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")

font613B = graphics.Font()
font613B.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13B.bdf")

font714 = graphics.Font()
font714.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x14.bdf")

font714B = graphics.Font()
font714B.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x14B.bdf")


fontHR12 = graphics.Font()
fontHR12.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf")

fontclR612 = graphics.Font()
fontclR612.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/clR6x12.bdf")

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
    elif topic == "ledSign/EN":
        if (msg.payload.decode()=="OFF"):
            run_text.mode="OFF"
            client.publish("ledSign/mode","OFF")
        else:
            run_text.mode="bigClock"
            client.publish("ledSign/mode","bigClock")
            

    
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

    mode = "bigClock"
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
                    self.line1=self.messageType + " || " + self.messageSender
                    self.line2=self.messageText
                    print(self.line1+"/"+self.line2)
                    self.newCommand=False
                self.staticLine1(font=font58, color = graphics.Color(255, 0, 0))
                self.staticLine2(font=font610, color = graphics.Color(255, 255, 0))
                
            elif self.mode == "static":
                self.staticLine1()
                self.staticLine2()
                self.staticLine3()
            elif self.mode == "scroll":
                self.scrollCounter +=1 
                self.scrollLine1()
            else:
                self.offscreen_canvas.Clear()
            
            offscreen_canvas=self.matrix.SwapOnVSync(self.offscreen_canvas)
    
    def bigClock(self):   
        graphics.DrawText(self.offscreen_canvas, font46, 17, 5, graphics.Color(128, 128, ), datetime.now().strftime('%A %b %d').upper())
        graphics.DrawText(self.offscreen_canvas, fontHR12, 24, 16, graphics.Color(128, 128, 128), datetime.now().strftime('%H:%M:%S'))

    def clockLine(self):
        graphics.DrawText(self.offscreen_canvas, font46, 6, 5, textColor, datetime.now().strftime('%a %m/%d   %H:%M:%S'))
        
    def staticLine1(self, font=font58, color=textColor):
        graphics.DrawText(self.offscreen_canvas, font46, 0, 5, textColor,(self.line1 or ""))

    def staticLine2(self, font=font46, color=textColor):
        graphics.DrawText(self.offscreen_canvas, font, 0, 14, color,(self.line2 or ""))
        # graphics.DrawText(self.offscreen_canvas, font46, 0, 10, textColor,(self.line2 or ""))

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
