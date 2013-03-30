import sys

class Gameboy:
    def __init__(self):
        self.cpu = gb_cpu()
        self.ram = self.cpu.ram
        self.gpu = gb_gpu(self.cpu, self.ram)
        self.joypad = gb_joypad()
        self.ram.joypad_obj = self.joypad

    def step_instruction(self):
        self.cpu.step()
        self.gpu.update(self.cpu.dt)

    def step_frame(self):
        end_clock = self.cpu.clock + 70224
        while self.cpu.clock < end_clock:
            self.step_instruction()

    def load_rom(self, fname):
        self.ram.load_rom(fname)

class Flags:
    Z = 0x80
    N = 0x40
    H = 0x20
    C = 0x10

class gb_cpu(object):
    def __init__(self):
        # Initialize registers
        self.A = 0x11
        self.B = 0x00
        self.D = 0xFF
        self.H = 0x01
        self.F = 0x80
        self.C = 0x00
        self.E = 0x56
        self.L = 0x4D
        self.SP = 0xFFFE
        self.PC = 0x100
        self.clock = 0
        self.dt = 0 # Amount of time spent on the last operation
        self.halted = False
        self.interrupts = False
        self.ram = gb_ram()

        self.timer_div_countdown = 256
        self.timer_counter_countdown = None

        # Debugging info
        self.used_ops = set()

        # Opcode format:
        # (arg_lengths, func, cycles), where arg_lengths is a tuple giving the byte length of each argument
        # cycles is the number of clock cycles the instruction takes
        self.opcodes = [
            ((), gb_cpu.op_00, 4),
            ((2,), gb_cpu.op_01, 12),
            ((), gb_cpu.op_02, 8),
            ((), gb_cpu.op_03, 8),
            ((), gb_cpu.op_04, 4),
            ((), gb_cpu.op_05, 4),
            ((1,), gb_cpu.op_06, 8),
            ((), gb_cpu.op_07, 4),
            ((2,), gb_cpu.op_08, 20),
            ((), gb_cpu.op_09, 8),
            ((), gb_cpu.op_0A, 8),
            ((), gb_cpu.op_0B, 8),
            ((), gb_cpu.op_0C, 4),
            ((), gb_cpu.op_0D, 4),
            ((1,), gb_cpu.op_0E, 8),
            ((), gb_cpu.op_0F, 4),
            ((1,), gb_cpu.op_10, 4),
            ((2,), gb_cpu.op_11, 12),
            ((), gb_cpu.op_12, 8),
            ((), gb_cpu.op_13, 8),
            ((), gb_cpu.op_14, 4),
            ((), gb_cpu.op_15, 4),
            ((1,), gb_cpu.op_16, 8),
            ((), gb_cpu.op_17, 4),
            ((1,), gb_cpu.op_18, 8),
            ((), gb_cpu.op_19, 8),
            ((), gb_cpu.op_1A, 8),
            ((), gb_cpu.op_1B, 8),
            ((), gb_cpu.op_1C, 4),
            ((), gb_cpu.op_1D, 4),
            ((1,), gb_cpu.op_1E, 8),
            ((), gb_cpu.op_1F, 4),
            ((1,), gb_cpu.op_20, 8),
            ((2,), gb_cpu.op_21, 12),
            ((), gb_cpu.op_22, 8),
            ((), gb_cpu.op_23, 8),
            ((), gb_cpu.op_24, 4),
            ((), gb_cpu.op_25, 4),
            ((1,), gb_cpu.op_26, 8),
            ((), gb_cpu.op_27, 4),
            ((1,), gb_cpu.op_28, 8),
            ((), gb_cpu.op_29, 8),
            ((), gb_cpu.op_2A, 8),
            ((), gb_cpu.op_2B, 8),
            ((), gb_cpu.op_2C, 4),
            ((), gb_cpu.op_2D, 4),
            ((1,), gb_cpu.op_2E, 8),
            ((), gb_cpu.op_2F, 4),
            ((1,), gb_cpu.op_30, 8),
            ((2,), gb_cpu.op_31, 12),
            ((), gb_cpu.op_32, 8),
            ((), gb_cpu.op_33, 8),
            ((), gb_cpu.op_34, 12),
            ((), gb_cpu.op_35, 12),
            ((1,), gb_cpu.op_36, 12),
            ((), gb_cpu.op_37, 4),
            ((1,), gb_cpu.op_38, 8),
            ((), gb_cpu.op_39, 8),
            ((), gb_cpu.op_3A, 8),
            ((), gb_cpu.op_3B, 8),
            ((), gb_cpu.op_3C, 4),
            ((), gb_cpu.op_3D, 4),
            ((1,), gb_cpu.op_3E, 8),
            ((), gb_cpu.op_3F, 4),
            ((), gb_cpu.op_40, 4),
            ((), gb_cpu.op_41, 4),
            ((), gb_cpu.op_42, 4),
            ((), gb_cpu.op_43, 4),
            ((), gb_cpu.op_44, 4),
            ((), gb_cpu.op_45, 4),
            ((), gb_cpu.op_46, 8),
            ((), gb_cpu.op_47, 4),
            ((), gb_cpu.op_48, 4),
            ((), gb_cpu.op_49, 4),
            ((), gb_cpu.op_4A, 4),
            ((), gb_cpu.op_4B, 4),
            ((), gb_cpu.op_4C, 4),
            ((), gb_cpu.op_4D, 4),
            ((), gb_cpu.op_4E, 8),
            ((), gb_cpu.op_4F, 4),
            ((), gb_cpu.op_50, 4),
            ((), gb_cpu.op_51, 4),
            ((), gb_cpu.op_52, 4),
            ((), gb_cpu.op_53, 4),
            ((), gb_cpu.op_54, 4),
            ((), gb_cpu.op_55, 4),
            ((), gb_cpu.op_56, 8),
            ((), gb_cpu.op_57, 4),
            ((), gb_cpu.op_58, 4),
            ((), gb_cpu.op_59, 4),
            ((), gb_cpu.op_5A, 4),
            ((), gb_cpu.op_5B, 4),
            ((), gb_cpu.op_5C, 4),
            ((), gb_cpu.op_5D, 4),
            ((), gb_cpu.op_5E, 8),
            ((), gb_cpu.op_5F, 4),
            ((), gb_cpu.op_60, 4),
            ((), gb_cpu.op_61, 4),
            ((), gb_cpu.op_62, 4),
            ((), gb_cpu.op_63, 4),
            ((), gb_cpu.op_64, 4),
            ((), gb_cpu.op_65, 4),
            ((), gb_cpu.op_66, 8),
            ((), gb_cpu.op_67, 4),
            ((), gb_cpu.op_68, 4),
            ((), gb_cpu.op_69, 4),
            ((), gb_cpu.op_6A, 4),
            ((), gb_cpu.op_6B, 4),
            ((), gb_cpu.op_6C, 4),
            ((), gb_cpu.op_6D, 4),
            ((), gb_cpu.op_6E, 8),
            ((), gb_cpu.op_6F, 4),
            ((), gb_cpu.op_70, 8),
            ((), gb_cpu.op_71, 8),
            ((), gb_cpu.op_72, 8),
            ((), gb_cpu.op_73, 8),
            ((), gb_cpu.op_74, 8),
            ((), gb_cpu.op_75, 8),
            ((), gb_cpu.op_76, 4),
            ((), gb_cpu.op_77, 8),
            ((), gb_cpu.op_78, 4),
            ((), gb_cpu.op_79, 4),
            ((), gb_cpu.op_7A, 4),
            ((), gb_cpu.op_7B, 4),
            ((), gb_cpu.op_7C, 4),
            ((), gb_cpu.op_7D, 4),
            ((), gb_cpu.op_7E, 8),
            ((), gb_cpu.op_7F, 4),
            ((), gb_cpu.op_80, 4),
            ((), gb_cpu.op_81, 4),
            ((), gb_cpu.op_82, 4),
            ((), gb_cpu.op_83, 4),
            ((), gb_cpu.op_84, 4),
            ((), gb_cpu.op_85, 4),
            ((), gb_cpu.op_86, 8),
            ((), gb_cpu.op_87, 4),
            ((), gb_cpu.op_88, 4),
            ((), gb_cpu.op_89, 4),
            ((), gb_cpu.op_8A, 4),
            ((), gb_cpu.op_8B, 4),
            ((), gb_cpu.op_8C, 4),
            ((), gb_cpu.op_8D, 4),
            ((), gb_cpu.op_8E, 8),
            ((), gb_cpu.op_8F, 4),
            ((), gb_cpu.op_90, 4),
            ((), gb_cpu.op_91, 4),
            ((), gb_cpu.op_92, 4),
            ((), gb_cpu.op_93, 4),
            ((), gb_cpu.op_94, 4),
            ((), gb_cpu.op_95, 4),
            ((), gb_cpu.op_96, 8),
            ((), gb_cpu.op_97, 4),
            ((), gb_cpu.op_98, 4),
            ((), gb_cpu.op_99, 4),
            ((), gb_cpu.op_9A, 4),
            ((), gb_cpu.op_9B, 4),
            ((), gb_cpu.op_9C, 4),
            ((), gb_cpu.op_9D, 4),
            ((), gb_cpu.op_9E, 8),
            ((), gb_cpu.op_9F, 4),
            ((), gb_cpu.op_A0, 4),
            ((), gb_cpu.op_A1, 4),
            ((), gb_cpu.op_A2, 4),
            ((), gb_cpu.op_A3, 4),
            ((), gb_cpu.op_A4, 4),
            ((), gb_cpu.op_A5, 4),
            ((), gb_cpu.op_A6, 8),
            ((), gb_cpu.op_A7, 4),
            ((), gb_cpu.op_A8, 4),
            ((), gb_cpu.op_A9, 4),
            ((), gb_cpu.op_AA, 4),
            ((), gb_cpu.op_AB, 4),
            ((), gb_cpu.op_AC, 4),
            ((), gb_cpu.op_AD, 4),
            ((), gb_cpu.op_AE, 8),
            ((), gb_cpu.op_AF, 4),
            ((), gb_cpu.op_B0, 4),
            ((), gb_cpu.op_B1, 4),
            ((), gb_cpu.op_B2, 4),
            ((), gb_cpu.op_B3, 4),
            ((), gb_cpu.op_B4, 4),
            ((), gb_cpu.op_B5, 4),
            ((), gb_cpu.op_B6, 8),
            ((), gb_cpu.op_B7, 4),
            ((), gb_cpu.op_B8, 4),
            ((), gb_cpu.op_B9, 4),
            ((), gb_cpu.op_BA, 4),
            ((), gb_cpu.op_BB, 4),
            ((), gb_cpu.op_BC, 4),
            ((), gb_cpu.op_BD, 4),
            ((), gb_cpu.op_BE, 8),
            ((), gb_cpu.op_BF, 4),
            ((), gb_cpu.op_C0, 8),
            ((), gb_cpu.op_C1, 12),
            ((2,), gb_cpu.op_C2, 12),
            ((2,), gb_cpu.op_C3, 12),
            ((2,), gb_cpu.op_C4, 12),
            ((), gb_cpu.op_C5, 16),
            ((1,), gb_cpu.op_C6, 8),
            ((), gb_cpu.op_C7, 32),
            ((), gb_cpu.op_C8, 8),
            ((), gb_cpu.op_C9, 8),
            ((2,), gb_cpu.op_CA, 12),
            ((1,), gb_cpu.op_CB, 8),
            ((2,), gb_cpu.op_CC, 12),
            ((2,), gb_cpu.op_CD, 12),
            ((1,), gb_cpu.op_CE, 8),
            ((), gb_cpu.op_CF, 32),
            ((), gb_cpu.op_D0, 8),
            ((), gb_cpu.op_D1, 12),
            ((2,), gb_cpu.op_D2, 12),
            ((), gb_cpu.op_D3, 0),
            ((2,), gb_cpu.op_D4, 12),
            ((), gb_cpu.op_D5, 16),
            ((1,), gb_cpu.op_D6, 8),
            ((), gb_cpu.op_D7, 32),
            ((), gb_cpu.op_D8, 8),
            ((), gb_cpu.op_D9, 8),
            ((2,), gb_cpu.op_DA, 12),
            ((), gb_cpu.op_DB, 0),
            ((2,), gb_cpu.op_DC, 12),
            ((), gb_cpu.op_DD, 0),
            ((1,), gb_cpu.op_DE, 8),
            ((), gb_cpu.op_DF, 32),
            ((1,), gb_cpu.op_E0, 12),
            ((), gb_cpu.op_E1, 12),
            ((), gb_cpu.op_E2, 8),
            ((), gb_cpu.op_E3, 0),
            ((), gb_cpu.op_E4, 0),
            ((), gb_cpu.op_E5, 16),
            ((1,), gb_cpu.op_E6, 8),
            ((), gb_cpu.op_E7, 32),
            ((1,), gb_cpu.op_E8, 16),
            ((), gb_cpu.op_E9, 4),
            ((2,), gb_cpu.op_EA, 16),
            ((), gb_cpu.op_EB, 0),
            ((), gb_cpu.op_EC, 0),
            ((), gb_cpu.op_ED, 0),
            ((1,), gb_cpu.op_EE, 8),
            ((), gb_cpu.op_EF, 32),
            ((1,), gb_cpu.op_F0, 12),
            ((), gb_cpu.op_F1, 12),
            ((), gb_cpu.op_F2, 8),
            ((), gb_cpu.op_F3, 4),
            ((), gb_cpu.op_F4, 0),
            ((), gb_cpu.op_F5, 16),
            ((1,), gb_cpu.op_F6, 8),
            ((), gb_cpu.op_F7, 32),
            ((1,), gb_cpu.op_F8, 12),
            ((), gb_cpu.op_F9, 8),
            ((2,), gb_cpu.op_FA, 16),
            ((), gb_cpu.op_FB, 4),
            ((), gb_cpu.op_FC, 0),
            ((), gb_cpu.op_FD, 0),
            ((1,), gb_cpu.op_FE, 8),
            ((), gb_cpu.op_FF, 32),
            ]
        self.extra_ops_table = [
            gb_cpu.op_CB_00, gb_cpu.op_CB_01, gb_cpu.op_CB_02, gb_cpu.op_CB_03,
            gb_cpu.op_CB_04, gb_cpu.op_CB_05, gb_cpu.op_CB_06, gb_cpu.op_CB_07,
            gb_cpu.op_CB_08, gb_cpu.op_CB_09, gb_cpu.op_CB_0A, gb_cpu.op_CB_0B,
            gb_cpu.op_CB_0C, gb_cpu.op_CB_0D, gb_cpu.op_CB_0E, gb_cpu.op_CB_0F,
            gb_cpu.op_CB_10, gb_cpu.op_CB_11, gb_cpu.op_CB_12, gb_cpu.op_CB_13,
            gb_cpu.op_CB_14, gb_cpu.op_CB_15, gb_cpu.op_CB_16, gb_cpu.op_CB_17,
            gb_cpu.op_CB_18, gb_cpu.op_CB_19, gb_cpu.op_CB_1A, gb_cpu.op_CB_1B,
            gb_cpu.op_CB_1C, gb_cpu.op_CB_1D, gb_cpu.op_CB_1E, gb_cpu.op_CB_1F,
            gb_cpu.op_CB_20, gb_cpu.op_CB_21, gb_cpu.op_CB_22, gb_cpu.op_CB_23,
            gb_cpu.op_CB_24, gb_cpu.op_CB_25, gb_cpu.op_CB_26, gb_cpu.op_CB_27,
            gb_cpu.op_CB_28, gb_cpu.op_CB_29, gb_cpu.op_CB_2A, gb_cpu.op_CB_2B,
            gb_cpu.op_CB_2C, gb_cpu.op_CB_2D, gb_cpu.op_CB_2E, gb_cpu.op_CB_2F,
            gb_cpu.op_CB_30, gb_cpu.op_CB_31, gb_cpu.op_CB_32, gb_cpu.op_CB_33,
            gb_cpu.op_CB_34, gb_cpu.op_CB_35, gb_cpu.op_CB_36, gb_cpu.op_CB_37,
            gb_cpu.op_CB_38, gb_cpu.op_CB_39, gb_cpu.op_CB_3A, gb_cpu.op_CB_3B,
            gb_cpu.op_CB_3C, gb_cpu.op_CB_3D, gb_cpu.op_CB_3E, gb_cpu.op_CB_3F,
            gb_cpu.op_CB_40, gb_cpu.op_CB_41, gb_cpu.op_CB_42, gb_cpu.op_CB_43,
            gb_cpu.op_CB_44, gb_cpu.op_CB_45, gb_cpu.op_CB_46, gb_cpu.op_CB_47,
            gb_cpu.op_CB_48, gb_cpu.op_CB_49, gb_cpu.op_CB_4A, gb_cpu.op_CB_4B,
            gb_cpu.op_CB_4C, gb_cpu.op_CB_4D, gb_cpu.op_CB_4E, gb_cpu.op_CB_4F,
            gb_cpu.op_CB_50, gb_cpu.op_CB_51, gb_cpu.op_CB_52, gb_cpu.op_CB_53,
            gb_cpu.op_CB_54, gb_cpu.op_CB_55, gb_cpu.op_CB_56, gb_cpu.op_CB_57,
            gb_cpu.op_CB_58, gb_cpu.op_CB_59, gb_cpu.op_CB_5A, gb_cpu.op_CB_5B,
            gb_cpu.op_CB_5C, gb_cpu.op_CB_5D, gb_cpu.op_CB_5E, gb_cpu.op_CB_5F,
            gb_cpu.op_CB_60, gb_cpu.op_CB_61, gb_cpu.op_CB_62, gb_cpu.op_CB_63,
            gb_cpu.op_CB_64, gb_cpu.op_CB_65, gb_cpu.op_CB_66, gb_cpu.op_CB_67,
            gb_cpu.op_CB_68, gb_cpu.op_CB_69, gb_cpu.op_CB_6A, gb_cpu.op_CB_6B,
            gb_cpu.op_CB_6C, gb_cpu.op_CB_6D, gb_cpu.op_CB_6E, gb_cpu.op_CB_6F,
            gb_cpu.op_CB_70, gb_cpu.op_CB_71, gb_cpu.op_CB_72, gb_cpu.op_CB_73,
            gb_cpu.op_CB_74, gb_cpu.op_CB_75, gb_cpu.op_CB_76, gb_cpu.op_CB_77,
            gb_cpu.op_CB_78, gb_cpu.op_CB_79, gb_cpu.op_CB_7A, gb_cpu.op_CB_7B,
            gb_cpu.op_CB_7C, gb_cpu.op_CB_7D, gb_cpu.op_CB_7E, gb_cpu.op_CB_7F,
            gb_cpu.op_CB_80, gb_cpu.op_CB_81, gb_cpu.op_CB_82, gb_cpu.op_CB_83,
            gb_cpu.op_CB_84, gb_cpu.op_CB_85, gb_cpu.op_CB_86, gb_cpu.op_CB_87,
            gb_cpu.op_CB_88, gb_cpu.op_CB_89, gb_cpu.op_CB_8A, gb_cpu.op_CB_8B,
            gb_cpu.op_CB_8C, gb_cpu.op_CB_8D, gb_cpu.op_CB_8E, gb_cpu.op_CB_8F,
            gb_cpu.op_CB_90, gb_cpu.op_CB_91, gb_cpu.op_CB_92, gb_cpu.op_CB_93,
            gb_cpu.op_CB_94, gb_cpu.op_CB_95, gb_cpu.op_CB_96, gb_cpu.op_CB_97,
            gb_cpu.op_CB_98, gb_cpu.op_CB_99, gb_cpu.op_CB_9A, gb_cpu.op_CB_9B,
            gb_cpu.op_CB_9C, gb_cpu.op_CB_9D, gb_cpu.op_CB_9E, gb_cpu.op_CB_9F,
            gb_cpu.op_CB_A0, gb_cpu.op_CB_A1, gb_cpu.op_CB_A2, gb_cpu.op_CB_A3,
            gb_cpu.op_CB_A4, gb_cpu.op_CB_A5, gb_cpu.op_CB_A6, gb_cpu.op_CB_A7,
            gb_cpu.op_CB_A8, gb_cpu.op_CB_A9, gb_cpu.op_CB_AA, gb_cpu.op_CB_AB,
            gb_cpu.op_CB_AC, gb_cpu.op_CB_AD, gb_cpu.op_CB_AE, gb_cpu.op_CB_AF,
            gb_cpu.op_CB_B0, gb_cpu.op_CB_B1, gb_cpu.op_CB_B2, gb_cpu.op_CB_B3,
            gb_cpu.op_CB_B4, gb_cpu.op_CB_B5, gb_cpu.op_CB_B6, gb_cpu.op_CB_B7,
            gb_cpu.op_CB_B8, gb_cpu.op_CB_B9, gb_cpu.op_CB_BA, gb_cpu.op_CB_BB,
            gb_cpu.op_CB_BC, gb_cpu.op_CB_BD, gb_cpu.op_CB_BE, gb_cpu.op_CB_BF,
            gb_cpu.op_CB_C0, gb_cpu.op_CB_C1, gb_cpu.op_CB_C2, gb_cpu.op_CB_C3,
            gb_cpu.op_CB_C4, gb_cpu.op_CB_C5, gb_cpu.op_CB_C6, gb_cpu.op_CB_C7,
            gb_cpu.op_CB_C8, gb_cpu.op_CB_C9, gb_cpu.op_CB_CA, gb_cpu.op_CB_CB,
            gb_cpu.op_CB_CC, gb_cpu.op_CB_CD, gb_cpu.op_CB_CE, gb_cpu.op_CB_CF,
            gb_cpu.op_CB_D0, gb_cpu.op_CB_D1, gb_cpu.op_CB_D2, gb_cpu.op_CB_D3,
            gb_cpu.op_CB_D4, gb_cpu.op_CB_D5, gb_cpu.op_CB_D6, gb_cpu.op_CB_D7,
            gb_cpu.op_CB_D8, gb_cpu.op_CB_D9, gb_cpu.op_CB_DA, gb_cpu.op_CB_DB,
            gb_cpu.op_CB_DC, gb_cpu.op_CB_DD, gb_cpu.op_CB_DE, gb_cpu.op_CB_DF,
            gb_cpu.op_CB_E0, gb_cpu.op_CB_E1, gb_cpu.op_CB_E2, gb_cpu.op_CB_E3,
            gb_cpu.op_CB_E4, gb_cpu.op_CB_E5, gb_cpu.op_CB_E6, gb_cpu.op_CB_E7,
            gb_cpu.op_CB_E8, gb_cpu.op_CB_E9, gb_cpu.op_CB_EA, gb_cpu.op_CB_EB,
            gb_cpu.op_CB_EC, gb_cpu.op_CB_ED, gb_cpu.op_CB_EE, gb_cpu.op_CB_EF,
            gb_cpu.op_CB_F0, gb_cpu.op_CB_F1, gb_cpu.op_CB_F2, gb_cpu.op_CB_F3,
            gb_cpu.op_CB_F4, gb_cpu.op_CB_F5, gb_cpu.op_CB_F6, gb_cpu.op_CB_F7,
            gb_cpu.op_CB_F8, gb_cpu.op_CB_F9, gb_cpu.op_CB_FA, gb_cpu.op_CB_FB,
            gb_cpu.op_CB_FC, gb_cpu.op_CB_FD, gb_cpu.op_CB_FE, gb_cpu.op_CB_FF,
            ]

    def load_rom(self, fname):
        self.ram.load_rom(fname)

    def __str__(self):
        return """
Clock: %d
A: %02x   F: %02x   SP: %04x
B: %02x   C: %02x   PC: %04x
D: %02x   E: %02x   Halt: %s
H: %02x   L: %02x   Ints: %s
""" % (self.clock,
       self.A, self.F, self.SP,
       self.B, self.C, self.PC,
       self.D, self.E, str(self.halted),
       self.H, self.L, str(self.interrupts))

    def step(self):
        self.check_interrupts()
        if not self.halted:
            self.execute_next_instruction()
        else:
            self.dt = 4
            self.clock += 4
        self.update_clock()

    def check_interrupts(self):
        if not self.interrupts:
            return
        enabled = self.ram.read(0xFFFF)
        triggered = self.ram.read(0xFF0F)
        for i in range(5):
            if (enabled & (1 << i)) and (triggered & (1 << i)):
                # Clear this interrupt
                self.ram.write(0xFF0F, triggered & ~(1 << i))
                # Push PC
                self.SP = (self.SP - 2) & 0xFFFF
                self.ram.write(self.SP, self.PC & 0xFF)
                self.ram.write(self.SP+1, self.PC >> 8)
                # Disable interrupts
                self.interrupts = False
                # Unhalt
                self.halted = False
                # Jump to appropriate address
                self.PC = 0x40 + i * 0x8

                # Don't do more than one interrupt at once!
                break

    def execute_next_instruction(self):
        op = self.ram.read(self.PC)
        self.PC += 1

        #print "op %02x" % op

        op_details = self.opcodes[op]
        args = []
        for l in op_details[0]:
            a = 0
            for i in range(l):
                a += self.ram.read(self.PC) << (8*i)
                self.PC += 1
            args.append(a)
        op_details[1](self, *args)
        self.clock += op_details[2]
        self.dt = op_details[2]
        self.used_ops.add(op)

    def update_clock(self):
        # update divider register
        self.timer_div_countdown -= self.dt
        if self.timer_div_countdown <= 0:
            div = self.ram.read(0xFF04)
            self.ram.write(0xFF04, (div + 1) & 0xFF)
            self.timer_div_countdown += 256

        # Timer register
        control = self.ram.read(0xFF07)
        timer_on = (control & 0x4) >> 2
        timer_spd = (control & 3)
        if timer_spd == 0:
            timer_period = 1024
        elif timer_spd == 1:
            timer_period = 16
        elif timer_spd == 2:
            timer_period = 64
        else:
            timer_period = 256
        if timer_on:
            if self.timer_counter_countdown is None:
                self.timer_counter_countdown = timer_period
            self.timer_counter_countdown -= self.dt
            if self.timer_counter_countdown <= 0:
                self.timer_counter_countdown += timer_period
                counter = self.ram.read(0xFF05)
                if counter == 0xFF:
                    modulo = self.ram.read(0xFF06)
                    self.ram.write(0xFF05, modulo)
                    self.int_timer()
                else:
                    self.ram.write(0xFF05, counter + 1)

        if self.ram.mbc_type == 3:
            # MBC3 real time clock
            if (self.ram.mbc3_rtc_dh & 0x40) == 0:
                # Not halted
                self.ram.mbc3_rtc_countdown -= self.dt
                if self.ram.mbc3_rtc_countdown <= 0:
                    self.ram.mbc3_rtc_countdown += self.ram.mbc3_rtc_cycles_per_second
                    self.ram.mbc3_rtc_count += 1

    def op_00(self):
        # NOP
        pass

    def op_01(self, data):
        # LD BC, data
        self.B = data >> 8
        self.C = data & 0xFF

    def op_02(self):
        # LD (BC), A
        self.ram.write((self.B << 8) | self.C, self.A)

    def op_03(self):
        # INC BC
        self.C = (self.C + 1) & 0xFF
        if self.C == 0:
            self.B = (self.B + 1) & 0xFF

    def op_04(self):
        # INC B
        self.B = (self.B + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.B == 0:
            self.F |= Flags.Z
        if (self.B & 0xF) == 0:
            self.F |= Flags.H

    def op_05(self):
        # DEC B
        self.B = (self.B - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.B == 0:
            self.F |= Flags.Z
        if (self.B & 0xF) == 0xF:
            self.F |= Flags.H

    def op_06(self, data):
        # LD B, n
        self.B = data

    def op_07(self):
        # RLCA - rotate A left, both carry flag and bit 0 now contain old bit 7
        high_bit = (self.A & 0x80) / 0x80
        self.A = ((self.A << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C

    def op_08(self, addr):
        # LD (nn), SP
        self.ram.write(addr, self.SP & 0xFF)
        self.ram.write(addr+1, self.SP >> 8)

    def op_09(self):
        # ADD HL, BC
        HL = (self.H << 8) | self.L
        n = (self.B << 8) | self.C
        # Leave zero flag alone
        self.F &= Flags.Z
        self.F &= ~Flags.N
        if (HL & 0x0FFF) + (n & 0x0FFF) > 0x0FFF:
            self.F |= Flags.H
        if HL + n > 0xFFFF:
            self.F |= Flags.C
        HL = (HL + n) & 0xFFFF
        self.H = HL >> 8
        self.L = HL & 0xFF

    def op_0A(self):
        # LD A, (BC)
        self.A = self.ram.read((self.B << 8) | self.C)

    def op_0B(self):
        # DEC BC
        self.C = (self.C - 1) & 0xFF
        if self.C == 0xFF:
            self.B = (self.B - 1) & 0xFF

    def op_0C(self):
        # INC C
        self.C = (self.C + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.C == 0:
            self.F |= Flags.Z
        if (self.C & 0xF) == 0:
            self.F |= Flags.H

    def op_0D(self):
        # DEC C
        self.C = (self.C - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.C == 0:
            self.F |= Flags.Z
        if (self.C & 0xF) == 0xF:
            self.F |= Flags.H

    def op_0E(self, data):
        # LD C, n
        self.C = data

    def op_0F(self):
        # RRCA - rotate A right, bit 0 to bit 7 and carry flag
        low_bit = self.A & 0x1
        self.A = (self.A >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C

    def op_10(self, data):
        if data == 0:
            # STOP
            # For now implemented as HALT
            if self.interrupts:
                self.halted = True

    def op_11(self, data):
        # LD DE, nn
        self.D = data >> 8
        self.E = data & 0xFF

    def op_12(self):
        # LD (DE), A
        self.ram.write((self.D << 8) | self.E, self.A)

    def op_13(self):
        # INC DE
        self.E = (self.E + 1) & 0xFF
        if self.E == 0:
            self.D = (self.D + 1) & 0xFF

    def op_14(self):
        # INC D
        self.D = (self.D + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.D == 0:
            self.F |= Flags.Z
        if (self.D & 0xF) == 0:
            self.F |= Flags.H

    def op_15(self):
        # DEC D
        self.D = (self.D - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.D == 0:
            self.F |= Flags.Z
        if (self.D & 0xF) == 0xF:
            self.F |= Flags.H

    def op_16(self, data):
        # LD D, n
        self.D = data

    def op_17(self):
        # RLA - rotate A left through carry flag
        high_bit = (self.A & 0x80) / 0x80
        c_flag = (self.F & Flags.C) / Flags.C
        self.A = ((self.A << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C

    def op_18(self, offset):
        # JR n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        self.PC = self.PC + offset

    def op_19(self):
        # ADD HL, DE
        HL = (self.H << 8) | self.L
        n = (self.D << 8) | self.E
        # Leave zero flag alone
        self.F &= Flags.Z
        self.F &= ~Flags.N
        if (HL & 0x0FFF) + (n & 0x0FFF) > 0x0FFF:
            self.F |= Flags.H
        if HL + n > 0xFFFF:
            self.F |= Flags.C
        HL = (HL + n) & 0xFFFF
        self.H = HL >> 8
        self.L = HL & 0xFF

    def op_1A(self):
        # LD A, (DE)
        self.A = self.ram.read((self.D << 8) | self.E)

    def op_1B(self):
        # DEC DE
        self.E = (self.E - 1) & 0xFF
        if self.E == 0xFF:
            self.D = (self.D - 1) & 0xFF

    def op_1C(self):
        # INC E
        self.E = (self.E + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.E == 0:
            self.F |= Flags.Z
        if (self.E & 0xF) == 0:
            self.F |= Flags.H

    def op_1D(self):
        # DEC E
        self.E = (self.E - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.E == 0:
            self.F |= Flags.Z
        if (self.E & 0xF) == 0xF:
            self.F |= Flags.H

    def op_1E(self, data):
        # LD E, n
        self.E = data

    def op_1F(self):
        # RRA - rotate A right through carry flag
        low_bit = self.A & 0x1
        c_flag = (self.F & Flags.C) / Flags.C
        self.A = (self.A >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C

    def op_20(self, offset):
        # JRNZ n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        if (self.F & Flags.Z) == 0:
            self.PC = self.PC + offset

    def op_21(self, data):
        # LD HL, nn
        self.H = data >> 8
        self.L = data & 0xFF

    def op_22(self):
        # LDI (HL), A
        self.ram.write((self.H << 8) | self.L, self.A)
        if self.L < 0xFF:
            self.L += 1
        else:
            self.L = 0
            self.H = (self.H + 1) & 0xFF

    def op_23(self):
        # INC HL
        self.L = (self.L + 1) & 0xFF
        if self.L == 0:
            self.H = (self.H + 1) & 0xFF

    def op_24(self):
        # INC H
        self.H = (self.H + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.H == 0:
            self.F |= Flags.Z
        if (self.H & 0xF) == 0:
            self.F |= Flags.H

    def op_25(self):
        # DEC H
        self.H = (self.H - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.H == 0:
            self.F |= Flags.Z
        if (self.H & 0xF) == 0xF:
            self.F |= Flags.H

    def op_26(self, data):
        # LD H, n
        self.H = data

    def op_27(self):
        # DAA - adjust Binary Coded Decimal results
        c_flag = (self.F & Flags.C) / Flags.C
        h_flag = (self.F & Flags.H) / Flags.H
        n_flag = (self.F & Flags.N) / Flags.N
        # Leave N flag alone
        if not n_flag:
            # Last op was an addition
            if h_flag or (self.A & 0xF) > 9:
                self.A += 0x06
            if c_flag or self.A > 0x9F:
                self.A += 0x60
        else:
            if h_flag:
                self.A = (self.A - 6) & 0xFF
            if c_flag:
                self.A -= 0x60
        self.F &= ~(Flags.H | Flags.Z)
        if (self.A & 0x100) == 0x100:
            self.F |= Flags.C

        self.A &= 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_28(self, offset):
        # JRZ n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        if (self.F & Flags.Z) == Flags.Z:
            self.PC = self.PC + offset

    def op_29(self):
        # ADD HL, HL
        HL = (self.H << 8) | self.L
        n = (self.H << 8) | self.L
        # Leave zero flag alone
        self.F &= Flags.Z
        self.F &= ~Flags.N
        if (HL & 0x0FFF) + (n & 0x0FFF) > 0x0FFF:
            self.F |= Flags.H
        if HL + n > 0xFFFF:
            self.F |= Flags.C
        HL = (HL + n) & 0xFFFF
        self.H = HL >> 8
        self.L = HL & 0xFF

    def op_2A(self):
        # LDI A, (HL)
        self.A = self.ram.read((self.H << 8) | self.L)
        if self.L < 0xFF:
            self.L += 1
        else:
            self.L = 0x00
            self.H = (self.H + 1) & 0xFF

    def op_2B(self):
        # DEC HL
        self.L = (self.L - 1) & 0xFF
        if self.L == 0xFF:
            self.H = (self.H - 1) & 0xFF

    def op_2C(self):
        # INC L
        self.L = (self.L + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.L == 0:
            self.F |= Flags.Z
        if (self.L & 0xF) == 0:
            self.F |= Flags.H

    def op_2D(self):
        # DEC L
        self.L = (self.L - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.L == 0:
            self.F |= Flags.Z
        if (self.L & 0xF) == 0xF:
            self.F |= Flags.H

    def op_2E(self, data):
        # LD L, n
        self.L = data

    def op_2F(self):
        # CPL - Flip all bits of A
        self.F &= Flags.Z | Flags.C
        self.F |= Flags.N | Flags.H
        self.A = self.A ^ 0xFF

    def op_30(self, offset):
        # JRNC n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        if (self.F & Flags.C) == 0:
            self.PC = self.PC + offset

    def op_31(self, data):
        # LD SP, nn
        self.SP = data

    def op_32(self):
        # LDD (HL), A
        self.ram.write((self.H << 8) | self.L, self.A)
        if self.L > 0:
            self.L -= 1
        else:
            self.L = 0xFF
            self.H = (self.H - 1) & 0xFF

    def op_33(self):
        # INC SP
        self.SP = (self.SP + 1) & 0xFFFF

    def op_34(self):
        # INC (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data = (data + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if data == 0:
            self.F |= Flags.Z
        if (data & 0xF) == 0:
            self.F |= Flags.H
        self.ram.write((self.H << 8) | self.L, data)

    def op_35(self):
        # DEC (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data = (data - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if data == 0:
            self.F |= Flags.Z
        if (data & 0xF) == 0xF:
            self.F |= Flags.H
        self.ram.write((self.H << 8) | self.L, data)

    def op_36(self, data):
        # LD (HL), n
        self.ram.write((self.H << 8) | self.L, data)

    def op_37(self):
        # SCF - Set carry flag
        self.F &= ~(Flags.N | Flags.H)
        self.F |= Flags.C

    def op_38(self, offset):
        # JRC n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        if (self.F & Flags.C) == Flags.C:
            self.PC = self.PC + offset

    def op_39(self):
        # ADD HL, SP
        HL = (self.H << 8) | self.L
        n = self.SP
        # Leave zero flag alone
        self.F &= Flags.Z
        self.F &= ~Flags.N
        if (HL & 0x0FFF) + (n & 0x0FFF) > 0x0FFF:
            self.F |= Flags.H
        if HL + n > 0xFFFF:
            self.F |= Flags.C
        HL = (HL + n) & 0xFFFF
        self.H = HL >> 8
        self.L = HL & 0xFF

    def op_3A(self):
        # LDD A, (HL)
        self.A = self.ram.read((self.H << 8) | self.L)
        if self.L > 0:
            self.L -= 1
        else:
            self.L = 0xFF
            self.H = (self.H - 1) & 0xFF

    def op_3B(self):
        # DEC SP
        self.SP = (self.SP - 1) & 0xFFFF

    def op_3C(self):
        # INC A
        self.A = (self.A + 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        if self.A == 0:
            self.F |= Flags.Z
        if (self.A & 0xF) == 0:
            self.F |= Flags.H

    def op_3D(self):
        # DEC A
        self.A = (self.A - 1) & 0xFF
        # Leave carry flag alone
        self.F &= Flags.C
        self.F |= Flags.N
        if self.A == 0:
            self.F |= Flags.Z
        if (self.A & 0xF) == 0xF:
            self.F |= Flags.H

    def op_3E(self, data):
        # LD A, n
        self.A = data

    def op_3F(self):
        # CCF - Complement carry flag
        self.F &= ~(Flags.N | Flags.H)
        self.F ^= Flags.C

    def op_40(self):
        # LD B, B
        # self.B = self.B
        pass

    def op_41(self):
        # LD B, C
        self.B = self.C

    def op_42(self):
        # LD B, D
        self.B = self.D

    def op_43(self):
        # LD B, E
        self.B = self.E

    def op_44(self):
        # LD B, H
        self.B = self.H

    def op_45(self):
        # LD B, L
        self.B = self.L

    def op_46(self):
        # LD B, (HL)
        self.B = self.ram.read((self.H << 8) | self.L)

    def op_47(self):
        # LD B, A
        self.B = self.A

    def op_48(self):
        # LD C, B
        self.C = self.B

    def op_49(self):
        # LD C, C
        # self.C = self.C
        pass

    def op_4A(self):
        # LD C, D
        self.C = self.D

    def op_4B(self):
        # LD C, E
        self.C = self.E

    def op_4C(self):
        # LD C, H
        self.C = self.H

    def op_4D(self):
        # LD C, L
        self.C = self.L

    def op_4E(self):
        # LD C, (HL)
        self.C = self.ram.read((self.H << 8) | self.L)

    def op_4F(self):
        # LD C, A
        self.C = self.A

    def op_50(self):
        # LD D, B
        self.D = self.B

    def op_51(self):
        # LD D, C
        self.D = self.C

    def op_52(self):
        # LD D, D
        # self.D = self.D
        pass

    def op_53(self):
        # LD D, E
        self.D = self.E

    def op_54(self):
        # LD D, H
        self.D = self.H

    def op_55(self):
        # LD D, L
        self.D = self.L

    def op_56(self):
        # LD D, (HL)
        self.D = self.ram.read((self.H << 8) | self.L)

    def op_57(self):
        # LD D, A
        self.D = self.A

    def op_58(self):
        # LD E, B
        self.E = self.B

    def op_59(self):
        # LD E, C
        self.E = self.C

    def op_5A(self):
        # LD E, D
        self.E = self.D

    def op_5B(self):
        # LD E, E
        # self.E = self.E
        pass

    def op_5C(self):
        # LD E, H
        self.E = self.H

    def op_5D(self):
        # LD E, L
        self.E = self.L

    def op_5E(self):
        # LD E, (HL)
        self.E = self.ram.read((self.H << 8) | self.L)

    def op_5F(self):
        # LD E, A
        self.E = self.A

    def op_60(self):
        # LD H, B
        self.H = self.B

    def op_61(self):
        # LD H, C
        self.H = self.C

    def op_62(self):
        # LD H, D
        self.H = self.D

    def op_63(self):
        # LD H, E
        self.H = self.E

    def op_64(self):
        # LD H, H
        # self.H = self.H
        pass

    def op_65(self):
        # LD H, L
        self.H = self.L

    def op_66(self):
        # LD H, (HL)
        self.H = self.ram.read((self.H << 8) | self.L)

    def op_67(self):
        # LD H, A
        self.H = self.A

    def op_68(self):
        # LD L, B
        self.L = self.B

    def op_69(self):
        # LD L, C
        self.L = self.C

    def op_6A(self):
        # LD L, D
        self.L = self.D

    def op_6B(self):
        # LD L, E
        self.L = self.E

    def op_6C(self):
        # LD L, H
        self.L = self.H

    def op_6D(self):
        # LD L, L
        # self.L = self.L
        pass

    def op_6E(self):
        # LD L, (HL)
        self.L = self.ram.read((self.H << 8) | self.L)

    def op_6F(self):
        # LD L, A
        self.L = self.A

    def op_70(self):
        # LD (HL), B
        self.ram.write((self.H << 8) | self.L, self.B)

    def op_71(self):
        # LD (HL), C
        self.ram.write((self.H << 8) | self.L, self.C)

    def op_72(self):
        # LD (HL), D
        self.ram.write((self.H << 8) | self.L, self.D)

    def op_73(self):
        # LD (HL), E
        self.ram.write((self.H << 8) | self.L, self.E)

    def op_74(self):
        # LD (HL), H
        self.ram.write((self.H << 8) | self.L, self.H)

    def op_75(self):
        # LD (HL), L
        self.ram.write((self.H << 8) | self.L, self.L)

    def op_76(self):
        # HALT
        if self.interrupts:
            self.halted = True

    def op_77(self):
        # LD (HL), A
        self.ram.write((self.H << 8) | self.L, self.A)

    def op_78(self):
        # LD A, B
        self.A = self.B

    def op_79(self):
        # LD A, C
        self.A = self.C

    def op_7A(self):
        # LD A, D
        self.A = self.D

    def op_7B(self):
        # LD A, E
        self.A = self.E

    def op_7C(self):
        # LD A, H
        self.A = self.H

    def op_7D(self):
        # LD A, L
        self.A = self.L

    def op_7E(self):
        # LD A, (HL)
        self.A = self.ram.read((self.H << 8) | self.L)

    def op_7F(self):
        # LD A, A
        # self.A = self.A
        pass

    def op_80(self):
        # ADD A, B
        self.F = 0
        if (self.A & 0xF) + (self.B & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.B > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.B) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_81(self):
        # ADD A, C
        self.F = 0
        if (self.A & 0xF) + (self.C & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.C > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.C) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_82(self):
        # ADD A, D
        self.F = 0
        if (self.A & 0xF) + (self.D & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.D > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.D) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_83(self):
        # ADD A, E
        self.F = 0
        if (self.A & 0xF) + (self.E & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.E > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.E) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_84(self):
        # ADD A, H
        self.F = 0
        if (self.A & 0xF) + (self.H & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.H > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.H) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_85(self):
        # ADD A, L
        self.F = 0
        if (self.A & 0xF) + (self.L & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.L > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.L) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_86(self):
        # ADD A, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        self.F = 0
        if (self.A & 0xF) + (data & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + data > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + data) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_87(self):
        # ADD A, A
        self.F = 0
        if (self.A & 0xF) + (self.A & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + self.A > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.A) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_88(self):
        # ADC A, B
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.B & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.B + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.B + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_89(self):
        # ADC A, C
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.C & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.C + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.C + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8A(self):
        # ADC A, D
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.D & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.D + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.D + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8B(self):
        # ADC A, E
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.E & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.E + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.E + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8C(self):
        # ADC A, H
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.H & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.H + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.H + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8D(self):
        # ADC A, L
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.L & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.L + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.L + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8E(self):
        # ADC A, (HL)
        c_flag = (self.F & Flags.C) / Flags.C
        data = self.ram.read((self.H << 8) | self.L)
        self.F = 0
        if (self.A & 0xF) + (data & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + data + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + data + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_8F(self):
        # ADC A, A
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (self.A & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + self.A + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + self.A + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_90(self):
        # SUB A, B
        self.F = Flags.N
        if (self.A & 0xF) < (self.B & 0xF):
            self.F |= Flags.H
        if self.A < self.B:
            self.F |= Flags.C
        self.A = (self.A - self.B) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_91(self):
        # SUB A, C
        self.F = Flags.N
        if (self.A & 0xF) < (self.C & 0xF):
            self.F |= Flags.H
        if self.A < self.C:
            self.F |= Flags.C
        self.A = (self.A - self.C) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_92(self):
        # SUB A, D
        self.F = Flags.N
        if (self.A & 0xF) < (self.D & 0xF):
            self.F |= Flags.H
        if self.A < self.D:
            self.F |= Flags.C
        self.A = (self.A - self.D) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_93(self):
        # SUB A, E
        self.F = Flags.N
        if (self.A & 0xF) < (self.E & 0xF):
            self.F |= Flags.H
        if self.A < self.E:
            self.F |= Flags.C
        self.A = (self.A - self.E) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_94(self):
        # SUB A, H
        self.F = Flags.N
        if (self.A & 0xF) < (self.H & 0xF):
            self.F |= Flags.H
        if self.A < self.H:
            self.F |= Flags.C
        self.A = (self.A - self.H) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_95(self):
        # SUB A, L
        self.F = Flags.N
        if (self.A & 0xF) < (self.L & 0xF):
            self.F |= Flags.H
        if self.A < self.L:
            self.F |= Flags.C
        self.A = (self.A - self.L) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_96(self):
        # SUB A, (HL)
        self.F = Flags.N
        data = self.ram.read((self.H << 8) | self.L)
        if (self.A & 0xF) < (data & 0xF):
            self.F |= Flags.H
        if self.A < data:
            self.F |= Flags.C
        self.A = (self.A - data) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_97(self):
        # SUB A, A
        self.F = Flags.N
        if (self.A & 0xF) < (self.A & 0xF):
            self.F |= Flags.H
        if self.A < self.A:
            self.F |= Flags.C
        self.A = (self.A - self.A) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_98(self):
        # SBC A, B
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.B & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.B + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.B - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_99(self):
        # SBC A, C
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.C & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.C + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.C - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9A(self):
        # SBC A, D
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.D & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.D + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.D - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9B(self):
        # SBC A, E
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.E & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.E + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.E - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9C(self):
        # SBC A, H
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.H & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.H + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.H - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9D(self):
        # SBC A, L
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.L & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.L + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.L - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9E(self):
        # SBC A, (HL)
        c_flag = (self.F & Flags.C) / Flags.C
        data = self.ram.read((self.H << 8) | self.L)
        self.F = Flags.N
        if (self.A & 0xF) < (data & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < data + c_flag:
            self.F |= Flags.C
        self.A = (self.A - data - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9F(self):
        # SBC A, A
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (self.A & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < self.A + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.A - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_A0(self):
        # AND A, B
        self.F = Flags.H
        self.A = self.A & self.B
        if self.A == 0:
            self.F |= Flags.Z

    def op_A1(self):
        # AND A, C
        self.F = Flags.H
        self.A = self.A & self.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_A2(self):
        # AND A, D
        self.F = Flags.H
        self.A = self.A & self.D
        if self.A == 0:
            self.F |= Flags.Z

    def op_A3(self):
        # AND A, E
        self.F = Flags.H
        self.A = self.A & self.E
        if self.A == 0:
            self.F |= Flags.Z

    def op_A4(self):
        # AND A, H
        self.F = Flags.H
        self.A = self.A & self.H
        if self.A == 0:
            self.F |= Flags.Z

    def op_A5(self):
        # AND A, L
        self.F = Flags.H
        self.A = self.A & self.L
        if self.A == 0:
            self.F |= Flags.Z

    def op_A6(self):
        # AND A, (HL)
        self.F = Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        self.A = self.A & data
        if self.A == 0:
            self.F |= Flags.Z

    def op_A7(self):
        # AND A, A
        self.F = Flags.H
        self.A = self.A & self.A
        if self.A == 0:
            self.F |= Flags.Z

    def op_A8(self):
        # XOR A, B
        self.F = 0
        self.A = self.A ^ self.B
        if self.A == 0:
            self.F |= Flags.Z

    def op_A9(self):
        # XOR A, C
        self.F = 0
        self.A = self.A ^ self.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_AA(self):
        # XOR A, D
        self.F = 0
        self.A = self.A ^ self.D
        if self.A == 0:
            self.F |= Flags.Z

    def op_AB(self):
        # XOR A, E
        self.F = 0
        self.A = self.A ^ self.E
        if self.A == 0:
            self.F |= Flags.Z

    def op_AC(self):
        # XOR A, H
        self.F = 0
        self.A = self.A ^ self.H
        if self.A == 0:
            self.F |= Flags.Z

    def op_AD(self):
        # XOR A, L
        self.F = 0
        self.A = self.A ^ self.L
        if self.A == 0:
            self.F |= Flags.Z

    def op_AE(self):
        # XOR A, (HL)
        self.F = 0
        data = self.ram.read((self.H << 8) | self.L)
        self.A = self.A ^ data
        if self.A == 0:
            self.F |= Flags.Z

    def op_AF(self):
        # XOR A, A
        self.F = 0
        self.A = self.A ^ self.A
        if self.A == 0:
            self.F |= Flags.Z

    def op_B0(self):
        # OR A, B
        self.F = 0
        self.A = self.A | self.B
        if self.A == 0:
            self.F |= Flags.Z

    def op_B1(self):
        # OR A, C
        self.F = 0
        self.A = self.A | self.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_B2(self):
        # OR A, D
        self.F = 0
        self.A = self.A | self.D
        if self.A == 0:
            self.F |= Flags.Z

    def op_B3(self):
        # OR A, E
        self.F = 0
        self.A = self.A | self.E
        if self.A == 0:
            self.F |= Flags.Z

    def op_B4(self):
        # OR A, H
        self.F = 0
        self.A = self.A | self.H
        if self.A == 0:
            self.F |= Flags.Z

    def op_B5(self):
        # OR A, L
        self.F = 0
        self.A = self.A | self.L
        if self.A == 0:
            self.F |= Flags.Z

    def op_B6(self):
        # OR A, (HL)
        self.F = 0
        data = self.ram.read((self.H << 8) | self.L)
        self.A = self.A | data
        if self.A == 0:
            self.F |= Flags.Z

    def op_B7(self):
        # OR A, A
        self.F = 0
        self.A = self.A | self.A
        if self.A == 0:
            self.F |= Flags.Z

    def op_B8(self):
        # CP A, B
        self.F = Flags.N
        if self.A == self.B:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.B & 0xF):
            self.F |= Flags.H
        if self.A < self.B:
            self.F |= Flags.C

    def op_B9(self):
        # CP A, C
        self.F = Flags.N
        if self.A == self.C:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.C & 0xF):
            self.F |= Flags.H
        if self.A < self.C:
            self.F |= Flags.C
    
    def op_BA(self):
        # CP A, D
        self.F = Flags.N
        if self.A == self.D:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.D & 0xF):
            self.F |= Flags.H
        if self.A < self.D:
            self.F |= Flags.C
    
    def op_BB(self):
        # CP A, E
        self.F = Flags.N
        if self.A == self.E:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.E & 0xF):
            self.F |= Flags.H
        if self.A < self.E:
            self.F |= Flags.C
    
    def op_BC(self):
        # CP A, H
        self.F = Flags.N
        if self.A == self.H:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.H & 0xF):
            self.F |= Flags.H
        if self.A < self.H:
            self.F |= Flags.C
    
    def op_BD(self):
        # CP A, L
        self.F = Flags.N
        if self.A == self.L:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.L & 0xF):
            self.F |= Flags.H
        if self.A < self.L:
            self.F |= Flags.C
    
    def op_BE(self):
        # CP A, (HL)
        self.F = Flags.N
        data = self.ram.read((self.H << 8) | self.L)
        if self.A == data:
            self.F |= Flags.Z
        if (self.A & 0xF) < (data & 0xF):
            self.F |= Flags.H
        if self.A < data:
            self.F |= Flags.C
    
    def op_BF(self):
        # CP A, A
        self.F = Flags.N
        if self.A == self.A:
            self.F |= Flags.Z
        if (self.A & 0xF) < (self.A & 0xF):
            self.F |= Flags.H
        if self.A < self.A:
            self.F |= Flags.C

    def op_C0(self):
        # RETNZ
        if (self.F & Flags.Z) == 0:
            lo = self.ram.read(self.SP)
            hi = self.ram.read(self.SP + 1)
            self.SP = (self.SP + 2) & 0xFFFF
            self.PC = (hi << 8) | lo

    def op_C1(self):
        # POP BC
        self.B = self.ram.read(self.SP + 1)
        self.C = self.ram.read(self.SP)
        self.SP = (self.SP + 2) & 0xFFFF

    def op_C2(self, addr):
        # JNZ nn
        if (self.F & Flags.Z) == 0:
            self.PC = addr

    def op_C3(self, addr):
        # JP nn
        self.PC = addr

    def op_C4(self, addr):
        # CALLNZ nn
        if (self.F & Flags.Z) == 0:
            # Push current address onto stack
            self.SP = (self.SP - 2) & 0xFFFF
            self.ram.write(self.SP, self.PC & 0xFF)
            self.ram.write(self.SP + 1, self.PC >> 8)
            # Jump to argument
            self.PC = addr

    def op_C5(self):
        # PUSH BC
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.C)
        self.ram.write(self.SP+1, self.B)

    def op_C6(self, data):
        # ADD A, #
        self.F = 0
        if (self.A & 0xF) + (data & 0xF) > 0xF:
            self.F |= Flags.H
        if self.A + data > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + data) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_C7(self):
        # RST 0x00
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x00

    def op_C8(self):
        # RETZ
        if (self.F & Flags.Z) == Flags.Z:
            lo = self.ram.read(self.SP)
            hi = self.ram.read(self.SP + 1)
            self.SP = (self.SP + 2) & 0xFFFF
            self.PC = (hi << 8) | lo

    def op_C9(self):
        # RET
        lo = self.ram.read(self.SP)
        hi = self.ram.read(self.SP + 1)
        self.SP = (self.SP + 2) & 0xFFFF
        self.PC = (hi << 8) | lo

    def op_CA(self, addr):
        # JZ nn
        if (self.F & Flags.Z) == Flags.Z:
            self.PC = addr

    def op_CB(self, sub_op):
        # Extra ops dispatcher
        sub_op_fn = self.extra_ops_table[sub_op]
        sub_op_fn(self)

    def op_CC(self, addr):
        # CALLZ nn
        if (self.F & Flags.Z) == Flags.Z:
            # Push current address onto stack
            self.SP = (self.SP - 2) & 0xFFFF
            self.ram.write(self.SP, self.PC & 0xFF)
            self.ram.write(self.SP + 1, self.PC >> 8)
            # Jump to argument
            self.PC = addr

    def op_CD(self, addr):
        # CALL nn
        # Push current address onto stack
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP + 1, self.PC >> 8)
        # Jump to argument
        self.PC = addr

    def op_CE(self, data):
        # ADC A, #
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = 0
        if (self.A & 0xF) + (data & 0xF) + c_flag > 0xF:
            self.F |= Flags.H
        if self.A + data + c_flag > 0xFF:
            self.F |= Flags.C
        self.A = (self.A + data + c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_CF(self):
        # RST 0x08
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x08

    def op_D0(self):
        # RETNC
        if (self.F & Flags.C) == 0:
            lo = self.ram.read(self.SP)
            hi = self.ram.read(self.SP + 1)
            self.SP = (self.SP + 2) & 0xFFFF
            self.PC = (hi << 8) | lo

    def op_D1(self):
        # POP DE
        self.D = self.ram.read(self.SP + 1)
        self.E = self.ram.read(self.SP)
        self.SP = (self.SP + 2) & 0xFFFF

    def op_D2(self, addr):
        # JNC nn
        if (self.F & Flags.C) == 0:
            self.PC = addr

    def op_D3(self, *args):
        # Does not exist
        assert False, "Op D3 does not exist"
        pass

    def op_D4(self, addr):
        # CALLNC nn
        if (self.F & Flags.C) == 0:
            # Push current address onto stack
            self.SP = (self.SP - 2) & 0xFFFF
            self.ram.write(self.SP, self.PC & 0xFF)
            self.ram.write(self.SP + 1, self.PC >> 8)
            # Jump to argument
            self.PC = addr

    def op_D5(self):
        # PUSH DE
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.E)
        self.ram.write(self.SP + 1, self.D)

    def op_D6(self, data):
        # SUB A, #
        self.F = Flags.N
        if (self.A & 7) < (data & 7):
            self.F |= Flags.H
        if self.A < data:
            self.F |= Flags.C
        self.A = (self.A - data) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_D7(self):
        # RST 0x10
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x10

    def op_D8(self):
        # RETC
        if (self.F & Flags.C) == Flags.C:
            lo = self.ram.read(self.SP)
            hi = self.ram.read(self.SP + 1)
            self.SP = (self.SP + 2) & 0xFFFF
            self.PC = (hi << 8) | lo

    def op_D9(self):
        # RETI
        lo = self.ram.read(self.SP)
        hi = self.ram.read(self.SP + 1)
        self.SP = (self.SP + 2) & 0xFFFF
        self.PC = (hi << 8) | lo
        self.interrupts = True

    def op_DA(self, addr):
        # JC nn
        if (self.F & Flags.C) == Flags.C:
            self.PC = addr

    def op_DB(self, *args):
        # Does not exist
        assert False, "Op DB does not exist"
        pass

    def op_DC(self, addr):
        # CALLC nn
        if (self.F & Flags.C) == Flags.C:
            # Push current address onto stack
            self.SP = (self.SP - 2) & 0xFFFF
            self.ram.write(self.SP, self.PC & 0xFF)
            self.ram.write(self.SP + 1, self.PC >> 8)
            # Jump to argument
            self.PC = addr

    def op_DD(self, *args):
        # Does not exist
        assert False, "Op DD does not exist"
        pass

    def op_DE(self, data):
        # SBC A, n
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) < (data & 0xF) + c_flag:
            self.F |= Flags.H
        if self.A < data + c_flag:
            self.F |= Flags.C
        self.A = (self.A - data - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_DF(self):
        # RST 0x18
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x18

    def op_E0(self, offset):
        # LDH (n), A
        self.ram.write(0xFF00 + offset, self.A)

    def op_E1(self):
        # POP HL
        self.H = self.ram.read(self.SP + 1)
        self.L = self.ram.read(self.SP)
        self.SP = (self.SP + 2) & 0xFFFF

    def op_E2(self):
        # LDH (C), A
        self.ram.write(0xFF00 + self.C, self.A)

    def op_E3(self, *args):
        # Does not exist
        assert False, "Op E3 does not exist"
        pass

    def op_E4(self, *args):
        # Does not exist
        assert False, "Op E4 does ont exist"
        pass

    def op_E5(self):
        # PUSH HL
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.L)
        self.ram.write(self.SP+1, self.H)

    def op_E6(self, data):
        # AND A, #
        self.F = Flags.H
        self.A = self.A & data
        if self.A == 0:
            self.F |= Flags.Z

    def op_E7(self):
        # RST 0x20
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x20

    def op_E8(self, data):
        # ADD SP, #
        self.F = 0
        if (self.SP & 0xF) + (data & 0xF) > 0xF:
            self.F |= Flags.H
        if (self.SP & 0xFF) + (data & 0xFF) > 0xFF:
            self.F |= Flags.C

        # Fix sign
        if data > 0x7F:
            data = data - 0x100

        self.SP = (self.SP + data) & 0xFFFF

    def op_E9(self):
        # JP HL
        addr = (self.H << 8) | self.L
        self.PC = addr

    def op_EA(self, addr):
        # LD (nn), A
        self.ram.write(addr, self.A)

    def op_EB(self, *args):
        # Does not exist
        assert False, "Op EB does not exist"
        pass

    def op_EC(self, *args):
        # Does not exist
        assert False, "Op EC does not exist"
        pass

    def op_ED(self, *args):
        # Does not exist
        assert False, "Op ED does not exist"
        pass

    def op_EE(self, data):
        # XOR A, #
        self.F = 0
        self.A = self.A ^ data
        if self.A == 0:
            self.F |= Flags.Z

    def op_EF(self):
        # RST 0x28
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x28

    def op_F0(self, offset):
        # LDH A, (n)
        self.A = self.ram.read(0xFF00 + offset)

    def op_F1(self):
        # POP AF
        self.A = self.ram.read(self.SP + 1)
        # Flags register only holds four bits
        self.F = self.ram.read(self.SP) & 0xF0
        self.SP = (self.SP + 2) & 0xFFFF

    def op_F2(self):
        # LDH A, (C)
        self.A = self.ram.read(0xFF00 + self.C)

    def op_F3(self):
        # DI - disable interrupts
        # TODO - should wait one instruction
        self.interrupts = False

    def op_F4(self, *args):
        # Does not exist
        assert False, "Op F4 does not exist"
        pass

    def op_F5(self):
        # PUSH AF
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.F)
        self.ram.write(self.SP + 1, self.A)

    def op_F6(self, data):
        # OR A, #
        self.F = 0
        self.A = self.A | data
        if self.A == 0:
            self.F |= Flags.Z

    def op_F7(self):
        # RST 0x30
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x30

    def op_F8(self, offset):
        # LDHL SP, d (put the effective address SP + d into HL)
        # Fix sign of argument
        if offset > 0x7F:
            offset = offset - 0x100

        addr = self.SP + offset
        self.H = addr >> 8
        self.L = addr & 0xFF
        self.F = 0
        # TODO - These might be not computed correctly
        if (self.SP & 0xF) + (offset & 0xF) > 0xF:
            self.F |= Flags.H
        if (self.SP & 0xFF) + (offset & 0xFF) > 0xFF:
            self.F |= Flags.C

    def op_F9(self):
        # LD SP, HL
        self.SP = (self.H << 8) | self.L

    def op_FA(self, addr):
        # LD A, (nn)
        self.A = self.ram.read(addr)

    def op_FB(self):
        # EI - enable interrupts
        # TODO - should wait for one instruction
        self.interrupts = True

    def op_FC(self, *args):
        # Does not exist
        assert False, "Op FC does not exist"
        pass

    def op_FD(self, *args):
        assert False, "Op FD does not exist"
        pass

    def op_FE(self, data):
        # CP A, #
        self.F = Flags.N
        if self.A == data:
            self.F |= Flags.Z
        if (self.A & 0xF) < (data & 0xF):
            self.F |= Flags.H
        if self.A < data:
            self.F |= Flags.C

    def op_FF(self):
        # RST 0x38
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x38
    
    # Extended ops
    def op_CB_00(self):
        # RLC B
        high_bit = (self.B & 0x80) >> 7
        self.B = ((self.B << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_01(self):
        # RLC C
        high_bit = (self.C & 0x80) >> 7
        self.C = ((self.C << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_02(self):
        # RLC D
        high_bit = (self.D & 0x80) >> 7
        self.D = ((self.D << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_03(self):
        # RLC E
        high_bit = (self.E & 0x80) >> 7
        self.E = ((self.E << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_04(self):
        # RLC H
        high_bit = (self.H & 0x80) >> 7
        self.H = ((self.H << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_05(self):
        # RLC L
        high_bit = (self.L & 0x80) >> 7
        self.L = ((self.L << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_06(self):
        # RLC (HL)
        data = self.ram.read((self.H << 8) | self.L)
        high_bit = (data & 0x80) >> 7
        data = ((data << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_07(self):
        # RLC A
        high_bit = (self.A & 0x80) >> 7
        self.A = ((self.A << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_08(self):
        # RRC B
        low_bit = (self.B & 1)
        self.B = (self.B >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_09(self):
        # RRC C
        low_bit = (self.C & 1)
        self.C = (self.C >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_0A(self):
        # RRC D
        low_bit = (self.D & 1)
        self.D = (self.D >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_0B(self):
        # RRC E
        low_bit = (self.E & 1)
        self.E = (self.E >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_0C(self):
        # RRC H
        low_bit = (self.H & 1)
        self.H = (self.H >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_0D(self):
        # RRC L
        low_bit = (self.L & 1)
        self.L = (self.L >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_0E(self):
        # RRC (HL)
        data = self.ram.read((self.H << 8) | self.L)
        low_bit = (data & 1)
        data = (data >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_0F(self):
        # RRC A
        low_bit = (self.A & 1)
        self.A = (self.A >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_10(self):
        # RL B
        high_bit = (self.B & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.B = ((self.B << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_11(self):
        # RL C
        high_bit = (self.C & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.C = ((self.C << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_12(self):
        # RL D
        high_bit = (self.D & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.D = ((self.D << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_13(self):
        # RL E
        high_bit = (self.E & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.E = ((self.E << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_14(self):
        # RL H
        high_bit = (self.H & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.H = ((self.H << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_15(self):
        # RL L
        high_bit = (self.L & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.L = ((self.L << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_16(self):
        # RL (HL)
        data = self.ram.read((self.H << 8) | self.L)
        high_bit = (data & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        data = ((data << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_17(self):
        # RL A
        high_bit = (self.A & 0x80) >> 7
        c_flag = (self.F & Flags.C) / Flags.C
        self.A = ((self.A << 1) & 0xFF) | c_flag
        self.F = high_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_18(self):
        # RR B
        low_bit = self.B & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.B = (self.B >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_19(self):
        # RR C
        low_bit = self.C & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.C = (self.C >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_1A(self):
        # RR D
        low_bit = self.D & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.D = (self.D >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_1B(self):
        # RR E
        low_bit = self.E & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.E = (self.E >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_1C(self):
        # RR H
        low_bit = self.H & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.H = (self.H >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_1D(self):
        # RR L
        low_bit = self.L & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.L = (self.L >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z

    def op_CB_1E(self):
        # RR (HL)
        data = self.ram.read((self.H << 8) | self.L)
        low_bit = data & 1
        c_flag = (self.F & Flags.C) / Flags.C
        data = (data >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_1F(self):
        # RR A
        low_bit = self.A & 1
        c_flag = (self.F & Flags.C) / Flags.C
        self.A = (self.A >> 1) | (c_flag << 7)
        self.F = low_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_20(self):
        # SLA B
        high_bit = (self.B & 0x80) >> 7
        self.B = (self.B << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_21(self):
        # SLA C
        high_bit = (self.C & 0x80) >> 7
        self.C = (self.C << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_22(self):
        # SLA D
        high_bit = (self.D & 0x80) >> 7
        self.D = (self.D << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_23(self):
        # SLA E
        high_bit = (self.E & 0x80) >> 7
        self.E = (self.E << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_24(self):
        # SLA H
        high_bit = (self.H & 0x80) >> 7
        self.H = (self.H << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_25(self):
        # SLA L
        high_bit = (self.L & 0x80) >> 7
        self.L = (self.L << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z

    def op_CB_26(self):
        # SLA (HL)
        data = self.ram.read((self.H << 8) | self.L)
        high_bit = (data & 0x80) >> 7
        data = (data << 1) & 0xFF
        self.F = high_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_27(self):
        # SLA A
        high_bit = (self.A & 0x80) >> 7
        self.A = (self.A << 1) & 0xFF
        self.F = high_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_CB_28(self):
        # SRA B
        low_bit = self.B & 1
        self.B = (self.B & 0x80) | (self.B >> 1)
        self.F = low_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z

    def op_CB_29(self):
        # SRA C
        low_bit = self.C & 1
        self.C = (self.C & 0x80) | (self.C >> 1)
        self.F = low_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z

    def op_CB_2A(self):
        # SRA D
        low_bit = self.D & 1
        self.D = (self.D & 0x80) | (self.D >> 1)
        self.F = low_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z

    def op_CB_2B(self):
        # SRA E
        low_bit = self.E & 1
        self.E = (self.E & 0x80) | (self.E >> 1)
        self.F = low_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_2C(self):
        # SRA H
        low_bit = self.H & 1
        self.H = (self.H & 0x80) | (self.H >> 1)
        self.F = low_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_2D(self):
        # SRA L
        low_bit = self.L & 1
        self.L = (self.L & 0x80) | (self.L >> 1)
        self.F = low_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_2E(self):
        # SRA (HL)
        data = self.ram.read((self.H << 8) | self.L)
        low_bit = data & 1
        self.L = (data & 0x80) | (data >> 1)
        self.F = low_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_2F(self):
        # SRA A
        low_bit = self.A & 1
        self.A = (self.A & 0x80) | (self.A >> 1)
        self.F = low_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_CB_30(self):
        # SWAP B
        self.F = 0
        self.B = (self.B >> 4) | ((self.B & 0xF) << 4)
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_31(self):
        # SWAP C
        self.F = 0
        self.C = (self.C >> 4) | ((self.C & 0xF) << 4)
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_32(self):
        # SWAP D
        self.F = 0
        self.D = (self.D >> 4) | ((self.D & 0xF) << 4)
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_33(self):
        # SWAP E
        self.F = 0
        self.E = (self.E >> 4) | ((self.E & 0xF) << 4)
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_34(self):
        # SWAP H
        self.F = 0
        self.H = (self.H >> 4) | ((self.H & 0xF) << 4)
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_35(self):
        # SWAP L
        self.F = 0
        self.L = (self.L >> 4) | ((self.L & 0xF) << 4)
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_36(self):
        # SWAP (HL)
        self.F = 0
        data = self.ram.read((self.H << 8) | self.L)
        data = (data >> 4) | ((data & 0xF) << 4)
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_37(self):
        # SWAP A
        self.F = 0
        self.A = (self.A >> 4) | ((self.A & 0xF) << 4)
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_38(self):
        # SRL B
        low_bit = self.B & 1
        self.B = self.B >> 1
        self.F = low_bit * Flags.C
        if self.B == 0:
            self.F |= Flags.Z
    
    def op_CB_39(self):
        # SRL C
        low_bit = self.C & 1
        self.C = self.C >> 1
        self.F = low_bit * Flags.C
        if self.C == 0:
            self.F |= Flags.Z
    
    def op_CB_3A(self):
        # SRL D
        low_bit = self.D & 1
        self.D = self.D >> 1
        self.F = low_bit * Flags.C
        if self.D == 0:
            self.F |= Flags.Z
    
    def op_CB_3B(self):
        # SRL E
        low_bit = self.E & 1
        self.E = self.E >> 1
        self.F = low_bit * Flags.C
        if self.E == 0:
            self.F |= Flags.Z
    
    def op_CB_3C(self):
        # SRL H
        low_bit = self.H & 1
        self.H = self.H >> 1
        self.F = low_bit * Flags.C
        if self.H == 0:
            self.F |= Flags.Z
    
    def op_CB_3D(self):
        # SRL L
        low_bit = self.L & 1
        self.L = self.L >> 1
        self.F = low_bit * Flags.C
        if self.L == 0:
            self.F |= Flags.Z
    
    def op_CB_3E(self):
        # SRL (HL)
        data = self.ram.read((self.H << 8) | self.L)
        low_bit = data & 1
        data = data >> 1
        self.F = low_bit * Flags.C
        if data == 0:
            self.F |= Flags.Z
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_3F(self):
        # SRL A
        low_bit = self.A & 1
        self.A = self.A >> 1
        self.F = low_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z
    
    def op_CB_40(self):
        # BIT 0, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_41(self):
        # BIT 0, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_42(self):
        # BIT 0, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_43(self):
        # BIT 0, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_44(self):
        # BIT 0, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_45(self):
        # BIT 0, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_46(self):
        # BIT 0, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_47(self):
        # BIT 0, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x01) == 0:
            self.F |= Flags.Z
    
    def op_CB_48(self):
        # BIT 1, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_49(self):
        # BIT 1, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4A(self):
        # BIT 1, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4B(self):
        # BIT 1, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4C(self):
        # BIT 1, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4D(self):
        # BIT 1, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4E(self):
        # BIT 1, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_4F(self):
        # BIT 1, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x02) == 0:
            self.F |= Flags.Z
    
    def op_CB_50(self):
        # BIT 2, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_51(self):
        # BIT 2, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_52(self):
        # BIT 2, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_53(self):
        # BIT 2, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_54(self):
        # BIT 2, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_55(self):
        # BIT 2, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_56(self):
        # BIT 2, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_57(self):
        # BIT 2, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x04) == 0:
            self.F |= Flags.Z
    
    def op_CB_58(self):
        # BIT 3, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_59(self):
        # BIT 3, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5A(self):
        # BIT 3, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5B(self):
        # BIT 3, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5C(self):
        # BIT 3, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5D(self):
        # BIT 3, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5E(self):
        # BIT 3, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_5F(self):
        # BIT 3, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x08) == 0:
            self.F |= Flags.Z
    
    def op_CB_60(self):
        # BIT 4, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_61(self):
        # BIT 4, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_62(self):
        # BIT 4, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_63(self):
        # BIT 4, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_64(self):
        # BIT 4, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_65(self):
        # BIT 4, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_66(self):
        # BIT 4, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_67(self):
        # BIT 4, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x10) == 0:
            self.F |= Flags.Z
    
    def op_CB_68(self):
        # BIT 5, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_69(self):
        # BIT 5, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6A(self):
        # BIT 5, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6B(self):
        # BIT 5, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6C(self):
        # BIT 5, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6D(self):
        # BIT 5, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6E(self):
        # BIT 5, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_6F(self):
        # BIT 5, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x20) == 0:
            self.F |= Flags.Z
    
    def op_CB_70(self):
        # BIT 6, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_71(self):
        # BIT 6, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_72(self):
        # BIT 6, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_73(self):
        # BIT 6, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_74(self):
        # BIT 6, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_75(self):
        # BIT 6, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_76(self):
        # BIT 6, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_77(self):
        # BIT 6, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x40) == 0:
            self.F |= Flags.Z
    
    def op_CB_78(self):
        # BIT 7, B
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.B & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_79(self):
        # BIT 7, C
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.C & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7A(self):
        # BIT 7, D
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.D & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7B(self):
        # BIT 7, E
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.E & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7C(self):
        # BIT 7, H
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.H & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7D(self):
        # BIT 7, L
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.L & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7E(self):
        # BIT 7, (HL)
        self.F &= Flags.C
        self.F |= Flags.H
        data = self.ram.read((self.H << 8) | self.L)
        if (data & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_7F(self):
        # BIT 7, A
        self.F &= Flags.C
        self.F |= Flags.H
        if (self.A & 0x80) == 0:
            self.F |= Flags.Z
    
    def op_CB_80(self):
        # RES 0, B
        self.B &= ~0x01
    
    def op_CB_81(self):
        # RES 0, C
        self.C &= ~0x01
    
    def op_CB_82(self):
        # RES 0, D
        self.D &= ~0x01
    
    def op_CB_83(self):
        # RES 0, E
        self.E &= ~0x01
    
    def op_CB_84(self):
        # RES 0, H
        self.H &= ~0x01
    
    def op_CB_85(self):
        # RES 0, L
        self.L &= ~0x01
    
    def op_CB_86(self):
        # RES 0, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x01
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_87(self):
        # RES 0, A
        self.A &= ~0x01
    
    def op_CB_88(self):
        # RES 1, B
        self.B &= ~0x02
    
    def op_CB_89(self):
        # RES 1, C
        self.C &= ~0x02
    
    def op_CB_8A(self):
        # RES 1, D
        self.D &= ~0x02
    
    def op_CB_8B(self):
        # RES 1, E
        self.E &= ~0x02
    
    def op_CB_8C(self):
        # RES 1, H
        self.H &= ~0x02
    
    def op_CB_8D(self):
        # RES 1, L
        self.L &= ~0x02
    
    def op_CB_8E(self):
        # RES 1, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x02
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_8F(self):
        # RES 1, A
        self.A &= ~0x02
    
    def op_CB_90(self):
        # RES 2, B
        self.B &= ~0x04
    
    def op_CB_91(self):
        # RES 2, C
        self.C &= ~0x04
    
    def op_CB_92(self):
        # RES 2, D
        self.D &= ~0x04
    
    def op_CB_93(self):
        # RES 2, E
        self.E &= ~0x04
    
    def op_CB_94(self):
        # RES 2, H
        self.H &= ~0x04
    
    def op_CB_95(self):
        # RES 2, L
        self.L &= ~0x04
    
    def op_CB_96(self):
        # RES 2, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x04
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_97(self):
        # RES 2, A
        self.A &= ~0x04
    
    def op_CB_98(self):
        # RES 3, B
        self.B &= ~0x08
    
    def op_CB_99(self):
        # RES 3, C
        self.C &= ~0x08
    
    def op_CB_9A(self):
        # RES 3, D
        self.D &= ~0x08
    
    def op_CB_9B(self):
        # RES 3, E
        self.E &= ~0x08
    
    def op_CB_9C(self):
        # RES 3, H
        self.H &= ~0x08
    
    def op_CB_9D(self):
        # RES 3, L
        self.L &= ~0x08
    
    def op_CB_9E(self):
        # RES 3, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x08
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_9F(self):
        # RES 3, A
        self.A &= ~0x08
    
    def op_CB_A0(self):
        # RES 4, B
        self.B &= ~0x10
    
    def op_CB_A1(self):
        # RES 4, C
        self.C &= ~0x10
    
    def op_CB_A2(self):
        # RES 4, D
        self.D &= ~0x10
    
    def op_CB_A3(self):
        # RES 4, E
        self.E &= ~0x10
    
    def op_CB_A4(self):
        # RES 4, H
        self.H &= ~0x10
    
    def op_CB_A5(self):
        # RES 4, L
        self.L &= ~0x10
    
    def op_CB_A6(self):
        # RES 4, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x10
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_A7(self):
        # RES 4, A
        self.A &= ~0x10
    
    def op_CB_A8(self):
        # RES 5, B
        self.B &= ~0x20
    
    def op_CB_A9(self):
        # RES 5, C
        self.C &= ~0x20
    
    def op_CB_AA(self):
        # RES 5, D
        self.D &= ~0x20
    
    def op_CB_AB(self):
        # RES 5, E
        self.E &= ~0x20
    
    def op_CB_AC(self):
        # RES 5, H
        self.H &= ~0x20
    
    def op_CB_AD(self):
        # RES 5, L
        self.L &= ~0x20
    
    def op_CB_AE(self):
        # RES 5, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x20
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_AF(self):
        # RES 5, A
        self.A &= ~0x20
    
    def op_CB_B0(self):
        # RES 6, B
        self.B &= ~0x40
    
    def op_CB_B1(self):
        # RES 6, C
        self.C &= ~0x40
    
    def op_CB_B2(self):
        # RES 6, D
        self.D &= ~0x40
    
    def op_CB_B3(self):
        # RES 6, E
        self.E &= ~0x40
    
    def op_CB_B4(self):
        # RES 6, H
        self.H &= ~0x40
    
    def op_CB_B5(self):
        # RES 6, L
        self.L &= ~0x40
    
    def op_CB_B6(self):
        # RES 6, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x40
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_B7(self):
        # RES 6, A
        self.A &= ~0x40
    
    def op_CB_B8(self):
        # RES 7, B
        self.B &= ~0x80
    
    def op_CB_B9(self):
        # RES 7, C
        self.C &= ~0x80
    
    def op_CB_BA(self):
        # RES 7, D
        self.D &= ~0x80
    
    def op_CB_BB(self):
        # RES 7, E
        self.E &= ~0x80
    
    def op_CB_BC(self):
        # RES 7, H
        self.H &= ~0x80
    
    def op_CB_BD(self):
        # RES 7, L
        self.L &= ~0x80
    
    def op_CB_BE(self):
        # RES 7, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data &= ~0x80
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_BF(self):
        # RES 7, A
        self.A &= ~0x80
    
    def op_CB_C0(self):
        # SET 0, B
        self.B |= 0x01
    
    def op_CB_C1(self):
        # SET 0, C
        self.C |= 0x01
    
    def op_CB_C2(self):
        # SET 0, D
        self.D |= 0x01
    
    def op_CB_C3(self):
        # SET 0, E
        self.E |= 0x01
    
    def op_CB_C4(self):
        # SET 0, H
        self.H |= 0x01
    
    def op_CB_C5(self):
        # SET 0, L
        self.L |= 0x01
    
    def op_CB_C6(self):
        # SET 0, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x01
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_C7(self):
        # SET 0, A
        self.A |= 0x01
    
    def op_CB_C8(self):
        # SET 1, B
        self.B |= 0x02
    
    def op_CB_C9(self):
        # SET 1, C
        self.C |= 0x02
    
    def op_CB_CA(self):
        # SET 1, D
        self.D |= 0x02
    
    def op_CB_CB(self):
        # SET 1, E
        self.E |= 0x02
    
    def op_CB_CC(self):
        # SET 1, H
        self.H |= 0x02
    
    def op_CB_CD(self):
        # SET 1, L
        self.L |= 0x02
    
    def op_CB_CE(self):
        # SET 1, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x02
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_CF(self):
        # SET 1, A
        self.A |= 0x02
    
    def op_CB_D0(self):
        # SET 2, B
        self.B |= 0x04
    
    def op_CB_D1(self):
        # SET 2, C
        self.C |= 0x04
    
    def op_CB_D2(self):
        # SET 2, D
        self.D |= 0x04
    
    def op_CB_D3(self):
        # SET 2, E
        self.E |= 0x04
    
    def op_CB_D4(self):
        # SET 2, H
        self.H |= 0x04
    
    def op_CB_D5(self):
        # SET 2, L
        self.L |= 0x04
    
    def op_CB_D6(self):
        # SET 2, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x04
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_D7(self):
        # SET 2, A
        self.A |= 0x04
    
    def op_CB_D8(self):
        # SET 3, B
        self.B |= 0x08
    
    def op_CB_D9(self):
        # SET 3, C
        self.C |= 0x08
    
    def op_CB_DA(self):
        # SET 3, D
        self.D |= 0x08
    
    def op_CB_DB(self):
        # SET 3, E
        self.E |= 0x08
    
    def op_CB_DC(self):
        # SET 3, H
        self.H |= 0x08
    
    def op_CB_DD(self):
        # SET 3, L
        self.L |= 0x08
    
    def op_CB_DE(self):
        # SET 3, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x08
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_DF(self):
        # SET 3, A
        self.A |= 0x08
    
    def op_CB_E0(self):
        # SET 4, B
        self.B |= 0x10
    
    def op_CB_E1(self):
        # SET 4, C
        self.C |= 0x10
    
    def op_CB_E2(self):
        # SET 4, D
        self.D |= 0x10
    
    def op_CB_E3(self):
        # SET 4, E
        self.E |= 0x10
    
    def op_CB_E4(self):
        # SET 4, H
        self.H |= 0x10
    
    def op_CB_E5(self):
        # SET 4, L
        self.L |= 0x10
    
    def op_CB_E6(self):
        # SET 4, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x10
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_E7(self):
        # SET 4, A
        self.A |= 0x10
    
    def op_CB_E8(self):
        # SET 5, B
        self.B |= 0x20
    
    def op_CB_E9(self):
        # SET 5, C
        self.C |= 0x20
    
    def op_CB_EA(self):
        # SET 5, D
        self.D |= 0x20
    
    def op_CB_EB(self):
        # SET 5, E
        self.E |= 0x20
    
    def op_CB_EC(self):
        # SET 5, H
        self.H |= 0x20
    
    def op_CB_ED(self):
        # SET 5, L
        self.L |= 0x20
    
    def op_CB_EE(self):
        # SET 5, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x20
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_EF(self):
        # SET 5, A
        self.A |= 0x20
    
    def op_CB_F0(self):
        # SET 6, B
        self.B |= 0x40
    
    def op_CB_F1(self):
        # SET 6, C
        self.C |= 0x40
    
    def op_CB_F2(self):
        # SET 6, D
        self.D |= 0x40
    
    def op_CB_F3(self):
        # SET 6, E
        self.E |= 0x40
    
    def op_CB_F4(self):
        # SET 6, H
        self.H |= 0x40
    
    def op_CB_F5(self):
        # SET 6, L
        self.L |= 0x40
    
    def op_CB_F6(self):
        # SET 6, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x40
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_F7(self):
        # SET 6, A
        self.A |= 0x40
    
    def op_CB_F8(self):
        # SET 7, B
        self.B |= 0x80
    
    def op_CB_F9(self):
        # SET 7, C
        self.C |= 0x80
    
    def op_CB_FA(self):
        # SET 7, D
        self.D |= 0x80
    
    def op_CB_FB(self):
        # SET 7, E
        self.E |= 0x80
    
    def op_CB_FC(self):
        # SET 7, H
        self.H |= 0x80
    
    def op_CB_FD(self):
        # SET 7, L
        self.L |= 0x80
    
    def op_CB_FE(self):
        # SET 7, (HL)
        data = self.ram.read((self.H << 8) | self.L)
        data |= 0x80
        self.ram.write((self.H << 8) | self.L, data)
    
    def op_CB_FF(self):
        # SET 7, A
        self.A |= 0x80

    def int_vblank(self):
        # Attempt to setup a vblank interrupt
        ints = self.ram.read(0xFF0F)
        self.ram.write(0xFF0F, ints | 0x1)

    def int_lcds(self):
        # Attempt to setup a LCD stat interrupt
        ints = self.ram.read(0xFF0F)
        self.ram.write(0xFF0F, ints | 0x2)

    def int_timer(self):
        # Attempt to setup a timer interrupt
        ints = self.ram.read(0xFF0F)
        self.ram.write(0xFF0F, ints | 0x4)

    def int_serial(self):
        # Attempt to setup a serial interrupt
        ints = self.ram.read(0xFF0F)
        self.ram.write(0xFF0F, ints | 0x8)

    def int_joypad(self):
        # Attempt to setup a joypad interrupt
        ints = self.ram.read(0xFF0F)
        self.ram.write(0xFF0F, ints | 0x10)

class gb_ram(object):
    def __init__(self):
        self.joypad_obj = None # joypad obj for input register
        self.rom = [] # Cartridge ROM
        self.vram = [0x00] * 0x2000 # Video RAM
        self.eram = [0x00] * 0x8000 # External RAM
        self.iram = [0x00] * 0x2000 # Internal RAM
        self.sprite_info = [0x00] * 0xA0
        self.zram = [0x00] * 0x80 # Zero-page RAM

        self.mmio = [0x00] * 0x80 # Memory mapped IO
        # Initial MMIO values
        self.mmio[0x10] = 0x80
        self.mmio[0x11] = 0xBF
        self.mmio[0x12] = 0xF3
        self.mmio[0x14] = 0xBF
        self.mmio[0x16] = 0x3F
        self.mmio[0x19] = 0xBF
        self.mmio[0x1A] = 0x7F
        self.mmio[0x1B] = 0xFF
        self.mmio[0x1C] = 0x9F
        self.mmio[0x1E] = 0xBF
        self.mmio[0x20] = 0xFF
        self.mmio[0x23] = 0xBF
        self.mmio[0x24] = 0x77
        self.mmio[0x25] = 0xF3
        self.mmio[0x26] = 0xF1
        self.mmio[0x40] = 0x91
        self.mmio[0x47] = 0xFC
        self.mmio[0x48] = 0xFF
        self.mmio[0x49] = 0xFF

        self.mbc_type = 0 # 0 = no switching, 1/2/3/5 for MBC 1/2/3/5

        # MBC1 registers
        self.mbc1_mode = 0 # 0 = 16/8 mode, 1 = 4/32 mode
        self.mbc1_rom_bank = 1 # 5/7 bit rom bank index
        self.mbc1_ram_bank = 0 # 2 bit ram bank index

        # MBC3 registers
        self.mbc3_rom_bank = 1
        self.mbc3_ram_bank = 0 # Also holds selected RTC register
        self.mbc3_rtc_count = 0 # Ticks except when halt flag is set in dh
        self.mbc3_rtc_cycles_per_second = 4194304
        self.mbc3_rtc_countdown = self.mbc3_rtc_cycles_per_second
        self.mbc3_rtc_s = 0
        self.mbc3_rtc_m = 0
        self.mbc3_rtc_h = 0
        self.mbc3_rtc_dl = 0
        self.mbc3_rtc_dh = 0
        self.mbc3_latch = 0

    def load_rom(self, fname):
        rom_string = open(fname).read()
        self.rom = [ord(c) for c in rom_string]

        # Set up mbc
        rom_type = self.rom[0x0147]
        if rom_type in (0, 8, 9):
            self.mbc_type = 0
        elif rom_type in (1, 2, 3):
            self.mbc_type = 1
        elif rom_type in (5, 6):
            self.mbc_type = 2
        elif rom_type in (0x12, 0x13):
            self.mbc_type = 3
        elif rom_type in (0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E):
            self.mbc_type = 5

    def dump(self):
        output = ""
        for row in range(0, 0x10000, 0x10):
            line = "%04x: " % row
            line += ' '.join("%02x" % self.read(p) for p in range(row, row+0x10))
            output += line + "\n"
        return output

    def read(self, p):
        if p >= 0xFF80:
            # Zero page RAM
            return self.zram[p - 0xFF80]
        elif p >= 0xFF00:
            return self.mmio[p - 0xFF00]
        elif p >= 0xFEA0:
            # Nothing here
            return 0
        elif p >= 0xFE00:
            # Sprite info
            return self.sprite_info[p - 0xFE00]
        elif p >= 0xE000:
            # Working RAM Shadow
            return self.iram[p - 0xE000]
        elif p >= 0xC000:
            # Working RAM
            return self.iram[p - 0xC000]
        elif p >= 0xA000:
            # External RAM
            if self.mbc_type == 3:
                if self.mbc3_ram_bank < 4:
                    return self.eram[p - 0xA000 + 0x2000 * self.mbc3_ram_bank]
                elif self.mbc3_ram_bank == 0x08:
                    return self.mbc3_rtc_s
                elif self.mbc3_ram_bank == 0x09:
                    return self.mbc3_rtc_m
                elif self.mbc3_ram_bank == 0x0A:
                    return self.mbc3_rtc_h
                elif self.mbc3_ram_bank == 0x0B:
                    return self.mbc3_rtc_dl
                elif self.mbc3_ram_bank == 0x0C:
                    return self.mbc3_rtc_dh
                else:
                    assert False, "Invalid RAM Bank number %x" % self.mbc3_ram_bank
            else:
                return self.eram[p - 0xA000]
        elif p >= 0x8000:
            # Graphics RAM
            return self.vram[p - 0x8000]
        elif p >= 0x4000:
            # ROM, switchable bank
            # TODO - Implement all MBCs
            if self.mbc_type == 0:
                return self.rom[p]
            elif self.mbc_type == 1:
                if self.mbc1_rom_bank == 0:
                    return self.rom[p]
                else:
                    return self.rom[p + 0x4000 * (self.mbc1_rom_bank - 1)]
            elif self.mbc_type == 3:
                if self.mbc3_rom_bank == 0:
                    return self.rom[p]
                else:
                    return self.rom[p + 0x4000 * (self.mbc3_rom_bank - 1)]
            else:
                assert False, "This MBC type not implemented"
        else:
            # ROM bank 0
            return self.rom[p]

    def write(self, p, d):
        d = d & 0xFF
        if p >= 0xFF80:
            # Zero page RAM
            self.zram[p - 0xFF80] = d
        elif p >= 0xFF00:
            self.mmio[p - 0xFF00] = d
            if p == 0xFF00 and self.joypad_obj is not None:
                # Input register
                if d & 0x30 == 0x10:
                    self.mmio[0] |= self.joypad_obj.P15_mask()
                elif d & 0x30 == 0x20:
                    self.mmio[0] |= self.joypad_obj.P14_mask()
            elif p == 0xFF46:
                # Transfer data from RAM to OAM
                offset = self.mmio[0x46] * 0x0100
                for i in range(0xA0):
                    self.sprite_info[i] = self.read(offset+i)
            elif p == 0xFF02:
                if d & 0x80 == 0x80:
                    sys.stdout.write(chr(self.mmio[0x01]))
        elif p >= 0xFEA0:
            # Nothing here
            return
        elif p >= 0xFE00:
            # Sprite info
            self.sprite_info[p - 0xFE00] = d
        elif p >= 0xE000:
            # Working RAM Shadow
            self.iram[p - 0xE000] = d
        elif p >= 0xC000:
            # Working RAM
            self.iram[p - 0xC000] = d
        elif p >= 0xA000:
            # External RAM
            if self.mbc_type == 3:
                if self.mbc3_ram_bank < 0x4:
                    self.eram[p - 0xA000 + 0x2000 * self.mbc3_ram_bank] = d
                else:
                    # Write to RTC register
                    if self.mbc3_ram_bank == 0x8:
                        self.mbc3_rtc_s = d
                    elif self.mbc3_ram_bank == 0x9:
                        self.mbc3_rtc_m = d
                    elif self.mbc3_ram_bank == 0xA:
                        self.mbc3_rtc_h = d
                    elif self.mbc3_ram_bank == 0xB:
                        self.mbc3_rtc_dl = d
                    elif self.mbc_3_ram_bank == 0xC:
                        self.mbc3_rtc_dh = d
                    # Update self.mbc3_rtc_count
                    day_count = ((self.mbc3_rtc_dh & 1) << 8) + self.mbc3_rtc_dl
                    self.mbc3_rtc_count = day_count * 86400 + self.mbc3_rtc_h * 3600 + self.mbc3_rtc_m * 60 + self.mbc_rtc_s
            else:
                self.eram[p - 0xA000] = d
        elif p >= 0x8000:
            # Graphics RAM
            self.vram[p - 0x8000] = d
        else:
            # Attempt to write into ROM area
            # Does not actually write, but interfaces with the MBC
            # TODO - fill in
            if self.mbc_type == 1:
                if p >= 0x6000:
                    self.mbc1_mode = d & 1
                    # print "MBC1 mode %d" % self.mbc1_mode
                elif p >= 0x4000:
                    if self.mbc1_mode == 0:
                        self.mbc1_rom_bank &= 0x1F
                        self.mbc1_rom_bank |= (d & 3) << 5
                    else:
                        self.mbc1_ram_bank = d & 3
                    # print "Selected ROM bank %d" % self.mbc1_rom_bank
                elif p >= 0x2000:
                    self.mbc1_rom_bank &= 0x60
                    self.mbc1_rom_bank |= (d & 0x1F)
                    # print "Selected ROM bank %d" % self.mbc1_rom_bank
                else:
                    # Technically should enable/disable RAM bank
                    pass
            elif self.mbc_type == 3:
                if p >= 0x6000:
                    if d == 1 and self.mbc3_latch == 0:
                        # Latch clock data
                        self.mbc3_rtc_s = self.mbc3_rtc_count % 60
                        self.mbc3_rtc_m = (self.mbc3_rtc_count / 60) % 60
                        self.mbc3_rtc_h = (self.mbc3_rtc_count / 3600) % 24
                        self.mbc3_rtc_dl = (self.mbc3_rtc_count / 86400) & 0xFF
                        self.mbc3_rtc_dh &= 0xFE
                        self.mbc3_rtc_dh |= ((self.mbc3_rtc_count / 86400) >> 8) & 1
                        if self.mbc3_rtc_count > 44236800:
                            self.mbc3_rtc_dh |= 0x80
                    self.mbc3_latch = d
                elif p >= 0x4000:
                    self.mbc3_ram_bank = d
                elif p >= 0x2000:
                    self.mbc3_rom_bank = d
                else:
                    # Technically should enable RAM and timer, we'll just have them always on for convenience
                    pass
            elif self.mbc_type == 0:
                # Do nothing
                pass
            else:
                assert False, "MBC type %d not implemented" % self.mbc_type
            return

class GPUFlags:
    BGON = 0x01 # Background on
    SPON = 0x02 # Sprites on
    SPSZ = 0x04 # Sprite size (0 = 8x8, 1 = 16x16)
    BGMAP = 0x08 # Background map
    BGSET = 0x10 # Background tileset
    WINON = 0x20 # Window on
    WINMAP = 0x40 # Window tilemap
    DISPON = 0x80 # Display on

class gb_gpu(object):
    def __init__(self, cpu_obj, ram_obj):
        self.cpu = cpu_obj
        self.ram = ram_obj
        self.modeclock = 0
        self.mode = 0
        self.line = 0
        self.pixels = [None] * 144
        for i in range(144):
            self.pixels[i] = [0x0] * 160

    def __str__(self):
        return """
GPU Mode: %d    Mode Clock: %d    Line: %3d (%02x)
""" % (self.mode, self.modeclock, self.line, self.line)

    def pixmap_str(self):
        return '\n'.join(''.join(str(p) for p in pix_row) for pix_row in self.pixels)

    # dt is the number of cycles since the last update
    def update(self, dt):
        self.modeclock += dt
        if self.mode == 2:
            # OAM read mode
            if self.modeclock >= 80:
                self.modeclock = 0
                self.mode = 3
        elif self.mode == 3:
            # VRAM read mode
            if self.modeclock >= 172:
                self.write_scanline()

                self.modeclock = 0
                self.mode = 0
        elif self.mode == 0:
            # HBLANK
            if self.modeclock >= 204:
                self.modeclock = 0
                self.line += 1
                if self.line == 143:
                    # Move to VBLANK
                    self.mode = 1

                    # Trigger vblank interrupt
                    self.cpu.int_vblank()
                else:
                    self.mode = 2
        elif self.mode == 1:
            # VBLANK for equivalent of 10 lines
            if self.modeclock >= 456:
                self.modeclock = 0
                self.line += 1
                if self.line > 153:
                    # Done with VBLANK
                    self.mode = 2
                    self.line = 0

        # Update MMIO registers
        self.ram.mmio[0x44] = self.line

    def write_scanline(self):
        flags = self.ram.mmio[0x40]
        scy = self.ram.mmio[0x42]
        scx = self.ram.mmio[0x43]

        # print "scy: %d, scx: %d" % (scy, scx)
        if flags & GPUFlags.BGON == GPUFlags.BGON:
            # Display background
            bg_pallette = self.ram.mmio[0x47]

            if (flags & GPUFlags.BGMAP) == 0:
                map_offset = 0x1800
            else:
                map_offset = 0x1C00

            map_line = ((self.line + scy) & 0xFF) >> 3
            pix_line = ((self.line + scy) & 0xFF) & 7
            # The tiles for this line
            # Each line consists of 32 tileset indices
            tiles = self.ram.vram[map_offset + map_line * 32 : map_offset + (map_line + 1) * 32]

            for pix in range(160):
                tile_index = ((pix + scx) & 0xFF) >> 3
                tile_bit = 7 - (((pix + scx) & 0xFF) & 7)

                tile_no = tiles[tile_index]

                # Account for different location of tileset 1
                if (flags & GPUFlags.BGSET) == 0 and tile_no < 0x80:
                    tile_no += 0x100

                tile_lo = self.ram.vram[tile_no * 0x10 + pix_line * 2]
                tile_hi = self.ram.vram[tile_no * 0x10 + pix_line * 2 + 1]

                pix_hi = ((tile_hi & (1 << tile_bit)) >> tile_bit)
                pix_lo = ((tile_lo & (1 << tile_bit)) >> tile_bit)

                pallette_index = pix_hi * 2 + pix_lo 
                self.pixels[self.line][pix] = (bg_pallette >> (pallette_index * 2)) & 3
        if (flags & GPUFlags.WINON) == GPUFlags.WINON:
            # Window layer
            x_pos = self.ram.read(0xFF4B) - 7
            y_pos = self.ram.read(0xFF4A)
            
            if (flags & GPUFlags.WINMAP) == 0:
                map_offset = 0x1800
            else:
                map_offset = 0x1C00

            bg_pallette = self.ram.mmio[0x47]

            if self.line >= y_pos:
                map_line = (self.line - y_pos) / 8
                pix_line = (self.line - y_pos) & 7

                tiles = self.ram.vram[map_offset + map_line * 32 : map_offset + (map_line + 1) * 32]

                for pix in range(x_pos, 160):
                    tile_index = (pix - x_pos) >> 3
                    tile_bit = 7 - ((pix - x_pos) & 7)

                    tile_no = tiles[tile_index]

                    if (flags & GPUFlags.BGSET) == 0 and tile_no < 0x80:
                        tile_no += 0x100

                    tile_lo = self.ram.vram[tile_no * 0x10 + pix_line * 2]
                    tile_hi = self.ram.vram[tile_no * 0x10 + pix_line * 2 + 1]

                    pix_hi = ((tile_hi & (1 << tile_bit)) >> tile_bit)
                    pix_lo = ((tile_lo & (1 << tile_bit)) >> tile_bit)

                    pallette_index = pix_hi * 2 + pix_lo
                    self.pixels[self.line][pix] = (bg_pallette >> (pallette_index * 2)) & 3
        if (flags & GPUFlags.SPON) == GPUFlags.SPON:
            # Draw sprites
            sprite_mode = flags & GPUFlags.SPSZ
            for sprite_index in range(40):
                sprite_off = 0x4 * sprite_index
                y_pos = self.ram.sprite_info[sprite_off] - 16
                x_pos = self.ram.sprite_info[sprite_off+1] - 8
                tile_index = self.ram.sprite_info[sprite_off+2]
                sprite_flags = self.ram.sprite_info[sprite_off+3]

                if sprite_mode == 0:
                    # 8x8 mode
                    above = ((sprite_flags & 0x80) == 0)
                    y_flip = ((sprite_flags & 0x40) == 0x40)
                    x_flip = ((sprite_flags & 0x20) == 0x20)
                    pal_num = ((sprite_flags & 0x10) / 0x10)
                    if pal_num == 0:
                        pallette = self.ram.mmio[0x48]
                    else:
                        pallette = self.ram.mmio[0x49]

                    if y_pos <= self.line and y_pos > self.line - 8:
                        if not y_flip:
                            pix_line = self.line - y_pos
                        else:
                            pix_line = 7 - (self.line - y_pos)
                        for pix in range(max(x_pos, 0), min(x_pos + 8, 159)):
                            if x_flip:
                                tile_bit = pix - x_pos
                            else:
                                tile_bit = 7 - (pix - x_pos)

                            tile_lo = self.ram.vram[tile_index * 0x10 + pix_line * 2]
                            tile_hi = self.ram.vram[tile_index * 0x10 + pix_line * 2 + 1]

                            pix_hi = ((tile_hi & (1 << tile_bit)) >> tile_bit)
                            pix_lo = ((tile_lo & (1 << tile_bit)) >> tile_bit)

                            pallette_index = pix_hi * 2 + pix_lo
                            if pallette_index != 0:
                                color = (pallette >> (pallette_index * 2)) & 3
                                
                                if (above or self.pixels[self.line][pix] == 0):
                                    self.pixels[self.line][pix] = color
                else:
                    # 8x16 mode
                    pass

class gb_joypad(object):
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.A = False
        self.B = False
        self.start = False
        self.select = False

    def P14_mask(self):
        mask = 0xF
        if self.right:
            mask &= ~0x1
        if self.left:
            mask &= ~0x2
        if self.up:
            mask &= ~0x4
        if self.down:
            mask &= ~0x8
        return mask

    def P15_mask(self):
        mask = 0xF
        if self.A:
            mask &= ~0x1
        if self.B:
            mask &= ~0x2
        if self.select:
            mask &= ~0x4
        if self.start:
            mask &= ~0x8
        return mask
