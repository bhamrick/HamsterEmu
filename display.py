import Tkinter as Tk
import StringIO
import base64

class Display(object):
    def __init__(self, gb_obj):
        self.root = Tk.Tk()
        self.root.geometry('160x144')
        self.root.title("Hamster Boy")
        self.label_image = None

        self.pim = Tk.PhotoImage(width = 160, height = 144)
        self.label_image = Tk.Label(self.root, image=self.pim)
        self.label_image.place(x=0, y=0, width=160, height=144)

        self.root.bind("<KeyPress>", self.keyPressed)
        self.root.bind("<KeyRelease>", self.keyReleased)

        self.gb = gb_obj

    def update(self, pixels):
        color_map = {
            0: "#FFFFFF",
            1: "#AAAAAA",
            2: "#555555",
            3: "#000000",
            }
        lines = ["{%s}" % ' '.join(color_map[p] for p in pix_row) for pix_row in pixels]
        self.pim.put(' '.join(lines))

    def keyPressed(self, event):
        if event.keysym == 'Right':
            self.gb.joypad.right = True
        elif event.keysym == 'Left':
            self.gb.joypad.left = True
        elif event.keysym == 'Up':
            self.gb.joypad.up = True
        elif event.keysym == 'Down':
            self.gb.joypad.down = True
        elif event.keysym == 'z':
            self.gb.joypad.A = True
        elif event.keysym == 'x':
            self.gb.joypad.B = True
        elif event.keysym == 'Return':
            self.gb.joypad.start = True
        elif event.keysym == 'BackSpace':
            self.gb.joypad.select = True

    def keyReleased(self, event):
        if event.keysym == 'Right':
            self.gb.joypad.right = False
        elif event.keysym == 'Left':
            self.gb.joypad.left = False
        elif event.keysym == 'Up':
            self.gb.joypad.up = False
        elif event.keysym == 'Down':
            self.gb.joypad.down = False
        elif event.keysym == 'z':
            self.gb.joypad.A = False
        elif event.keysym == 'x':
            self.gb.joypad.B = False
        elif event.keysym == 'Return':
            self.gb.joypad.start = False
        elif event.keysym == 'BackSpace':
            self.gb.joypad.select = False
