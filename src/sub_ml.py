from ctypes import windll, wintypes, byref
from struct import unpack, pack
import psutil
import cfg_ml
import ad_ml
import save_ml

cfg = cfg_ml
ad = ad_ml
save = save_ml

# import copy
OpenProcess = windll.kernel32.OpenProcess
CloseHandle = windll.kernel32.CloseHandle
ReadMem = windll.kernel32.ReadProcessMemory
WriteMem = windll.kernel32.WriteProcessMemory


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
    WriteMem(cfg.h_pro, ad.STOP_AD, b'\x01', 1, None)


def play():

    # 再生
    WriteMem(cfg.h_pro, ad.STOP_AD, b'\x00', 1, None)


def tagCharacterCheck():
    ReadMem(cfg.h_pro, ad.HI_KO_P1_AD, cfg.b_hi_ko_flag_p1, 1, None)
    ReadMem(cfg.h_pro, ad.HI_KO_P2_AD, cfg.b_hi_ko_flag_p2, 1, None)

    cfg.size_p1 = 0
    if cfg.b_hi_ko_flag_p1.raw == b'\x01':
        cfg.size_p1 = ad.PLR_STRUCT_SIZE * 2

    cfg.size_p2 = 0
    if cfg.b_hi_ko_flag_p2.raw == b'\x01':
        cfg.size_p2 = ad.PLR_STRUCT_SIZE * 2


def situationCheck():
    # タッグキャラ対策
    tagCharacterCheck()

    ReadMem(cfg.h_pro, ad.X_P1_AD + cfg.size_p1, cfg.b_x_p1, 4, None)
    ReadMem(cfg.h_pro, ad.ATK_P1_AD + cfg.size_p1, cfg.b_atk_p1, 4, None)
    ReadMem(cfg.h_pro, ad.HITSTOP_P1_AD + cfg.size_p1, cfg.b_hitstop_p1, 4, None)
    ReadMem(cfg.h_pro, ad.HIT_P1_AD + cfg.size_p1, cfg.b_hit_p1, 2, None)
    ReadMem(cfg.h_pro, ad.NOGUARD_P1_AD + cfg.size_p1, cfg.b_noguard_p1, 1, None)
    ReadMem(cfg.h_pro, ad.MOTION_TYPE_P1_AD + cfg.size_p1, cfg.b_mftp_p1, 2, None)
    ReadMem(cfg.h_pro, ad.MOTION_P1_AD + cfg.size_p1, cfg.b_mf_p1, 4, None)
    ReadMem(cfg.h_pro, ad.GAUGE_P1_AD + cfg.size_p1, cfg.b_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.ANTEN_STOP_AD + cfg.size_p1, cfg.b_anten_stop_p1, 1, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, cfg.b_m_gauge_p1, 4, None)

    ReadMem(cfg.h_pro, ad.X_P2_AD + cfg.size_p2, cfg.b_x_p2, 4, None)
    ReadMem(cfg.h_pro, ad.ATK_P2_AD + cfg.size_p2, cfg.b_atk_p2, 4, None)
    ReadMem(cfg.h_pro, ad.HIT_P2_AD + cfg.size_p2, cfg.b_hit_p2, 2, None)
    ReadMem(cfg.h_pro, ad.HITSTOP_P2_AD + cfg.size_p2, cfg.b_hitstop_p2, 4, None)
    ReadMem(cfg.h_pro, ad.NOGUARD_P2_AD + cfg.size_p2, cfg.b_noguard_p2, 1, None)
    ReadMem(cfg.h_pro, ad.MOTION_TYPE_P2_AD + cfg.size_p2, cfg.b_mftp_p2, 2, None)
    ReadMem(cfg.h_pro, ad.MOTION_P2_AD + cfg.size_p2, cfg.b_mf_p2, 4, None)
    ReadMem(cfg.h_pro, ad.ANTEN2_STOP_AD + cfg.size_p2, cfg.b_anten_stop_p2, 1, None)
    ReadMem(cfg.h_pro, ad.GAUGE_P2_AD + cfg.size_p2, cfg.b_gauge_p2, 4, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, cfg.b_m_gauge_p2, 4, None)

    ReadMem(cfg.h_pro, ad.UKEMI2_P2_AD + cfg.size_p2, cfg.b_ukemi1, 2, None)

    # 状況チェック
    ReadMem(cfg.h_pro, ad.TIMER_AD, cfg.b_timer, 4, None)
    ReadMem(cfg.h_pro, ad.HOSEI_AD, cfg.b_hosei, 4, None)
    ReadMem(cfg.h_pro, ad.UKEMI_AD, cfg.b_ukemi2, 2, None)

    ReadMem(cfg.h_pro, ad.DAMAGE_AD, cfg.b_damage, 4, None)
    ReadMem(cfg.h_pro, ad.START_POSI_AD, cfg.b_start_posi, 1, None)


