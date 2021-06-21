import struct, array, sys, time, random
from display import Display
from graphics_init import FONT, KEY_MAP
import pygame


EXE_DELAY = 1  # MS
TIMER_DELAY = 17  # 60 Hz update freq
TIMER = pygame.USEREVENT + 1


filepath = "./games/PONG"
soundpath = "square.wav"


class CPU:
    def __init__(self, program):
        self.registers = [0] * 16  # 8 bits each
        self.instruction_pointer = 0  # 16 bits
        self.program_counter = 0x200  # 16 bits
        self.memory = bytearray(4096)  # 4k memory
        self.delay_timer = 0
        self.sound_timer = 0
        self.stack = list()
        self.display = Display()
        self.initialize_memory(program)
        pygame.mixer.init(buffer=1)
        self.sound = pygame.mixer.Sound(file=soundpath)


    def initialize_memory(self, program):
        program_offset = 0x200
        for i in range(len(program)):
            self.memory[program_offset + i] = program[i]
        self.memory[0x0050:0x00A0] = FONT



    def emulate(self):
        counter = 0
        running = True

        pygame.time.set_timer(TIMER, TIMER_DELAY)

        while running:
            pygame.time.wait(EXE_DELAY)
            self.emulate_cycle()
            counter += 1

            for event in pygame.event.get():
                if event.type == pygame.quit():
                    running = False

                if event.type == TIMER:
                    self.decrement_timers()



                if (self.sound_timer > 0):
                    if not pygame.mixer.get_busy():
                        self.sound.play(loops=-1)

                else:
                    self.sound.stop()



        pygame.display.quit()
        pygame.quit()
        print(counter)




    def emulate_cycle(self):
        opcode_byte1 = self.memory[self.program_counter]
        opcode_byte2 = self.memory[self.program_counter + 1]
        opcode = (opcode_byte1 << 8) | opcode_byte2
        top = opcode >> 12


        address = opcode & 0x0fff
        regx = (opcode & 0x0f00) >> 8
        regy = (opcode & 0x00f0) >> 4
        byte = opcode & 0x00ff
        nibble = opcode & 0x000f

        if top == 0:
            if address == 0x0e0:
                self.display.clear_screen()
                self.program_counter += 2

            elif address == 0x0ee:
                if self.stack:
                    self.program_counter = self.stack.pop()

                else:
                    print("Invalid return")
                    exit(1)

            else:
                print("Not running RCA 1802 program; skipping")
                self.program_counter += 2












