import os
import time
from ctypes import windll, wintypes, byref, create_string_buffer
import copy
INVALID_HANDLE_VALUE = -1
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
ENABLE_LVB_GRID_WORLDWIDE = 0x0010

hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
dwMode = wintypes.DWORD()
dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
# dwMode.value |= ENABLE_LVB_GRID_WORLDWIDE

os.system('mode con: cols=50 lines=21')
os.system('cls')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする
i=0
while 1:
    time.sleep(0.1)
    i+=1
    if i == 5:
        i=0

    match i:
        case "1":
            print("1111")
        case 2:
            print("2222")
        case 3:
            print("3333")
        case _:
            print("0000")