def situationMem():
    # 状況を記憶
    ReadMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    ReadMem(cfg.h_pro, ad.X_P1_AD, cfg.b_dat_p1, 4, None)
    ReadMem(cfg.h_pro, ad.X_P2_AD, cfg.b_dat_p2, 4, None)
    ReadMem(cfg.h_pro, ad.X_P3_AD, cfg.b_dat_p3, 4, None)
    ReadMem(cfg.h_pro, ad.X_P4_AD, cfg.b_dat_p4, 4, None)


    cfg.size_p1 = cfg.size_p1
    cfg.size_p2 = cfg.size_p2

    ReadMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, save.m_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, save.m_gauge_p2, 4, None)

    ReadMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, cfg.b_m_st_p1, 1, None)
    ReadMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, cfg.b_m_st_p2, 1, None)

    ReadMem(cfg.h_pro, ad.DAT_P1_AD, save.P1_data1, save.data_size, None)
    ReadMem(cfg.h_pro, ad.DAT_P2_AD, save.P2_data1, save.data_size, None)
    ReadMem(cfg.h_pro, ad.SAVE_BASE_AD, save.save_data, save.data_size2, None)


def situationWrit():
    # 状況を再現
    WriteMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    WriteMem(cfg.h_pro, ad.X_P1_AD, cfg.b_dat_p1, 4, None)
    WriteMem(cfg.h_pro, ad.X_P2_AD, cfg.b_dat_p2, 4, None)
    WriteMem(cfg.h_pro, ad.X_P3_AD, cfg.b_dat_p3, 4, None)
    WriteMem(cfg.h_pro, ad.X_P4_AD, cfg.b_dat_p4, 4, None)

    WriteMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, save.m_gauge_p1, 4, None)
    WriteMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, save.m_gauge_p2, 4, None)

    WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, cfg.b_m_st_p1, 1, None)
    WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, cfg.b_m_st_p2, 1, None)

def situationWrit2():
    # 状況を再現
    WriteMem(cfg.h_pro, ad.SAVE_BASE_AD, save.save_data, save.data_size2, None)
    WriteMem(cfg.h_pro, ad.DAT_P1_AD, save.P1_data1, save.data_size, None)
    WriteMem(cfg.h_pro, ad.DAT_P2_AD, save.P2_data1, save.data_size, None)


def moon_change():
    if cfg.moonchange_flag == 0:
        cfg.moonchange_flag = 1
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, b'\x01', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, b'\x01', 1, None)

    elif cfg.moonchange_flag == 1:
        cfg.moonchange_flag = 0
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, b'\x00', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, b'\x00', 1, None)


