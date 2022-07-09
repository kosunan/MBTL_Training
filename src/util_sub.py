from struct import unpack, pack
from ctypes import windll, wintypes, byref
import os
import time
import ctypes
import psutil
import cfg_tl
cfg = cfg_tl

wintypes = ctypes.wintypes
windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory
OpenProcess = windll.kernel32.OpenProcess
Module32Next = windll.kernel32.Module32Next
Module32First = windll.kernel32.Module32First
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CloseHandle = windll.kernel32.CloseHandle
sizeof = ctypes.sizeof


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HMODULE),
        ("szModule",           ctypes.c_byte * 256),
        ("szExePath",          ctypes.c_byte * 260),
    ]


def get_connection(process_name):
    res = False

    while res == False:
        res = pidget(process_name)
        if res == False:
            os.system('cls')
            print("Waiting for " + process_name + " to start")
            time.sleep(0.5)
    pid = res
    h_pro = OpenProcess(0x1F0FFF, False, pid)
    base_ad = get_base_addres(pid)

    return pid, h_pro, base_ad


def pidget(process_name):
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }

    try:
        pid = dict_pids[process_name]
    except:
        pid = False

    return pid


def get_base_addres(pid):

    # MODULEENTRY32を取得
    snapshot = CreateToolhelp32Snapshot(0x00000008, pid)

    lpme = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)

    res = Module32First(snapshot, byref(lpme))

    while pid != lpme.th32ProcessID:
        res = Module32Next(snapshot, byref(lpme))

    b_baseAddr = create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr

    base_ad = unpack('q', b_baseAddr.raw)[0]

    return base_ad


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]


def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def r_mem_2(ad, b_obj):
    ReadMem(cfg.h_pro, ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def w_mem(ad, b_obj):
    WriteMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def para_read(obj):
    obj.num = r_mem(obj.ad, obj.b_dat)


def para_read_2(obj):
    obj.num = r_mem_2(obj.ad, obj.b_dat)


def para_write(obj):
    w_mem(obj.ad, obj.b_dat)


def text_font(rgb):
    Text_font_str = "\x1b[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


G_atk = get_font((255, 255, 255), (255, 0, 0))
G_mot = get_font((255, 255, 255), (65, 200, 0))
G_mot2 = get_font((255, 255, 255), (35, 158, 0))

G_grd_stun = get_font((255, 255, 255), (170, 170, 170))
G_hit_stun = get_font((255, 255, 255), (170, 170, 170))
G_fre = get_font((92, 92, 92), (25, 25, 25))
G_jmp = get_font((177, 177, 177), (241, 224, 132))
G_seeld = get_font((255, 255, 255), (145, 194, 255))
G_inv = get_font((200, 200, 200), (255, 255, 255))
G_adv = get_font((255, 255, 255), (25, 25, 25))
G_bunker = get_font((255, 255, 255), (225, 184, 0))
G_air = get_font((255, 255, 255), (25, 25, 25))
G_hit_stop = get_font((255, 255, 255), (228, 94, 155))


def bar_coloring(flame_status):
    atk_flag = flame_status[0]
    action_flag = flame_status[1]
    inv_flag = flame_status[2]
    grd_stun_flag = flame_status[3]
    hit_stun_flag = flame_status[4]
    jmp_flag = flame_status[5]
    air_flag = flame_status[6]
    seeld_flag = flame_status[7]
    bunker_flag = flame_status[8]
    motion_type = flame_status[9]
    motion_num = flame_status[10]
    advantage_f = flame_status[11]
    active = flame_status[12]

    font_1 = G_fre
    font_2 = G_fre

    if inv_flag == 1:  # 無敵中
        font_1 = G_inv

    elif jmp_flag == 1:  # ジャンプ
        font_1 = G_jmp

    elif seeld_flag == 1:  # シールド中
        font_1 = G_seeld

    elif grd_stun_flag == 1:  # ガード
        font_1 = G_grd_stun

    elif hit_stun_flag == 1:  # ヒット硬直中
        font_1 = G_hit_stun

    elif action_flag == 1:  # モーション途中
        font_1 = G_mot
        if motion_num == 0:
            font_1 = G_mot2

    elif action_flag == 0:  #
        font_1 = G_fre

    if air_flag == 1:  # 空中にいる場合
        font_2 = G_air

    if atk_flag == 1:  # 攻撃判定を出している場合
        font_2 = G_atk
        if air_flag == 1:  # 空中にいる場合
            font_2 += "\x1b[4m"

    num_1 = ""
    num_2 = ""

    num_1 = str(motion_num)
    if num_1 == "0":
        num_1 = str(motion_type)

    if action_flag == 0:
        num_1 = ""

    if advantage_f != 0 and num_1 == "":
        font_1 = G_adv
        num_1 = str(abs(advantage_f))

    if air_flag == 1:  # 空中にいる場合
        num_2 = "^"

    if atk_flag == 1:
        num_2 = str(active)

    ret_1 = font_1 + num_1.rjust(2, " ")[-2:]
    ret_2 = font_2 + num_2.rjust(2, " ")[-2:]

    return ret_1,  ret_2


def ex_cmd_enable():
    INVALID_HANDLE_VALUE = -1
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_LVB_GRID_WORLDWIDE = 0x0010

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hOut == INVALID_HANDLE_VALUE:
        return False
    dwMode = wintypes.DWORD()
    if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
        return False
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    # dwMode.value |= ENABLE_LVB_GRID_WORLDWIDE
    if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
        return False
    return True
