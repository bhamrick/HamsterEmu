class Flags:
    Z = 0x80
    N = 0x40
    H = 0x20
    C = 0x10

class gb_cpu(object):
    def __init__(self):
        # Initialize registers
        self.A = 0
        self.B = 0
        self.D = 0
        self.H = 0
        self.F = 0
        self.C = 0
        self.E = 0
        self.L = 0
        self.SP = 0
        self.PC = 0x100
        self.halted = False
        self.interrupts = False
        self.ram = gb_ram()
        # Opcode format:
        # (arg_lengths, func), where arg_lengths is a tuple giving the byte length of each argument
        self.opcodes = [
            ((), op_00),
            ((2), op_01),
            ((), op_02),
            ((), op_03),
            ((), op_04),
            ((), op_05),
            ((1), op_06),
            ((), op_07),
            ((2), op_08),
            ((), op_09),
            ((), op_0A),
            ((), op_0B),
            ((), op_0C),
            ((), op_0D),
            ((1), op_0E),
            ((), op_0F),
            ((1), op_10),
            ((2), op_11),
            ((), op_12),
            ((), op_13),
            ((), op_14),
            ((), op_15),
            ((1), op_16),
            ((), op_17),
            ((1), op_18),
            ((), op_19),
            ((), op_1A),
            ((), op_1B),
            ((), op_1C),
            ((), op_1D),
            ((1), op_1E),
            ((), op_1F),
            ((1), op_20),
            ((2), op_21),
            ((), op_22),
            ((), op_23),
            ((), op_24),
            ((), op_25),
            ((1), op_26),
            ((), op_27),
            ((1), op_28),
            ((), op_29),
            ((), op_2A),
            ((), op_2B),
            ((), op_2C),
            ((), op_2D),
            ((1), op_2E),
            ((), op_2F),
            ((1), op_30),
            ((2), op_31),
            ((), op_32),
            ((), op_33),
            ((), op_34),
            ((), op_35),
            ((1), op_36),
            ((), op_37),
            ((1), op_38),
            ((), op_39),
            ((), op_3A),
            ((), op_3B),
            ((), op_3C),
            ((), op_3D),
            ((1), op_3E),
            ((), op_3F),
            ((), op_40),
            ((), op_41),
            ((), op_42),
            ((), op_43),
            ((), op_44),
            ((), op_45),
            ((), op_46),
            ((), op_47),
            ((), op_48),
            ((), op_49),
            ((), op_4A),
            ((), op_4B),
            ((), op_4C),
            ((), op_4D),
            ((), op_4E),
            ((), op_4F),
            ((), op_50),
            ((), op_51),
            ((), op_52),
            ((), op_53),
            ((), op_54),
            ((), op_55),
            ((), op_56),
            ((), op_57),
            ((), op_58),
            ((), op_59),
            ((), op_5A),
            ((), op_5B),
            ((), op_5C),
            ((), op_5D),
            ((), op_5E),
            ((), op_5F),
            ((), op_60),
            ((), op_61),
            ((), op_62),
            ((), op_63),
            ((), op_64),
            ((), op_65),
            ((), op_66),
            ((), op_67),
            ((), op_68),
            ((), op_69),
            ((), op_6A),
            ((), op_6B),
            ((), op_6C),
            ((), op_6D),
            ((), op_6E),
            ((), op_6F),
            ((), op_70),
            ((), op_71),
            ((), op_72),
            ((), op_73),
            ((), op_74),
            ((), op_75),
            ((), op_76),
            ((), op_77),
            ((), op_78),
            ((), op_79),
            ((), op_7A),
            ((), op_7B),
            ((), op_7C),
            ((), op_7D),
            ((), op_7E),
            ((), op_7F),
            ((), op_80),
            ((), op_81),
            ((), op_82),
            ((), op_83),
            ((), op_84),
            ((), op_85),
            ((), op_86),
            ((), op_87),
            ((), op_88),
            ((), op_89),
            ((), op_8A),
            ((), op_8B),
            ((), op_8C),
            ((), op_8D),
            ((), op_8E),
            ((), op_8F),
            ((), op_90),
            ((), op_91),
            ((), op_92),
            ((), op_93),
            ((), op_94),
            ((), op_95),
            ((), op_96),
            ((), op_97),
            ((), op_98),
            ((), op_99),
            ((), op_9A),
            ((), op_9B),
            ((), op_9C),
            ((), op_9D),
            ((), op_9E),
            ((), op_9F),
            ((), op_A0),
            ((), op_A1),
            ((), op_A2),
            ((), op_A3),
            ((), op_A4),
            ((), op_A5),
            ((), op_A6),
            ((), op_A7),
            ((), op_A8),
            ((), op_A9),
            ((), op_AA),
            ((), op_AB),
            ((), op_AC),
            ((), op_AD),
            ((), op_AE),
            ((), op_AF),
            ((), op_B0),
            ((), op_B1),
            ((), op_B2),
            ((), op_B3),
            ((), op_B4),
            ((), op_B5),
            ((), op_B6),
            ((), op_B7),
            ((), op_B8),
            ((), op_B9),
            ((), op_BA),
            ((), op_BB),
            ((), op_BC),
            ((), op_BD),
            ((), op_BE),
            ((), op_BF),
            ((), op_C0),
            ((), op_C1),
            ((2), op_C2),
            ((2), op_C3),
            ((2), op_C4),
            ((), op_C5),
            ((1), op_C6),
            ((), op_C7),
            ((), op_C8),
            ((), op_C9),
            ((2), op_CA),
            ((1), op_CB),
            ((2), op_CC),
            ((2), op_CD),
            ((1), op_CE),
            ((), op_CF),
            ((), op_D0),
            ((), op_D1),
            ((2), op_D2),
            ((), op_D3),
            ((2), op_D4),
            ((), op_D5),
            ((1), op_D6),
            ((), op_D7),
            ((), op_D8),
            ((), op_D9),
            ((2), op_DA),
            ((), op_DB),
            ((2), op_DC),
            ((), op_DD),
            ((), op_DE),
            ((), op_DF),
            ((1), op_E0),
            ((), op_E1),
            ((), op_E2),
            ((), op_E3),
            ((), op_E4),
            ((), op_E5),
            ((1), op_E6),
            ((), op_E7),
            ((1), op_E8),
            ((), op_E9),
            ((2), op_EA),
            ((), op_EB),
            ((), op_EC),
            ((), op_ED),
            ((1), op_EE),
            ((), op_EF),
            ((1), op_F0),
            ((), op_F1),
            ((), op_F2),
            ((), op_F3),
            ((), op_F4),
            ((), op_F5),
            ((1), op_F6),
            ((), op_F7),
            ((1), op_F8),
            ((), op_F9),
            ((2), op_FA),
            ((), op_FB),
            ((), op_FC),
            ((), op_FD),
            ((1), op_FE),
            ((), op_FF),
            ]

    def load_rom(self, fname):
        self.ram.load_rom(fname)

    def execute_next_instruction(self):
        op = self.ram.read(self.PC)
        self.PC += 1

        op_details = self.opcodes[op]
        args = []
        for l in op_details[0]:
            a = 0
            for i in range(l):
                a += self.ram.read(self.PC) << (8*i)
                self.PC += 1
            args.append(a)
        op_detals[1](self, *args)

    def op_00(self):
        # NOP
        pass

    def op_01(self, data):
        # LD BC, data
        self.B = data >> 8
        self.C = data & 0xFF

    def op_02(self):
        self.ram.write((self.B << 8) | self.C, self.A)

    def op_03(self):
        # INC BC
        self.C = (self.C + 1) & 0xFF
        if self.C == 0:
            self.B + (self.B + 1) & 0xFF

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
        if (self.B & 0xF) != 0xF:
            self.F |= Flags.H

    def op_06(self, data):
        # LD B, n
        self.B = data

    def op_07(self):
        # RLCA - rotate A left, both carry flag and bit 0 now contain old bit 7
        high_bit = (self.A & 0x80) / 0x80
        self.A = ((self.A << 1) & 0xFF) | high_bit
        self.F = high_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z

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
        if (self.C & 0xF) != 0xF:
            self.F |= Flags.H

    def op_0E(self, data):
        # LD C, n
        self.C = data

    def op_0F(self):
        # RRCA - rotate A right, bit 0 to bit 7 and carry flag
        low_bit = self.A & 0x1
        self.A = (self.A >> 1) | (low_bit << 7)
        self.F = low_bit * Flags.C
        if self.A == 0:
            self.F |= Flags.Z

    def op_10(self, data):
        if data == 0:
            # STOP
            # For now implemented as HALT
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
            self.D + (self.D + 1) & 0xFF

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
        if (self.D & 0xF) != 0xF:
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
        if self.A == 0:
            self.F |= Flags.Z

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
        if (self.E & 0xF) != 0xF:
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
        if self.A == 0:
            self.F |= Flags.Z

    def op_20(self, offset):
        # JRNZ n
        # Fix sign
        if offset > 0x7F:
            offset = offset - 0x100
        if (self.F & Flags.Z) == 0:
            self.PC = self.PC + offset

    def op_21(self, data):
        self.H = data >> 8
        self.L = data & 0xFF

    def op_22(self):
        # LDI (HL), A
        self.ram.write((self.H << 8) | self.L, self.A)
        if L < 0xFF:
            L += 1
        else:
            L = 0
            H = (H + 1) & 0xFF

    def op_23(self):
        # INC HL
        self.L = (self.L + 1) & 0xFF
        if self.L == 0:
            self.H + (self.H + 1) & 0xFF

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
        if (self.H & 0xF) != 0xF:
            self.F |= Flags.H

    def op_26(self, data):
        # LD H, n
        self.H = data

    def op_27(self):
        # DAA - adjust Binary Coded Decimal results
        # Leave N flag alone
        self.F &= Flags.N
        if self.A & 0xF > 9:
            self.F |= Flags.C
            self.A -= 10
            self.A += 0x10
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
        if L < 0xFF:
            L += 1
        else:
            L = 0x00
            H = (H + 1) & 0xFF

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
        if (self.L & 0xF) != 0xF:
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
        if L > 0:
            L -= 1
        else:
            L = 0xFF
            H = (H - 1) & 0xFF

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
        if (data & 0xF) != 0xF:
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
        if L > 0:
            L -= 1
        else:
            L = 0xFF
            H = (H - 1) & 0xFF

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
        if (self.A & 0xF) != 0xF:
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
        if (self.A & 7) >= (self.B & 7):
            self.F |= Flags.H
        if self.A >= self.B:
            self.F |= Flags.C
        self.A = (self.A - self.B) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_91(self):
        # SUB A, C
        self.F = Flags.N
        if (self.A & 7) >= (self.C & 7):
            self.F |= Flags.H
        if self.A >= self.C:
            self.F |= Flags.C
        self.A = (self.A - self.C) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_92(self):
        # SUB A, D
        self.F = Flags.N
        if (self.A & 7) >= (self.D & 7):
            self.F |= Flags.H
        if self.A >= self.D:
            self.F |= Flags.C
        self.A = (self.A - self.D) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_93(self):
        # SUB A, E
        self.F = Flags.N
        if (self.A & 7) >= (self.E & 7):
            self.F |= Flags.H
        if self.A >= self.E:
            self.F |= Flags.C
        self.A = (self.A - self.E) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_94(self):
        # SUB A, H
        self.F = Flags.N
        if (self.A & 7) >= (self.H & 7):
            self.F |= Flags.H
        if self.A >= self.H:
            self.F |= Flags.C
        self.A = (self.A - self.H) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_95(self):
        # SUB A, L
        self.F = Flags.N
        if (self.A & 7) >= (self.L & 7):
            self.F |= Flags.H
        if self.A >= self.L:
            self.F |= Flags.C
        self.A = (self.A - self.L) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_96(self):
        # SUB A, (HL)
        self.F = Flags.N
        data = self.ram.read((self.H << 8) | self.L)
        if (self.A & 7) >= (data & 7):
            self.F |= Flags.H
        if self.A >= data:
            self.F |= Flags.C
        self.A = (self.A - data) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_97(self):
        # SUB A, A
        self.F = Flags.N
        if (self.A & 7) >= (self.A & 7):
            self.F |= Flags.H
        if self.A >= self.A:
            self.F |= Flags.C
        self.A = (self.A - self.A) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_98(self):
        # SBC A, B
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.B + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.B + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.B - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_99(self):
        # SBC A, C
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.C + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.C + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.C - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9A(self):
        # SBC A, D
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.D + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.D + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.D - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9B(self):
        # SBC A, E
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.E + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.E + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.E - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9C(self):
        # SBC A, H
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.H + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.H + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.H - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9D(self):
        # SBC A, L
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.L + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.L + c_flag:
            self.F |= Flags.C
        self.A = (self.A - self.L - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9E(self):
        # SBC A, (HL)
        c_flag = (self.F & Flags.C) / Flags.C
        data = self.ram.read((self.H << 8) | self.L)
        self.F = Flags.N
        if (self.A & 0xF) >= (data + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= data + c_flag:
            self.F |= Flags.C
        self.A = (self.A - data - c_flag) & 0xFF
        if self.A == 0:
            self.F |= Flags.Z

    def op_9F(self):
        # SBC A, A
        c_flag = (self.F & Flags.C) / Flags.C
        self.F = Flags.N
        if (self.A & 0xF) >= (self.A + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= self.A + c_flag:
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
        self.A = self.A | self.L
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
        if (self.A & 0xF) >= (self.B & 0xF):
            self.F |= Flags.H
        if self.A >= self.B:
            self.F |= Flags.C

    def op_B9(self):
        # CP A, C
        self.F = Flags.N
        if self.A == self.C:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.C & 0xF):
            self.F |= Flags.H
        if self.A >= self.C:
            self.F |= Flags.C
    
    def op_BA(self):
        # CP A, D
        self.F = Flags.N
        if self.A == self.D:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.D & 0xF):
            self.F |= Flags.H
        if self.A >= self.D:
            self.F |= Flags.C
    
    def op_BB(self):
        # CP A, E
        self.F = Flags.N
        if self.A == self.E:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.E & 0xF):
            self.F |= Flags.H
        if self.A >= self.E:
            self.F |= Flags.C
    
    def op_BC(self):
        # CP A, H
        self.F = Flags.N
        if self.A == self.H:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.H & 0xF):
            self.F |= Flags.H
        if self.A >= self.H:
            self.F |= Flags.C
    
    def op_BD(self):
        # CP A, L
        self.F = Flags.N
        if self.A == self.L:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.L & 0xF):
            self.F |= Flags.H
        if self.A >= self.L:
            self.F |= Flags.C
    
    def op_BE(self):
        # CP A, (HL)
        self.F = Flags.N
        data = self.ram.read((self.H << 8) | self.L)
        if self.A == data:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (data & 0xF):
            self.F |= Flags.H
        if self.A >= data:
            self.F |= Flags.C
    
    def op_BF(self):
        # CP A, A
        self.F = Flags.N
        if self.A == self.A:
            self.F |= Flags.Z
        if (self.A & 0xF) >= (self.A & 0xF):
            self.F |= Flags.H
        if self.A >= self.A:
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

    def op_CB(self, reg_id):
        # Extra ops
        self.F = 0
        if reg_id == 0x37:
            # SWAP A
            self.A = (self.A >> 4) | ((self.A & 0xF) << 4)
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x07:
            # RLC A
            high_bit = (self.A & 0x80) >> 7
            self.A = ((self.A << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x17:
            # RL A
            high_bit = (self.A & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.A = ((self.A << 1) & 0xFF) | c_flag
            self.F = high_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0F:
            # RRC A
            low_bit = (self.A & 1)
            self.A = (self.A >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x30:
            # SWAP B
            self.B = (self.B >> 4) | ((self.B & 0xF) << 4)
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x00:
            # RLC B
            high_bit = (self.B & 0x80) >> 7
            self.B = ((self.B << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x10:
            # RL B
            high_bit = (self.B & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.B = ((self.B << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x31:
            # SWAP C
            self.C = (self.C >> 4) | ((self.C & 0xF) << 4)
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x01:
            # RLC C
            high_bit = (self.C & 0x80) >> 7
            self.C = ((self.C << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x11:
            # RL C
            high_bit = (self.C & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.C = ((self.C << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x32:
            # SWAP D
            self.D = (self.D >> 4) | ((self.D & 0xF) << 4)
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x02:
            # RLC D
            high_bit = (self.D & 0x80) >> 7
            self.D = ((self.D << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x12:
            # RL D
            high_bit = (self.D & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.D = ((self.D << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x33:
            # SWAP E
            self.E = (self.E >> 4) | ((self.E & 0xF) << 4)
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x03:
            # RLC E
            high_bit = (self.E & 0x80) >> 7
            self.E = ((self.E << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x13:
            # RL E
            high_bit = (self.E & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.E = ((self.E << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x34:
            # SWAP H
            self.H = (self.H >> 4) | ((self.H & 0xF) << 4)
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x04:
            # RLC H
            high_bit = (self.H & 0x80) >> 7
            self.H = ((self.H << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x14:
            # RL H
            high_bit = (self.H & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.H = ((self.H << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x35:
            # SWAP L
            self.L = (self.L >> 4) | ((self.L & 0xF) << 4)
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x05:
            # RLC L
            high_bit = (self.L & 0x80) >> 7
            self.L = ((self.L << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x15:
            # RL L
            high_bit = (self.L & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            self.L = ((self.L << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x36:
            # SWAP (HL)
            data = self.ram.read((self.H << 8) | self.L)
            data = (data >> 4) | ((data & 0xF) << 4)
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x06:
            # RLC (HL)
            data = self.ram.read((self.H << 8) | self.L)
            high_bit = (data & 0x80) >> 7
            data = ((data << 1) & 0xFF) | high_bit
            self.F = high_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x16:
            # RL (HL)
            data = self.ram.read((self.H << 8) | self.L)
            high_bit = (data & 0x80) >> 7
            c_flag = (self.F & Flags.C) / Flags.C
            data = ((data << 1) & 0xFF) | c_flag
            self.F = high_bit * flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x08:
            # RRC B
            low_bit = (self.B & 1)
            self.B = (self.B >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x09:
            # RRC C
            low_bit = (self.C & 1)
            self.C = (self.C >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0A:
            # RRC D
            low_bit = (self.D & 1)
            self.D = (self.D >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0B:
            # RRC E
            low_bit = (self.E & 1)
            self.E = (self.E >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0C:
            # RRC H
            low_bit = (self.H & 1)
            self.H = (self.H >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0D:
            # RRC L
            low_bit = (self.L & 1)
            self.L = (self.L >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x0E:
            # RRC (HL)
            data = self.ram.read((self.H << 8) | self.L)
            low_bit = (data & 1)
            data = (data >> 1) | (low_bit << 7)
            self.F = low_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x1F:
            # RR A
            low_bit = self.A & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.A = (self.A >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x18:
            # RR B
            low_bit = self.B & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.B = (self.B >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x19:
            # RR C
            low_bit = self.C & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.C = (self.C >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x1A:
            # RR D
            low_bit = self.D & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.D = (self.D >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x1B:
            # RR E
            low_bit = self.E & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.E = (self.E >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x1C:
            # RR H
            low_bit = self.H & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.H = (self.H >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x1D:
            # RR L
            low_bit = self.L & 1
            c_flag = (self.F & Flags.C) / Flags.C
            self.L = (self.L >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x1E:
            # RR (HL)
            data = self.ram.read((self.H << 8) | self.L)
            low_bit = data & 1
            c_flag = (self.F & Flags.C) / Flags.C
            data = (data >> 1) | (c_flag << 7)
            self.F = low_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x27:
            # SLA A
            high_bit = (self.A & 0x80) >> 7
            self.A = (self.A << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x20:
            # SLA B
            high_bit = (self.B & 0x80) >> 7
            self.B = (self.B << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x21:
            # SLA C
            high_bit = (self.C & 0x80) >> 7
            self.C = (self.C << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x22:
            # SLA D
            high_bit = (self.D & 0x80) >> 7
            self.D = (self.D << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x23:
            # SLA E
            high_bit = (self.E & 0x80) >> 7
            self.E = (self.E << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x24:
            # SLA H
            high_bit = (self.H & 0x80) >> 7
            self.H = (self.H << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x25:
            # SLA L
            high_bit = (self.L & 0x80) >> 7
            self.L = (self.L << 1) & 0xFF
            self.F = high_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x26:
            # SLA (HL)
            data = self.ram.read((self.H << 8) | self.L)
            high_bit = (data & 0x80) >> 7
            data = (data << 1) & 0xFF
            self.F = high_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x2F:
            # SRA A
            low_bit = self.A & 1
            self.A = (self.A & 0x80) | (self.A >> 1)
            self.F = low_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x28:
            # SRA B
            low_bit = self.B & 1
            self.B = (self.B & 0x80) | (self.B >> 1)
            self.F = low_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x29:
            # SRA C
            low_bit = self.C & 1
            self.C = (self.C & 0x80) | (self.C >> 1)
            self.F = low_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x2A:
            # SRA D
            low_bit = self.D & 1
            self.D = (self.D & 0x80) | (self.D >> 1)
            self.F = low_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x2B:
            # SRA E
            low_bit = self.E & 1
            self.E = (self.E & 0x80) | (self.E >> 1)
            self.F = low_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x2C:
            # SRA H
            low_bit = self.H & 1
            self.H = (self.H & 0x80) | (self.H >> 1)
            self.F = low_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x2D:
            # SRA L
            low_bit = self.L & 1
            self.L = (self.L & 0x80) | (self.L >> 1)
            self.F = low_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x2E:
            # SRA (HL)
            data = self.ram.read((self.H << 8) | self.L)
            low_bit = data & 1
            self.L = (data & 0x80) | (data >> 1)
            self.F = low_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x3F:
            # SRL A
            low_bit = self.A & 1
            self.A = self.A >> 1
            self.F = low_bit * Flags.C
            if self.A == 0:
                self.F |= Flags.Z
        elif reg_id == 0x38:
            # SRL B
            low_bit = self.B & 1
            self.B = self.B >> 1
            self.F = low_bit * Flags.C
            if self.B == 0:
                self.F |= Flags.Z
        elif reg_id == 0x39:
            # SRL C
            low_bit = self.C & 1
            self.C = self.C >> 1
            self.F = low_bit * Flags.C
            if self.C == 0:
                self.F |= Flags.Z
        elif reg_id == 0x3A:
            # SRL D
            low_bit = self.D & 1
            self.D = self.D >> 1
            self.F = low_bit * Flags.C
            if self.D == 0:
                self.F |= Flags.Z
        elif reg_id == 0x3B:
            # SRL E
            low_bit = self.E & 1
            self.E = self.E >> 1
            self.F = low_bit * Flags.C
            if self.E == 0:
                self.F |= Flags.Z
        elif reg_id == 0x3C:
            # SRL H
            low_bit = self.H & 1
            self.H = self.H >> 1
            self.F = low_bit * Flags.C
            if self.H == 0:
                self.F |= Flags.Z
        elif reg_id == 0x3D:
            # SRL L
            low_bit = self.L & 1
            self.L = self.L >> 1
            self.F = low_bit * Flags.C
            if self.L == 0:
                self.F |= Flags.Z
        elif reg_id == 0x3E:
            # SRL (HL)
            data = self.ram.read((self.H << 8) | self.L)
            low_bit = data & 1
            data = data >> 1
            self.F = low_bit * Flags.C
            if data == 0:
                self.F |= Flags.Z
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x47:
            # BIT b, A - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.A & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x40:
            # BIT b, B - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.B & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x41:
            # BIT b, C - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.C & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x42:
            # BIT b, D - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.D & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x43:
            # BIT b, E - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.E & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x44:
            # BIT b, H - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.H & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x45:
            # BIT b, L - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            if (self.L & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0x46:
            # BIT b, (HL) - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.F &= Flags.C
            self.F |= Flags.H
            data = self.ram.read((self.H << 8) | self.L)
            if (data & (1 << bit)) == 0:
                self.F |= Flags.Z
        elif reg_id == 0xC7:
            # SET b, A - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.A |= (1 << bit)
        elif reg_id == 0xC0:
            # SET b, B - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.B |= (1 << bit)
        elif reg_id == 0xC1:
            # SET b, C - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.C |= (1 << bit)
        elif reg_id == 0xC2:
            # SET b, D - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.D |= (1 << bit)
        elif reg_id == 0xC3:
            # SET b, E - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.E |= (1 << bit)
        elif reg_id == 0xC4:
            # SET b, H - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.H |= (1 << bit)
        elif reg_id == 0xC5:
            # SET b, L - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.L |= (1 << bit)
        elif reg_id == 0xC6:
            # SET b, (HL) - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            data = self.ram.read((self.H << 8) | self.L)
            data |= (1 << bit)
            self.ram.write((self.H << 8) | self.L, data)
        elif reg_id == 0x87:
            # RES b, A - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.A &= ~(1 << bit)
        elif reg_id == 0x80:
            # RES b, B - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.B &= ~(1 << bit)
        elif reg_id == 0x81:
            # RES b, C - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.C &= ~(1 << bit)
        elif reg_id == 0x82:
            # RES b, D - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.D &= ~(1 << bit)
        elif reg_id == 0x83:
            # RES b, E - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.E &= ~(1 << bit)
        elif reg_id == 0x84:
            # RES b, H - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.H &= ~(1 << bit)
        elif reg_id == 0x85:
            # RES b, L - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            self.L &= ~(1 << bit)
        elif reg_id == 0x86:
            # RES b, (HL) - This op takes an additional byte
            bit = self.ram.read(self.PC)
            self.PC += 1
            data = self.ram.read((self.H << 8) | self.L)
            data &= ~(1 << bit)
            self.ram.write((self.H << 8) | self.L, data)

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
        if (self.A & 7) >= (data & 7):
            self.F |= Flags.H
        if self.A >= data:
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

    def op_DC(self, adr):
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
        if (self.A & 0xF) >= (data + 0xF) + c_flag:
            self.F |= Flags.H
        if self.A >= data + c_flag:
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
        # Fix sign
        if data > 0x7F:
            data = data - 0x100
        self.F = 0
        # TODO - May be wrong
        if (self.SP & 0xF) + (data & 0xF) > 0xF:
            self.F |= Flags.H
        if (self.SP & 0xFF) + data > 0xFF:
            self.F |= Flags.C
        self.SP = (self.SP + data) & 0xFFFF

    def op_E9(self):
        # JP (HL)
        addr = self.ram.read((self.H << 8) | self.L)
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
        self.F = self.ram.read(self.SP)
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
        self.A = self.A | self.L
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
        if (self.SP & 0xF) + (args[0] & 0xF) > 0xF:
            self.F |= Flags.H
        if (self.SP & 0xFF) + (args[0] & 0xFF) > 0xFF:
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
        if (self.A & 0xF) >= (data & 0xF):
            self.F |= Flags.H
        if self.A >= data:
            self.F |= Flags.C

    def op_FF(self):
        # RST 0x38
        self.SP = (self.SP - 2) & 0xFFFF
        self.ram.write(self.SP, self.PC & 0xFF)
        self.ram.write(self.SP+1, self.PC >> 8)
        self.PC = 0x38

class gb_ram(object):
    def __init__(self):
        self.rom = [] # Cartridge ROM
        self.vram = [0x00] * 0x2000 # Video RAM
        self.eram = [0x00] * 0x2000 # External RAM
        self.iram = [0x00] * 0x2000 # Internal RAM
        self.sprite_info = [0x00] * 0xA0
        self.zram = [0x00] * 0x80 # Zero-page RAM

    def load_rom(self, fname):
        rom_string = open(fname).read()
        self.rom = [ord(c) for c in rom_string]

    def read(self, p):
        if p >= 0xFF80:
            # Zero page RAM
            return self.zram[p - 0xFF80]
        elif p >= 0xFF00:
            # TODO -- Memory mapped I/O
            return 0
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
            return self.eram[p - 0xA000]
        elif p >= 0x8000:
            # Graphics RAM
            return self.vram[p - 0x8000]
        elif p >= 0x4000:
            # ROM, switchable bank
            # TODO - switching
            # For now, just return as if it's bank 1
            return self.rom[p]
        else:
            # ROM bank 0
            return self.rom[p]

    def write(self, p, d):
        d = d & 0xFF
        if p >= 0xFF80:
            # Zero page RAM
            self.zram[p - 0xFF80] = d
        elif p >= 0xFF00:
            # TODO -- Memory mapped I/O
            return
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
            self.eram[p - 0xA000] = d
        elif p >= 0x8000:
            # Graphics RAM
            self.vram[p - 0x8000] = d
        elif p >= 0x4000:
            # ROM, switchable bank
            # TODO - switching
            # For now, just return as if it's bank 1
            self.rom[p] = d
        else:
            # ROM bank 0
            self.rom[p] = d