def MAX_Damage_ini():

    ReadMem(cfg.h_pro, ad.MAX_Damage_Pointer_AD, cfg.temp, 4, None)

    addres = unpack('l', cfg.temp.raw)[0]
    addres = addres + 0x1c
    WriteMem(cfg.h_pro, addres, b'\x00\x00\x00\x00', 4, None)
    WriteMem(cfg.h_pro, addres + 4, b'\x00\x00\x00\x00', 4, None)


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (
        cfg.mftp_p1 != 0 or
        cfg.mftp_p2 != 0 or
        cfg.hitstop_p1 != 0 or
        cfg.hitstop_p2 != 0 or
        cfg.hit_p1 != 0 or
        cfg.hit_p2 != 0
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
        cfg.Bar_flag = 1

    # 暗転判定処理
    if cfg.anten_stop == 128 or cfg.anten2_stop == 128:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # if cfg.reset_flag == 1:
    #     cfg.Bar_flag = 0

    # バー追加処理
    if cfg.Bar_flag == 1:
        if (cfg.hitstop_p1 == 0 or cfg.hitstop_p2 == 0):
            bar_add()


def advantage_calc():

    if cfg.hit_p1 == 0 and cfg.hit_p2 == 0 and cfg.mftp_p1 == 0 and cfg.mftp_p2 == 0:
        cfg.DataFlag1 = 0

    if (cfg.hit_p1 != 0 or cfg.mftp_p1 != 0) and (cfg.hit_p2 != 0 or cfg.mftp_p2 != 0):
        cfg.DataFlag1 = 1
        cfg.yuuriF = 0

    if cfg.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg.hit_p1 == 0 and cfg.mftp_p1 == 0) and (cfg.hit_p2 != 0 or cfg.mftp_p2 != 0):
            cfg.yuuriF += 1

        # 不利フレーム検証
        if (cfg.hit_p1 != 0 or cfg.mftp_p1 != 0) and (cfg.hit_p2 == 0 and cfg.mftp_p2 == 0):
            cfg.yuuriF -= 1

def overall_calc():
    # 全体フレームの取得
    if cfg.mf_p1 != 0:
        cfg.zen_P1 = cfg.mf_p1

    if cfg.mf_p2 != 0:
        cfg.zen_P2 = cfg.mf_p2


def bar_add():

    DEF = '\x1b[0m'

    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    BC_white = "\x1b[40m"
    FC_white = "\x1b[30m"

    WHITE = '\x1b[39m'
    RED = '\x1b[31m'

    atk = "\x1b[41m" + FC_DEF
    mot = "\x1b[107m" + FC_DEF
    grd = "\x1b[48;5;08m" + FC_DEF
    nog = "\x1b[38;5;243m" + BC_DEF
    fre = "\x1b[38;5;234m" + BC_DEF

    p1num = ""
    p2num = ""
    P1_b_c = ""
    P2_b_c = ""
    bc = ""
    fc = ""
    fb = ""
    # 1P
    if cfg.b_atk_p1.raw != b'\x00\x00\x00\x00':  # 攻撃判定を出しているとき
        fb = atk

    elif cfg.mf_p1 != 0:  # モーション途中
        fb = mot

    elif cfg.hit_p1 != 0:  # ガード硬直中
        fb = grd

    elif cfg.mftp_p1 != 0:  # ガードできないとき
        fb = nog

    elif cfg.mf_p1 == 0:  # 何もしていないとき
        fb = fre

    P1_b_c = fb

    # 2P
    if cfg.b_atk_p2.raw != b'\x00\x00\x00\x00':  # 攻撃判定を出しているとき
        fb = atk

    elif cfg.mf_p2 != 0:  # モーション途中
        fb = mot

    elif cfg.hit_p2 != 0:  # ガード硬直中
        fb = grd

    elif cfg.mftp_p2 != 0:  # ガードできないとき
        fb = nog

    elif cfg.mf_p2 == 0:  # 何もしていないとき
        fb = fre

    P2_b_c = fb

    if cfg.mf_p1 != 0:
        p1num = str(cfg.mf_p1)
    else:
        p1num = str(cfg.mftp_p1)

    if cfg.mf_p2 != 0:
        p2num = str(cfg.mf_p2)
    else:
        p2num = str(cfg.mftp_p2)

    if cfg.hit_p1 != 0:
        p1num = str(cfg.hit_p1)

    if cfg.hit_p2 != 0:
        p2num = str(cfg.hit_p2)

    if p1num == '':
        p1num = '0'

    if p2num == '':
        p2num = '0'

    if cfg.anten <= 1:
        cfg.Bar_num += 1
        if cfg.Bar_num == 80:
            cfg.Bar_num = 0

    cfg.p1_barlist[cfg.Bar_num] = P1_b_c + p1num.rjust(2, " ")[-2:]
    cfg.p2_barlist[cfg.Bar_num] = P2_b_c + p2num.rjust(2, " ")[-2:]


