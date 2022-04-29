from ctypes import windll, wintypes, byref
from struct import unpack
from struct import unpack, pack
import ad_ml
import cfg_ml
import copy
import ctypes
import keyboard
import os
import psutil
import save_ml
ad = ad_ml
cfg = cfg_ml
save = save_ml

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


def get_base_addres():
    cfg_ml.pid = 0
    while cfg_ml.pid == 0:

        dict_pids = {
            p.info["name"]: p.info["pid"]
            for p in psutil.process_iter(attrs=["name", "pid"])
        }

        for n in dict_pids:
            if n == "MBTL.exe":
                cfg_ml.pid = dict_pids["MBTL.exe"]

        if cfg_ml.pid == 0:
            os.system('cls')
            print("Waiting for MBTL to start")

    cfg_ml.h_pro = OpenProcess(0x1F0FFF, False, cfg_ml.pid)

    # MODULEENTRY32を取得
    snapshot = CreateToolhelp32Snapshot(0x00000008, cfg_ml.pid)

    lpme = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)

    res = Module32First(snapshot, byref(lpme))

    while cfg_ml.pid != lpme.th32ProcessID:
        res = Module32Next(snapshot, byref(lpme))

    b_baseAddr = create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr

    cfg.base_ad = unpack('q', b_baseAddr.raw)[0]


def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def w_mem(ad, b_obj):
    WriteMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


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


def pidget():
    # 実行中のすべてのＩＤ＋プロセス名取得
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }

    cfg.pid = dict_pids["MBTL.exe"]
    cfg.h_pro = OpenProcess(0x1F0FFF, False, cfg.pid)


def pause():

    # 一時停止
    w_mem(ad.STOP_AD, b'\x01')


def play():

    # 再生
    w_mem(ad.STOP_AD, b'\x00')


def tagCharacterCheck():
    if cfg.P1.b_tag_flag.raw == b'\x00':
        cfg.p1 = cfg.P1
        cfg.p3 = cfg.P3
        cfg.p_info[0] = cfg.P1
        cfg.p_info[2] = cfg.P3

    elif cfg.P1.b_tag_flag.raw == b'\x01':
        cfg.p1 = cfg.P3
        cfg.p3 = cfg.P1
        cfg.p_info[0] = cfg.P3
        cfg.p_info[2] = cfg.P1

    if cfg.P2.b_tag_flag.raw == b'\x00':
        cfg.p2 = cfg.P2
        cfg.p4 = cfg.P4
        cfg.p_info[1] = cfg.P2
        cfg.p_info[3] = cfg.P4

    elif cfg.P2.b_tag_flag.raw == b'\x01':
        cfg.p2 = cfg.P4
        cfg.p4 = cfg.P2
        cfg.p_info[3] = cfg.P4
        cfg.p_info[1] = cfg.P2


def situationCheck():
    for n in cfg.P_info:
        r_mem(n.anten_stop_ad, n.b_anten_stop)
        r_mem(n.anten_stop2_ad, n.b_anten_stop2)
        r_mem(n.atk_ad, n.b_atk)
        r_mem(n.gauge_ad, n.b_gauge)
        r_mem(n.hit_ad, n.b_hit)
        r_mem(n.hitstop_ad, n.b_hitstop)
        r_mem(n.inv_ad, n.b_inv)
        r_mem(n.moon_ad, n.b_moon)
        r_mem(n.moon_st_ad, n.b_moon_st)
        r_mem(n.motion_ad, n.b_motion)
        r_mem(n.motion_type_ad, n.b_motion_type)
        r_mem(n.noguard_ad, n.b_noguard)
        r_mem(n.seeld_ad, n.b_seeld)
        r_mem(n.step_inv_ad, n.b_step_inv)
        r_mem(n.tag_flag_ad, n.b_tag_flag)
        r_mem(n.ukemi1_ad, n.b_ukemi1)
        r_mem(n.ukemi2_ad, n.b_ukemi2)
        r_mem(n.x_ad, n.b_x)

    r_mem(ad.TIMER_AD, cfg.b_timer)
    r_mem(ad.HOSEI_AD, cfg.b_hosei)
    r_mem(ad.DAMAGE_AD, cfg.b_damage)
    r_mem(ad.START_POSI_AD, cfg.b_start_posi)
    r_mem(ad.UKEMI_AD, cfg.b_ukemi)
    r_mem(ad.ANTEN_AD, cfg.b_anten)


