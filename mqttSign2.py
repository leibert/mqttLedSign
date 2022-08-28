#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

line1 = "Test Line 1"
line2 = "Test Line 2"

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/4x6.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            # len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            # pos -= 1
            # if (pos + len < 0):
            #     pos = offscreen_canvas.width
            graphics.DrawText(offscreen_canvas, font, 42, 6, textColor,line1)
            graphics.DrawText(offscreen_canvas, font, 72, 13, textColor,line2)
            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
