from gb import Gameboy
from display import Display
import sys

def main(rom_file):
    game = Gameboy()
    disp = Display(game)
    game.load_rom(rom_file)
    def advance():
        game.step_frame()
        disp.update(game.gpu.pixels)
        disp.root.after(1, advance)
    disp.root.after(1, advance)
    disp.root.mainloop()

if __name__ == "__main__":
    rom = "Tetris.gb"
    if len(sys.argv) > 1:
        rom = sys.argv[1]
    main(rom)