def situationMem():
    # 状況を記憶
    r_mem(ad.CAM_AD, save.b_cam)
    save.P_info = copy.deepcopy(cfg.P_info)


def situationWrit():
    # 状況を再現
    w_mem(ad.CAM_AD, save.b_cam)

    for n in save.P_info:
        w_mem(n.gauge_ad, n.b_gauge)
        w_mem(n.moon_ad, n.b_moon)
        w_mem(n.moon_st_ad, n.b_moon_st)
        w_mem(n.x_ad, n.b_x)


def moon_change():

    if cfg.P_info[0].b_moon_st.raw == b'\x00':
        for n in cfg.P_info:
            w_mem(n.moon_st_ad, b'\x01')

    elif cfg.P_info[0].b_moon_st.raw == b'\x01':
        for n in cfg.P_info:
            w_mem(n.moon_st_ad, b'\00')

    for n in cfg.P_info:
        w_mem(n.moon_ad, b'\x10\x27')


def MAX_Damage_ini():

    r_mem(ad.MAX_Damage_Pointer_AD, cfg.temp)

    addres = unpack('l', cfg.temp.raw)[0]
    addres = addres + 0x1c
    w_mem(addres, b'\x00\x00\x00\x00')
    w_mem(addres + 4, b'\x00\x00\x00\x00')


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (
        cfg.p1.motion_type != 0 or
        cfg.p2.motion_type != 0 or
        cfg.p1.hitstop != 0 or
        cfg.p2.hitstop != 0 or
        cfg.p1.hit != 0 or
        cfg.p2.hit != 0
    ):
        cfg.reset_flag = 0
        cfg.Bar_flag = 1
        cfg.interval = 0
    else:
        cfg.Bar_flag = 0
        cfg.interval += 1

    # バーリセット判定
    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.reset_flag == 0:
        if cfg.Bar80_flag == 0:
            cfg.Bar_flag = 1

    # ヒットストップ処理
    if (cfg.p1.hitstop != 0 and cfg.p2.hitstop != 0):
        cfg.hitstop += 1
    elif (cfg.p1.hitstop == 0 or cfg.p2.hitstop == 0):
        cfg.hitstop = 0

    if cfg.anten_flag == 16 and cfg.p1.anten_stop2 == cfg.p1.anten_stop2_old:
        cfg.anten += 1
    else:
        cfg.anten = 0

    if cfg.anten_flag == 16 and cfg.p2.anten_stop2 == cfg.p2.anten_stop2_old:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # バー追加処理
    if cfg.Bar_flag == 1:
        bar_add()


def advantage_calc():
    if cfg.p1.hit == 0 and cfg.p2.hit == 0 and cfg.p1.motion_type == 0 and cfg.p2.motion_type == 0:
        cfg.DataFlag1 = 0

    if (cfg.p1.hit != 0 or cfg.p1.motion_type != 0) and (cfg.p2.hit != 0 or cfg.p2.motion_type != 0):
        cfg.DataFlag1 = 1
        cfg.yuuriF = 0

    if cfg.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg.p1.hit == 0 and cfg.p1.motion_type == 0) and (cfg.p2.hit != 0 or cfg.p2.motion_type != 0):
            cfg.yuuriF += 1

        # 不利フレーム検証
        if (cfg.p1.hit != 0 or cfg.p1.motion_type != 0) and (cfg.p2.hit == 0 and cfg.p2.motion_type == 0):
            cfg.yuuriF -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg.p1.motion != 0:
        cfg.p1.zen = cfg.p1.motion

    if cfg.p2.motion != 0:
        cfg.p2.zen = cfg.p2.motion


