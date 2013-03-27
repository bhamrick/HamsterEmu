from gb import Gameboy
from display import Display

def main(rom_file):
    game = Gameboy()
    disp = Display()
    game.load_rom(rom_file)
    def advance():
        game.step_frame()
        print game.cpu.clock / 70224
        disp.update(game.gpu.pixels)
        disp.root.after(500, advance)
    disp.root.after(500, advance)
    disp.root.mainloop()

if __name__ == "__main__":
    main("test1/TESTGAME.GB")
