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
list_20 = []
list_A = []
i = 0
c_b = 0
for c_r in range(255):
    for c_g in range(255):
        c_b = 0
        # for c_b in range(255):
        while c_b <= 255:
            i_2=0
            list_20 = ""
            temp = ""
            while i_2 <= 40:

                temp +=  '\x1b[48;2;' + str(c_r) + ';' + str(c_g) + ';' + str(c_b) + 'm' + '●' + '\x1b[0m'
                # list_20.append(temp)
                i_2 += 1
            print('\x1b[1;1H'+temp)
            c_b += 80
            i += 1

print(i)
# print(i)
time.sleep(22222)
num = 0
coler_num = 0
st_Bar = ""
bar_num = 0
view_range = 255
view_num = 0
view_barlist = list(range(view_range))
view_st = ""
while 1:
    view_st = '\x1b[1;1H'
    for n in range(view_range):

        view_st += list_A[coler_num]

        coler_num += 1
        if coler_num == len(list_A):
            coler_num = 0
    print(view_st)
    print(coler_num)