def bar_add():

    DEF = '\x1b[0m'

    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    atk = "\x1b[38;5;255m" + "\x1b[48;5;160m"
    mot = "\x1b[38;5;255m" + "\x1b[48;5;010m"
    grd = '\x1b[0m' + "\x1b[48;5;250m"
    nog = "\x1b[38;5;250m" + "\x1b[48;5;000m"
    fre = "\x1b[38;5;234m" + "\x1b[48;5;000m"
    non = "\x1b[38;5;148m" + "\x1b[48;5;201m"

    if cfg.anten == 0 and cfg.hitstop == 0:
        cfg.Bar_num += 1
        if cfg.Bar_num == cfg.bar_range:
            cfg.Bar_num = 0
            cfg.Bar80_flag = 1

    for n in cfg.p_info:
        num = ""
        fb = ""
        font = DEF

        if n.b_atk.raw != b'\x00':  # 攻撃判定を出しているとき
            fb = atk

        elif (n.inv == 0 and n.motion != 0) or (n.b_step_inv.raw != b'\x00' and n.motion_type == 46):  # 無敵中
            fb = "\x1b[48;5;015m"

        elif n.motion != 0:  # モーション途中
            fb = mot

        elif n.hit != 0:  # ガードorヒット硬直中
            fb = grd

        elif n.motion_type != 0:  # ガードできないとき
            fb = nog

        elif n.motion == 0:  # 何もしていないとき
            fb = fre

        else:  # いずれにも当てはまらないとき
            fb = non

        # ジャンプ移行中
        if n.motion_type == 34 or n.motion_type == 35 or n.motion_type == 36 or n.motion_type == 37:
            fb = "\x1b[38;5;000m" + "\x1b[48;5;011m"

        # シールド中
        if n.b_seeld.raw == b'\x02':
            fb = "\x1b[38;5;255m" + "\x1b[48;5;006m"
        if n.b_seeld.raw == b'\x03':
            fb = "\x1b[38;5;255m" + "\x1b[48;5;004m"

        # 起き上がり中
        if n.motion_type == 593:
            fb = "\x1b[38;5;255m" + "\x1b[48;5;055m"
        font += fb

        if n.motion != 0:
            num = str(n.motion)
        else:
            num = str(n.motion_type)

        if n.hit != 0:
            num = str(n.hit)

        if num == '0' and cfg.DataFlag1 == 1:
            if n == cfg.p_info[0] or n == cfg.p_info[1]:
                font = DEF + "\x1b[38;5;244m" + "\x1b[48;5;000m"
                num = str(abs(cfg.yuuriF))

        n.barlist_1[cfg.Bar_num] = font + num.rjust(2, " ")[-2:]


def bar_ini():
    cfg.reset_flag = 1
    cfg.p1.Bar_1 = ""
    cfg.p2.Bar_1 = ""
    cfg.p3.Bar_1 = ""
    cfg.p4.Bar_1 = ""
    cfg.st_Bar = ""
    cfg.Bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.Bar80_flag = 0
    cfg.interval_time = 80

    for n in range(cfg.bar_range):
        cfg.p1.barlist_1[n] = ""
        cfg.p2.barlist_1[n] = ""
        cfg.p3.barlist_1[n] = ""
        cfg.p4.barlist_1[n] = ""
        cfg.st_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg.p2.hitstop != 0 and cfg.p1.act_flag == 0 and cfg.p1.hit == 0:
        cfg.p1.act = cfg.p1.zen
        cfg.p1.act_flag = 1

    if cfg.p1.hitstop != 0 and cfg.p2.act_flag == 0 and cfg.p2.hit == 0:
        cfg.p2.act = cfg.p2.zen
        cfg.p2.act_flag = 1

    if cfg.p1.motion == 0 and cfg.p1.atk == 0:
        cfg.p1.act_flag = 0

    if cfg.p2.motion == 0 and cfg.p2.atk == 0:
        cfg.p2.act_flag = 0