def bar_ini():
    cfg.reset_flag = 1
    cfg.P1_Bar = ""
    cfg.P2_Bar = ""
    cfg.Bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0

    cfg.p1_index = 0
    cfg.p2_index = 0

    for n in range(len(cfg.p1_barlist)):
        cfg.p1_barlist[n] = ""

    for n in range(len(cfg.p2_barlist)):
        cfg.p2_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg.hitstop_p2 != 0 and cfg.act_flag_P1 == 0 and cfg.hit_p1 == 0:
        cfg.act_P1 = cfg.zen_P1
        cfg.act_flag_P1 = 1

    if cfg.hitstop_p1 != 0 and cfg.act_flag_P2 == 0 and cfg.hit_p2 == 0:
        cfg.act_P2 = cfg.zen_P2
        cfg.act_flag_P2 = 1

    if cfg.mf_p1 == 0 and cfg.atk_p1 == 0:
        cfg.act_flag_P1 = 0

    if cfg.mf_p2 == 0 and cfg.atk_p2 == 0:
        cfg.act_flag_P2 = 0


def get_values():

    cfg.x_p1 = unpack('l', cfg.b_x_p1.raw)[0]
    cfg.x_p2 = unpack('l', cfg.b_x_p2.raw)[0]
    cfg.mftp_p1 = unpack('h', cfg.b_mftp_p1.raw)[0]
    cfg.mftp_p2 = unpack('h', cfg.b_mftp_p2.raw)[0]
    cfg.mftp_debug_p1 = cfg.mftp_p1
    cfg.mftp_debug_p2 = cfg.mftp_p2
    cfg.mf_p1 = 256 - unpack('l', cfg.b_mf_p1.raw)[0]
    cfg.mf_p2 = 256 - unpack('l', cfg.b_mf_p2.raw)[0]
    cfg.atk_p1 = unpack('l', cfg.b_atk_p1.raw)[0]
    cfg.atk_p2 = unpack('l', cfg.b_atk_p2.raw)[0]
    cfg.hitstop_p1 = unpack('l', cfg.b_hitstop_p1.raw)[0]
    cfg.hitstop_p2 = unpack('l', cfg.b_hitstop_p2.raw)[0]
    cfg.hit_p1 = unpack('h', cfg.b_hit_p1.raw)[0]
    cfg.hit_p2 = unpack('h', cfg.b_hit_p2.raw)[0]
    cfg.noguard_p1 = unpack('b', cfg.b_noguard_p1.raw)[0]
    cfg.noguard_p2 = unpack('b', cfg.b_noguard_p2.raw)[0]
    cfg.noguard_debug_p1 = cfg.noguard_p1
    cfg.noguard_debug_p2 = cfg.noguard_p2
    cfg.anten_stop = unpack('B', cfg.b_anten_stop_p1.raw)[0]
    cfg.anten2_stop = unpack('B', cfg.b_anten_stop_p2.raw)[0]

    cfg.hosei = unpack('l', cfg.b_hosei.raw)[0]
    cfg.gauge_p1 = unpack('l', cfg.b_gauge_p1.raw)[0]
    cfg.gauge_p2 = unpack('l', cfg.b_gauge_p2.raw)[0]

    cfg.m_gauge_p1 = unpack('l', cfg.b_m_gauge_p1.raw)[0]
    cfg.m_gauge_p2 = unpack('l', cfg.b_m_gauge_p2.raw)[0]

    if unpack('h', cfg.b_ukemi1.raw)[0] != 0:
        cfg.ukemi1 = unpack('h', cfg.b_ukemi1.raw)[0] + 1

    cfg.ukemi2 = unpack('h', cfg.b_ukemi2.raw)[0]
    cfg.damage = unpack('l', cfg.b_damage.raw)[0]
    cfg.dmy_timer = unpack('l', cfg.b_dmy_timer.raw)[0]
    cfg.dmyend_timer = unpack('l', cfg.b_dmyend_timer.raw)[0]

    if cfg.mf_p1 == 256:
        cfg.mf_p1 = 0

    if cfg.mf_p2 == 256:
        cfg.mf_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mf_p1 > 1:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mf_p2 > 1:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 21:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 21:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 39 and cfg.mftp_p2 != 590:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 38 and cfg.mftp_p2 != 590:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 81:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 81:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 80:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 80:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 149:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 149:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 98:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 98:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 147:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 147:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 171:
        cfg.mf_p1 = 0
        cfg.mftp_p1 = 0

    if cfg.noguard_p2 == 77 and cfg.mftp_p2 == 171:
        cfg.mf_p2 = 0
        cfg.mftp_p2 = 0

    if (cfg.mftp_p1 == 0 or cfg.mftp_p1 == 10 or
            cfg.mftp_p1 == 11 or cfg.mftp_p1 == 12 or
            cfg.mftp_p1 == 13 or cfg.mftp_p1 == 14 or
            cfg.mftp_p1 == 15 or cfg.mftp_p1 == 18 or
            cfg.mftp_p1 == 40 or cfg.mftp_p1 == 20 or
            cfg.mftp_p1 == 16 or cfg.mftp_p1 == 594 or
            cfg.mftp_p1 == 17):
        cfg.mftp_p1 = 0

    if (cfg.mftp_p2 == 0 or cfg.mftp_p2 == 10 or
            cfg.mftp_p2 == 11 or cfg.mftp_p2 == 12 or
            cfg.mftp_p2 == 13 or cfg.mftp_p2 == 14 or
            cfg.mftp_p2 == 15 or cfg.mftp_p2 == 18 or
            cfg.mftp_p2 == 40 or cfg.mftp_p2 == 20 or
            cfg.mftp_p2 == 16 or cfg.mftp_p2 == 594 or
            cfg.mftp_p2 == 17):
        cfg.mftp_p2 = 0

    if cfg.hitstop_p1 == 65536:
        cfg.hitstop_p1 = 0

    if cfg.hitstop_p2 == 65536:
        cfg.hitstop_p2 = 0


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg.x_p1).rjust(8, " ")
    x_p2 = str(cfg.x_p2).rjust(8, " ")

    zen_P1 = str(cfg.zen_P1).rjust(3, " ")
    zen_P2 = str(cfg.zen_P2).rjust(3, " ")

    gauge_p1 = str('{:.02f}'.format(cfg.gauge_p1 / 100)).rjust(7, " ")
    gauge_p2 = str('{:.02f}'.format(cfg.gauge_p2 / 100)).rjust(7, " ")

    m_gauge_p1 = str('{:.02f}'.format(cfg.m_gauge_p1 / 100)).rjust(7, " ")
    m_gauge_p2 = str('{:.02f}'.format(cfg.m_gauge_p2 / 100)).rjust(7, " ")

    act_P1 = str(cfg.act_P1).rjust(3, " ")
    act_P2 = str(cfg.act_P2).rjust(3, " ")

    # yuuriF = str(cfg.yuuriF).rjust(4, " ")
    yuuriF = str(cfg.yuuriF).rjust(7, " ")


    hosei = str(cfg.hosei).rjust(4, " ")
    ukemi1 = str(cfg.ukemi1).rjust(3, " ")
    ukemi2 = str(cfg.ukemi2).rjust(3, " ")
    kyori = cfg.x_p1 - cfg.x_p2

    # damage = cfg.damage
    # kouritu = "0".rjust(8, " ")
    # # if damage != 0:
    # #     kouritu = damage / (100 - cfg.hosei)
    # #     kouritu = str('{:.02f}'.format(kouritu)).rjust(8, " ")

    cfg.P1_Bar = ""
    cfg.P2_Bar = ""
    temp = cfg.Bar_num
    temp = temp + 1
    for n in cfg.p1_barlist:

        if temp == 80:
            temp = 0

        cfg.P1_Bar += cfg.p1_barlist[temp]
        temp += 1

    for n in cfg.p2_barlist:

        if temp == 80:
            temp = 0

        cfg.P2_Bar += cfg.p2_barlist[temp]
        temp += 1

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += '1P|Position' + x_p1
    state_str += ' FirstActive' + act_P1
    state_str += ' Overall' + zen_P1
    state_str += ' Circuit' + gauge_p1 + '%'
    state_str += ' Moon' + m_gauge_p1 + '%' + END

    state_str += '2P|Position' + x_p2
    state_str += ' FirstActive' + act_P2
    state_str += ' Overall' + zen_P2
    state_str += ' Circuit' + gauge_p2 + '%'
    state_str += ' Moon' + m_gauge_p2 + '%' + END


    state_str += '  |Advantage' + yuuriF
    state_str += ' Proration' + hosei + "%"
    state_str += ' Untec' + ukemi1 + ',' + ukemi2
    state_str += '  Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.P1_Bar + END
    state_str += '2P|' + cfg.P2_Bar + END

    print(state_str)

    # print("hit_p1 " + str(cfg.hit_p1).rjust(7, " ") + " noguard_p1 " + str(cfg.noguard_debug_p1).rjust(7, " ") + "  mftp_p1 " +
    #       str(cfg.mftp_debug_p1).rjust(7, " ") + "  mf_p1 " + str(cfg.mf_p1).rjust(7, " "))
    # print("hit_p2 " + str(cfg.hit_p2).rjust(7, " ") + " noguard_p2 " + str(cfg.noguard_debug_p2).rjust(7, " ") + "  mftp_p2 " +
    #       str(cfg.mftp_debug_p2).rjust(7, " ") + "  mf_p2 " + str(cfg.mf_p2).rjust(7, " "))
    # print("f_timer " + str(cfg.f_timer).rjust(7, " "))


