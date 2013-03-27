import Tkinter as Tk
import StringIO
import base64

class Display(object):
    def __init__(self):
        self.root = Tk.Tk()
        self.root.geometry('160x144')
        self.root.title("Hamster Boy")
        self.label_image = None

        self.pim = Tk.PhotoImage(width = 160, height = 144)
        self.label_image = Tk.Label(self.root, image=self.pim)
        self.label_image.place(x=0, y=0, width=160, height=144)

    def update(self, pixels):
        color_map = {
            0: "#FFFFFF",
            1: "#AAAAAA",
            2: "#555555",
            3: "#000000",
            }
        lines = ["{%s}" % ' '.join(color_map[p] for p in pix_row) for pix_row in pixels]
        self.pim.put(' '.join(lines))