def get_values():
    for n in cfg.P_info:
        n.x = unpack('l', n.b_x.raw)[0]
        if n.motion_type != 0:
            n.motion_type_old = n.motion_type
        n.motion_type = unpack('h', n.b_motion_type.raw)[0]

        n.motion = 256 - unpack('l', n.b_motion.raw)[0]
        n.atk = unpack('b', n.b_atk.raw)[0]
        n.inv = unpack('b', n.b_inv.raw)[0]

        n.hitstop_old = n.hitstop
        n.hitstop = unpack('b', n.b_hitstop.raw)[0]
        n.hit = unpack('h', n.b_hit.raw)[0]
        n.noguard = unpack('b', n.b_noguard.raw)[0]
        n.anten_stop = unpack('B', n.b_anten_stop.raw)[0]
        n.anten_stop2_old = n.anten_stop2
        n.anten_stop2 = unpack('l', n.b_anten_stop2.raw)[0]

        n.gauge = unpack('l', n.b_gauge.raw)[0]
        n.moon = unpack('l', n.b_moon.raw)[0]
        n.ukemi1 = unpack('h', n.b_ukemi1.raw)[0]
        n.ukemi2 = unpack('h', n.b_ukemi2.raw)[0]

    cfg.damage = unpack('l', cfg.b_damage.raw)[0]
    cfg.hosei = unpack('l', cfg.b_hosei.raw)[0]
    cfg.ukemi = unpack('h', cfg.b_ukemi.raw)[0]
    cfg.anten_flag = unpack('B', cfg.b_anten.raw)[0]

    tagCharacterCheck()
    # 初回77だけ無視してmotion_typeを表示
    for n in cfg.p_info:
        if n.motion_type_old == n.motion_type:
            n.motion_chenge_flag += 1
        else:
            n.motion_chenge_flag = 0

    for n in cfg.p_info:
        if n.hitstop == 65536:
            n.hitstop = 0

        if n.motion == 256:
            n.motion = 0
        if n.noguard == 77:
            negligible_number = [21, 81, 80, 149,
                                 98, 171, 44,
                                 40, 10, 11, 12,
                                 13, 14, 15, 18,
                                 20, 16, 594, 17,
                                 38, 39, 19, 201,
                                 200]

            for m in negligible_number:

                if n.motion > 1:
                    n.motion = 0

                if n.motion_type == m:
                    n.motion = 0
                    n.motion_type = 0
                    break

            if n.motion_chenge_flag != 0:
                negligible_number = [147]
                for m in negligible_number:
                    if n.motion_type == m:
                        n.motion = 0
                        n.motion_type = 0
                        break


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg.p1.x).rjust(8, " ")
    x_p2 = str(cfg.p2.x).rjust(8, " ")
    act_P1 = str(cfg.p1.act).rjust(3, " ")
    act_P2 = str(cfg.p2.act).rjust(3, " ")
    zen_P1 = str(cfg.p1.zen).rjust(3, " ")
    zen_P2 = str(cfg.p2.zen).rjust(3, " ")
    gauge_p1 = str('{:.02f}'.format(cfg.p1.gauge / 100)).rjust(7, " ")
    gauge_p2 = str('{:.02f}'.format(cfg.p2.gauge / 100)).rjust(7, " ")
    m_gauge_p1 = str('{:.02f}'.format(cfg.p1.moon / 100)).rjust(7, " ")
    m_gauge_p2 = str('{:.02f}'.format(cfg.p2.moon / 100)).rjust(7, " ")

    ukemi = str(cfg.ukemi).rjust(3, " ")

    if cfg.p2.ukemi2 != 0:
        ukemi2 = str(cfg.p2.ukemi2 + 1).rjust(3, " ")
        cfg.ukemi2 = cfg.p2.ukemi2

    else:
        ukemi2 = str(cfg.ukemi2 + 1).rjust(3, " ")

    yuuriF = str(cfg.yuuriF).rjust(7, " ")

    hosei = str(cfg.hosei).rjust(4, " ")

    kyori = cfg.p1.x - cfg.p2.x

    # damage = cfg.damage
    # kouritu = "0".rjust(8, " ")
    # # if damage != 0:
    # #     kouritu = damage / (100 - cfg.hosei)
    # #     kouritu = str('{:.02f}'.format(kouritu)).rjust(8, " ")

    cfg.p1.Bar_1 = ""
    cfg.p2.Bar_1 = ""
    cfg.p3.Bar_1 = ""
    cfg.p4.Bar_1 = ""

    cfg.st_Bar = ""

    temp = cfg.Bar_num

    for n in range(cfg.bar_range):
        temp += 1
        if temp == cfg.bar_range:
            temp = 0
        cfg.p1.Bar_1 += cfg.p1.barlist_1[temp]
        cfg.p2.Bar_1 += cfg.p2.barlist_1[temp]
        cfg.p3.Bar_1 += cfg.p3.barlist_1[temp]
        cfg.p4.Bar_1 += cfg.p4.barlist_1[temp]

        cfg.st_Bar += cfg.st_barlist[temp]

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += '1P|Position' + x_p1
    state_str += ' FirstActive' + act_P1
    state_str += ' Overall' + zen_P1
    state_str += ' Circuit' + gauge_p1 + '%'

    state_str += ' Moon' + m_gauge_p1 + '%'

    if keyboard.is_pressed("F1"):
        f1 = '  \x1b[007m' + '[F1]Reset' + '\x1b[0m'
    else:
        f1 = '  [F1]Reset'

    if keyboard.is_pressed("F2"):
        f2 = '  \x1b[007m' + '[F2]Save' + '\x1b[0m'
    else:
        f2 = '  [F2]Save'

    if keyboard.is_pressed("F3"):
        f3 = '  \x1b[007m' + '[F3]Moon switch' + '\x1b[0m'
    else:
        f3 = '  [F3]Moon switch'

    if keyboard.is_pressed("F4"):
        f4 = '  \x1b[007m' + '[F4]Max damage ini' + '\x1b[0m'
    else:
        f4 = '  [F4]Max damage ini'

    state_str += '   ' + f1 + f2 + f3 + f4 + END

    state_str += '2P|Position' + x_p2
    state_str += ' FirstActive' + act_P2
    state_str += ' Overall' + zen_P2
    state_str += ' Circuit' + gauge_p2 + '%'
    state_str += ' Moon' + m_gauge_p2 + '%' + END

    state_str += '  |Advantage' + yuuriF
    state_str += ' Proration' + hosei + "%"
    state_str += ' Untec' + ukemi2 + ',' + ukemi
    state_str += '  Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.p1.Bar_1 + END
    state_str += '2P|' + cfg.p2.Bar_1 + END
    # state_str += '3P|' + cfg.p3.Bar_1 + END
    # state_str += '4P|' + cfg.p4.Bar_1 + END判断
    print(state_str)
    degug_view()


