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

view_range = 300
st_barlist = list(range(view_range))

for n in range(len(st_barlist)):
    st_barlist[n] = "000m "

st_Bar = ""
bar_num = 0
view_num = 0


class Character_info:
    def __init__(self):
        self.name1 = 'aaaa'
        self.name2 = 'bbbb'


info_1 = Character_info()
info_2 = Character_info()

c_info = [Character_info(), Character_info()]

c_info[0].name1 = "1234"
c_info[0].name2 = "5678"

c_info[1].name1 = "55555"
c_info[1].name2 = "1234"
aaa = ""
aaa = copy.deepcopy(c_info[0])
bbb = ""
bbb = c_info[0]

c_info[0].name1 = "hhhh"
c_info[0].name2 = "5678"
bbb.name1 = "fdgdfgdfg"

ssssssssss = create_string_buffer(20)
ssssssssss.raw = b'\x01'

print('c_info[0] ' + c_info[0].name1)
print('c_info[0] ' + c_info[0].name2)
print('c_info[1] ' + c_info[1].name1)
print('c_info[1] ' + c_info[1].name2)
print('c_info1 ' + info_1.name1)
print('c_info1 ' + info_1.name2)
print('aaa ' + aaa.name1)
print('aaa ' + aaa.name2)
print('bbb ' + bbb.name1)
print('bbb ' + bbb.name2)


# print (ssssssssss.raw)
# print (len(ssssssssss.raw))
# print (len(ssssssssss))

#
while 1:
    #
    #     content = "\x1b[48;5;" + str(bar_num) + "m" + str(bar_num).rjust(3, "0") + "a " + "\x1b[0m"
    #
    #     st_barlist[view_num] = content
    #
    #     st_Bar = ""
    #     num_c = view_num
    #
    #     for i in range(view_range):
    #         num_c += 1
    #         if num_c == view_range:
    #             num_c = 0
    #
    #         st_Bar += st_barlist[num_c]
    #
    #
    #     print('\x1b[1;1H' + st_Bar)
    #     print('view_num' + str(view_num))
    #     print('bar_num' + str(bar_num))
    #     print('num_c' + str(num_c))
    #
    #     view_num += 1
    #     if view_num == view_range:
    #         view_num = 0
    #
    #     bar_num = bar_num + 1
    #     if bar_num == 255:
    #         bar_num = 0
    #
    time.sleep(0.005)

#
#     if (num + 1) % 20 == 0:
#         a += '\x1b[K' + '\n'
# a += '\n'