def determineReset():
    bar_ini_flag = 0
    cfg.interval_time = 0
    # 状況でインターバルを変化
    if cfg.Bar_num >= 80:
        cfg.interval_time = 10
    else:
        cfg.interval_time = 50

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.Bar_flag == 1:
        bar_ini_flag = 1

    cfg.interval2 += 1

    # # 起き上がりセットプレイ研究用リセット
    # if (
    #     cfg.mftp_p2 == 590 and
    #     cfg.interval2 > 80
    # ):
    #     bar_ini_flag = 1

    # # 1Pがジャンプする際にリセット
    # if (
    #     (
    #         (cfg.mftp_p1 == 36 and cfg.old_mftp != 36) or
    #         (cfg.mftp_p1 == 35 and cfg.old_mftp != 35) or
    #         (cfg.mftp_p1 == 39 and cfg.old_mftp != 39) or
    #         (cfg.mftp_p1 == 38 and cfg.old_mftp != 38)
    #     ) and cfg.interval2 > 80
    # ):
    #     bar_ini_flag = 1

    cfg.old_mftp = cfg.mftp_p1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()


def timer_check():
    ReadMem(cfg.h_pro, ad.TIMER_AD, cfg.b_timer, 4, None)
    cfg.f_timer = unpack('l', cfg.b_timer.raw)[0]


def tr_flag_check():

    ReadMem(cfg.h_pro, ad.TR_FLAG_AD, cfg.b_tr_flag, 1, None)

def startposi():
    x_p1 = unpack('l', cfg.b_dat_p1.raw)[0]
    x_p2 = unpack('l', cfg.b_dat_p2.raw)[0]

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

    WriteMem(cfg_ml.h_pro, ad_ml.START_POSI_AD, b_ini_posi_flag, 1, None)