def degug_view():
    if cfg.debug_flag == 1:
        debug_str_p1 = "f_timer " + str(cfg.f_timer).rjust(7, " ")
        debug_str_p2 = "Bar_num " + str(cfg.Bar_num).rjust(7, " ")

        debug_str_p1 += "motion_type " + str(cfg.p1.motion_type).rjust(7, " ")
        debug_str_p2 += "motion_type " + str(cfg.p2.motion_type).rjust(7, " ")
        debug_str_p1 += " motion " + str(cfg.p1.motion).rjust(7, " ")
        debug_str_p2 += " motion " + str(cfg.p2.motion).rjust(7, " ")
        debug_str_p1 += " anten_stop " + str(cfg.p1.anten_stop).rjust(7, " ")
        debug_str_p2 += " anten_stop " + str(cfg.p2.anten_stop).rjust(7, " ")
        debug_str_p1 += " motion_chenge_flag " + str(cfg.p1.motion_chenge_flag).rjust(7, " ")
        debug_str_p2 += " motion_chenge_flag " + str(cfg.p2.motion_chenge_flag).rjust(7, " ")
        debug_str_p1 += " hitstop " + str(cfg.p1.hitstop).rjust(7, " ")
        debug_str_p2 += " hitstop " + str(cfg.p2.hitstop).rjust(7, " ")
        debug_str_p1 += " noguard " + str(cfg.p1.noguard).rjust(7, " ")
        debug_str_p2 += " noguard " + str(cfg.p2.noguard).rjust(7, " ")
        debug_str_p1 += " hitstop_old " + str(cfg.p1.hitstop_old).rjust(7, " ")
        debug_str_p2 += " hitstop_old " + str(cfg.p2.hitstop_old).rjust(7, " ")

        debug_str_p1 += " anten " + str(cfg.anten).rjust(7, " ")

        print(debug_str_p1)
        print(debug_str_p2)


def determineReset():
    bar_ini_flag = 0

    if cfg.Bar80_flag == 1:
        cfg.interval_time = 1

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.Bar_flag == 1:
        bar_ini_flag = 1

    cfg.interval2 += 1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()


def timer_check():
    r_mem(ad.TIMER_AD, cfg.b_timer)
    cfg.f_timer = unpack('l', cfg.b_timer.raw)[0]


def tr_flag_check():
    r_mem(ad.TR_FLAG_AD, cfg.b_tr_flag)


def startposi():
    x_p1 = unpack('l', save.P_info[0].b_x.raw)[0]
    x_p2 = unpack('l', save.P_info[1].b_x.raw)[0]

    b_ini_posi_flag = b'\x00'
    if x_p1 < x_p2:
        b_ini_posi_flag = b'\x00'

    if x_p1 > x_p2:
        b_ini_posi_flag = b'\x05'

    if x_p1 == 262144:
        b_ini_posi_flag = b'\x04'

    if x_p1 == -262144:
        b_ini_posi_flag = b'\x03'

    if x_p2 == 262144:
        b_ini_posi_flag = b'\x02'

    if x_p2 == -262144:
        b_ini_posi_flag = b'\x01'

    w_mem(ad.START_POSI_AD, b_ini_posi_flag)
