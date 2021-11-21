from ctypes import windll,  wintypes, byref
from struct import unpack, pack
import psutil
import cfg_ml
import ad_ml
import time
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

    cfg_ml.pid = dict_pids["MBTL.exe"]
    cfg_ml.h_pro = OpenProcess(0x1F0FFF, False, cfg_ml.pid)


def pause():

    # 一時停止
    WriteMem(cfg_ml.h_pro, ad_ml.STOP_AD, b'\x01', 1, None)


def play():

    # 再生
    WriteMem(cfg_ml.h_pro, ad_ml.STOP_AD, b'\x00', 1, None)


def situationMem():
    # 状況を記憶
    ReadMem(cfg_ml.h_pro, ad_ml.DAT1_AD, cfg_ml.b_dat_1, 4619, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAT2_AD, cfg_ml.b_dat_2, 2000, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAT_P1_AD, cfg_ml.b_dat_p1, 3060, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAT_P2_AD, cfg_ml.b_dat_p2, 3060, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAT_P3_AD, cfg_ml.b_dat_p3, 3060, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAT_P3_AD, cfg_ml.b_dat_p3, 3060, None)

def situationWrit():
    # 状況を再現
    WriteMem(cfg_ml.h_pro, ad_ml.DAT1_AD, cfg_ml.b_dat_1, 4619, None)
    # WriteMem(cfg_ml.h_pro, ad_ml.DAT2_AD, cfg_ml.b_dat_2, 2000, None)
    WriteMem(cfg_ml.h_pro, ad_ml.DAT_P1_AD, cfg_ml.b_dat_p1, 3060, None)
    WriteMem(cfg_ml.h_pro, ad_ml.DAT_P2_AD, cfg_ml.b_dat_p2, 3060, None)
    # WriteMem(cfg_ml.h_pro, ad_ml.DAT_P3_AD, cfg_ml.b_dat_p3, 3060, None)
    # WriteMem(cfg_ml.h_pro, ad_ml.DAT_P3_AD, cfg_ml.b_dat_p3, 3060, None)
    print("2")
    time.sleep(1)
    # 再生
    WriteMem(cfg_ml.h_pro, ad_ml.STOP_AD, b'\x00', 1, None)

def situationCheck():

    # 状況チェック
    ReadMem(cfg_ml.h_pro, ad_ml.TIMER_AD, cfg_ml.b_f_timer, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.X_P1_AD, cfg_ml.b_x_p1, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.X_P2_AD, cfg_ml.b_x_p2, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.ATK_P1_AD, cfg_ml.b_atk_p1, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.ATK_P2_AD, cfg_ml.b_atk_p2, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.HITSTOP_P1_AD, cfg_ml.b_hitstop_p1, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.HITSTOP_P2_AD, cfg_ml.b_hitstop_p2, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.HIT_P1_AD, cfg_ml.b_hit_p1, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.HIT_P2_AD, cfg_ml.b_hit_p2, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.NOGUARD_P1_AD, cfg_ml.b_noguard_p1, 1, None)
    ReadMem(cfg_ml.h_pro, ad_ml.NOGUARD_P2_AD, cfg_ml.b_noguard_p2, 1, None)
    ReadMem(cfg_ml.h_pro, ad_ml.MOTION_TYPE_P1_AD, cfg_ml.b_mftp_p1, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.MOTION_TYPE_P2_AD, cfg_ml.b_mftp_p2, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.MOTION_P1_AD, cfg_ml.b_mf_p1, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.MOTION_P2_AD, cfg_ml.b_mf_p2, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.HOSEI_AD, cfg_ml.b_hosei, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.ANTEN_STOP_AD, cfg_ml.b_anten_stop, 1, None)
    ReadMem(cfg_ml.h_pro, ad_ml.ANTEN2_STOP_AD, cfg_ml.b_anten2_stop, 1, None)
    ReadMem(cfg_ml.h_pro, ad_ml.GAUGE_P1_AD, cfg_ml.b_gauge_p1, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.GAUGE_P2_AD, cfg_ml.b_gauge_p2, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.UKEMI_AD, cfg_ml.b_ukemi, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.UKEMI2_AD, cfg_ml.b_ukemi2, 2, None)
    ReadMem(cfg_ml.h_pro, ad_ml.TR_FLAG_AD, cfg_ml.b_tr_flag, 1, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DAMAGE_AD, cfg_ml.b_damage, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DMY_TIMER_AD, cfg_ml.b_dmy_timer, 4, None)
    ReadMem(cfg_ml.h_pro, ad_ml.DMYEND_TIMER_AD,
            cfg_ml.b_dmyend_timer, 4, None)


def change():

    cfg_ml.x_p1.raw = pack('l', unpack('l', cfg_ml.b_x_p1.raw)[0] * -1)
    cfg_ml.x_p2.raw = pack('l', unpack('l', cfg_ml.b_x_p2.raw)[0] * -1)
    cfg_ml.cam_1.raw = pack('l', unpack('l', cfg_ml.b_cam_1.raw)[0] * -1)
    cfg_ml.cam_2.raw = pack('l', unpack('l', cfg_ml.b_cam_2.raw)[0] * -1)
    cfg_ml.cam_3.raw = pack('l', unpack('l', cfg_ml.b_cam_3.raw)[0] * -1)

    WriteMem(cfg_ml.h_pro, ad_ml.X_P1_AD, cfg_ml.b_x_p1.raw, 4, None)
    WriteMem(cfg_ml.h_pro, ad_ml.X_P2_AD, cfg_ml.b_x_p2.raw, 4, None)
    WriteMem(cfg_ml.h_pro, ad_ml.CAM_1_AD, cfg_ml.b_cam_1.raw, 4, None)
    WriteMem(cfg_ml.h_pro, ad_ml.CAM_2_AD, cfg_ml.b_cam_2.raw, 4, None)
    WriteMem(cfg_ml.h_pro, ad_ml.CAM_3_AD, cfg_ml.b_cam_3.raw, 4, None)


def moon_change():
    if cfg_ml.moonchange_flag == 0:
        WriteMem(cfg_ml.h_pro, ad_ml.M_ST_P1_AD, b'\x01', 1, None)
        WriteMem(cfg_ml.h_pro, ad_ml.M_ST_P2_AD, b'\x01', 1, None)
        cfg_ml.moonchange_flag = 1
    else:
        WriteMem(cfg_ml.h_pro, ad_ml.M_ST_P1_AD, b'\x00', 1, None)
        WriteMem(cfg_ml.h_pro, ad_ml.M_ST_P2_AD, b'\x00', 1, None)
        cfg_ml.moonchange_flag = 0


def MAX_Damage_ini():
    temp = b'\x00\x00\x00\x00'
    WriteMem(cfg_ml.h_pro, ad_ml.MAX_Damage_AD, temp, 4, None)


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (
        cfg_ml.mftp_p1 != 0 or
        cfg_ml.mftp_p2 != 0 or
        cfg_ml.hitstop_p1 != 0 or
        cfg_ml.hitstop_p2 != 0 or
        cfg_ml.hit_p1 != 0 or
        cfg_ml.hit_p2 != 0
    ):
        cfg_ml.Bar_flag = 1
        cfg_ml.interval = 0
    else:
        cfg_ml.Bar_flag = 0
        cfg_ml.interval += 1

    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg_ml.interval_time >= cfg_ml.interval and cfg_ml.Bar_num != 0:
        cfg_ml.Bar_flag = 1

    # 暗転判定処理
    if cfg_ml.anten_stop == 128 or cfg_ml.anten2_stop == 128:
        cfg_ml.anten += 1
    else:
        cfg_ml.anten = 0

    # バー追加処理
    if cfg_ml.Bar_num <= 80 and cfg_ml.Bar_flag == 1:
        if ((cfg_ml.hitstop_p1 != 0 and cfg_ml.hitstop_p2 != 0) == False):
            bar_add()


def advantage_calc():

    if cfg_ml.hit_p1 == 0 and cfg_ml.hit_p2 == 0 and cfg_ml.mftp_p1 == 0 and cfg_ml.mftp_p2 == 0:
        cfg_ml.DataFlag1 = 0

    if (cfg_ml.hit_p1 != 0 or cfg_ml.mftp_p1 != 0) and (cfg_ml.hit_p2 != 0 or cfg_ml.mftp_p2 != 0):
        cfg_ml.DataFlag1 = 1
        cfg_ml.yuuriF = 0

    if cfg_ml.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg_ml.hit_p1 == 0 and cfg_ml.mftp_p1 == 0) and (cfg_ml.hit_p2 != 0 or cfg_ml.mftp_p2 != 0):
            cfg_ml.yuuriF += 1

        # 不利フレーム検証
        if (cfg_ml.hit_p1 != 0 or cfg_ml.mftp_p1 != 0) and (cfg_ml.hit_p2 == 0 and cfg_ml.mftp_p2 == 0):
            cfg_ml.yuuriF -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg_ml.mf_p1 != 0:
        cfg_ml.zen_P1 = cfg_ml.mf_p1

    if cfg_ml.mf_p2 != 0:
        cfg_ml.zen_P2 = cfg_ml.mf_p2


def advantage_calc():
    if cfg_ml.hit_p1 == 0 and cfg_ml.hit_p2 == 0 and cfg_ml.mftp_p1 == 0 and cfg_ml.mftp_p2 == 0:
        cfg_ml.DataFlag1 = 0

    if (cfg_ml.hit_p1 != 0 or cfg_ml.mftp_p1 != 0) and (cfg_ml.hit_p2 != 0 or cfg_ml.mftp_p2 != 0):
        cfg_ml.DataFlag1 = 1
        cfg_ml.yuuriF = 0

    if cfg_ml.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg_ml.hit_p1 == 0 and cfg_ml.mftp_p1 == 0) and (cfg_ml.hit_p2 != 0 or cfg_ml.mftp_p2 != 0):
            cfg_ml.yuuriF += 1

        # 不利フレーム検証
        if (cfg_ml.hit_p1 != 0 or cfg_ml.mftp_p1 != 0) and (cfg_ml.hit_p2 == 0 and cfg_ml.mftp_p2 == 0):
            cfg_ml.yuuriF -= 1


def bar_add():

    # ESC[0m	指定をリセットし未指定状態に戻す。 SGRによって変化させたあとは、必ずこのコードを出力して他の出力に影響を与えないようにする
    # ESC[1m	ボールド指定、フォントが対応していれば太字になる。TeraTermでは色が変化、この色は設定で指定する
    # ESC[2m	薄く表示する、あまり対応されていないらしいが、gnome-terminalでは文字色が変化している
    # ESC[3m	イタリック表示、フォントが対応していればイタリック体になる
    # ESC[4m	アンダーライン
    # ESC[5m	ブリンク、毎分150回以下のペースで点滅する。TeraTermでは色が変化。この色は設定で指定する
    # ESC[6m	高速ブリンク、あまり対応されていないらしい
    # ESC[7m	反転、前景色と背景色を入れ替えて表示
    # ESC[8m	表示を隠す、gnome-terminalとxtermでは見えない。 選択による反転でも見えないが、コピーアンドペーストすると、ちゃんとその文字が出力されていることが分かる
    # ESC[9m	取り消し、gnome-terminalでは取り消し線が表示された
    # ESC[30m～ESC[37m	文字色指定、色番号0～7は後述
    # ESC[38m	文字色指定拡張用、引き続き引数をとる。5;xで、0～255のカラーインデックス指定。 2;r;g;bでRGB指定。ただし、24bitカラーが表示できる端末は少ない
    # ESC[39m	文字色をデフォルトに戻す
    # ESC[40m～ESC[47m	背景色指定、色番号0～7は後述
    # ESC[48m	背景色指定拡張用、引き続き引数をとる。5;xで、0～255のカラーインデックス指定。 2;r;g;bでRGB指定。ただし、24bitカラーが表示できる端末は少ない
    # ESC[49m	背景色をデフォルトに戻す
    # ESC[90m～ESC[97m	前景色指定、30番代の指定より強い色。標準ではないらしい
    # ESC[100m～ESC[107m	背景色指定、40番代の指定より強い色。標準ではないらしい

    # \x1b[48m;5;xで、0～255の背景色カラーインデックス指定。
    # \x1b[48m;5;xxxm

    # \x1b[38m;5;xで、0～255の文字色カラーインデックス指定。
    # \x1b[38m;5;xxxm

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
    if cfg_ml.b_atk_p1.raw != b'\x00\x00\x00\x00':  # 攻撃判定を出しているとき
        fb = atk

    elif cfg_ml.mf_p1 != 0:  # モーション途中
        fb = mot

    elif cfg_ml.hit_p1 != 0:  # ガード硬直中
        fb = grd

    elif cfg_ml.mftp_p1 != 0:  # ガードできないとき
        fb = nog

    elif cfg_ml.mf_p1 == 0:  # 何もしていないとき
        fb = fre

    P1_b_c = fb

    # 2P
    if cfg_ml.b_atk_p2.raw != b'\x00\x00\x00\x00':  # 攻撃判定を出しているとき
        fb = atk

    elif cfg_ml.mf_p2 != 0:  # モーション途中
        fb = mot

    elif cfg_ml.hit_p2 != 0:  # ガード硬直中
        fb = grd

    elif cfg_ml.mftp_p2 != 0:  # ガードできないとき
        fb = nog

    elif cfg_ml.mf_p2 == 0:  # 何もしていないとき
        fb = fre

    P2_b_c = fb

    if cfg_ml.mf_p1 != 0:
        p1num = str(cfg_ml.mf_p1)
    else:
        p1num = str(cfg_ml.mftp_p1)

    if cfg_ml.mf_p2 != 0:
        p2num = str(cfg_ml.mf_p2)
    else:
        p2num = str(cfg_ml.mftp_p2)

    if cfg_ml.hit_p1 != 0:
        p1num = str(cfg_ml.hit_p1)

    if cfg_ml.hit_p2 != 0:
        p2num = str(cfg_ml.hit_p2)

    if p1num == '':
        p1num = '0'

    if p2num == '':
        p2num = '0'

    cfg_ml.p1_barlist[cfg_ml.Bar_num] = P1_b_c + p1num.rjust(2, " ")[-2:]
    cfg_ml.p2_barlist[cfg_ml.Bar_num] = P2_b_c + p2num.rjust(2, " ")[-2:]
    if cfg_ml.anten <= 1:
        cfg_ml.Bar_num += 1


def bar_ini():
    cfg_ml.P1_Bar = ""
    cfg_ml.P2_Bar = ""
    cfg_ml.Bar_num = 0
    cfg_ml.interval = 0
    cfg_ml.interval2 = 0
    cfg_ml.bar_ini_flag2 = 0

    cfg_ml.p1_index = 0
    cfg_ml.p2_index = 0

    for n in range(len(cfg_ml.p1_barlist)):
        cfg_ml.p1_barlist[n] = ""

    for n in range(len(cfg_ml.p2_barlist)):
        cfg_ml.p2_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg_ml.hitstop_p2 != 0 and cfg_ml.act_flag_P1 == 0:
        cfg_ml.act_P1 = cfg_ml.zen_P1
        cfg_ml.act_flag_P1 = 1

    if cfg_ml.hitstop_p1 != 0 and cfg_ml.act_flag_P2 == 0:
        cfg_ml.act_P2 = cfg_ml.zen_P2
        cfg_ml.act_flag_P2 = 1

    if cfg_ml.mf_p1 == 0 and cfg_ml.atk_p1 == 0:
        cfg_ml.act_flag_P1 = 0

    if cfg_ml.mf_p2 == 0 and cfg_ml.atk_p2 == 0:
        cfg_ml.act_flag_P2 = 0


def get_values():
    cfg_ml.f_timer = unpack('l', cfg_ml.b_f_timer.raw)[0]
    cfg_ml.x_p1 = unpack('l', cfg_ml.b_x_p1.raw)[0]
    cfg_ml.x_p2 = unpack('l', cfg_ml.b_x_p2.raw)[0]
    cfg_ml.mftp_p1 = unpack('h', cfg_ml.b_mftp_p1.raw)[0]
    cfg_ml.mftp_p2 = unpack('h', cfg_ml.b_mftp_p2.raw)[0]
    cfg_ml.mftp_debug_p1 = cfg_ml.mftp_p1
    cfg_ml.mftp_debug_p2 = cfg_ml.mftp_p2
    cfg_ml.mf_p1 = 256 - unpack('l', cfg_ml.b_mf_p1.raw)[0]
    cfg_ml.mf_p2 = 256 - unpack('l', cfg_ml.b_mf_p2.raw)[0]
    cfg_ml.atk_p1 = unpack('l', cfg_ml.b_atk_p1.raw)[0]
    cfg_ml.atk_p2 = unpack('l', cfg_ml.b_atk_p2.raw)[0]
    cfg_ml.hitstop_p1 = unpack('l', cfg_ml.b_hitstop_p1.raw)[0]
    cfg_ml.hitstop_p2 = unpack('l', cfg_ml.b_hitstop_p2.raw)[0]
    cfg_ml.hit_p1 = unpack('h', cfg_ml.b_hit_p1.raw)[0]
    cfg_ml.hit_p2 = unpack('h', cfg_ml.b_hit_p2.raw)[0]
    cfg_ml.noguard_p1 = unpack('b', cfg_ml.b_noguard_p1.raw)[0]
    cfg_ml.noguard_p2 = unpack('b', cfg_ml.b_noguard_p2.raw)[0]
    cfg_ml.noguard_debug_p1 = cfg_ml.noguard_p1
    cfg_ml.noguard_debug_p2 = cfg_ml.noguard_p2
    cfg_ml.anten_stop = unpack('B', cfg_ml.b_anten_stop.raw)[0]
    cfg_ml.anten2_stop = unpack('B', cfg_ml.b_anten2_stop.raw)[0]

    cfg_ml.hosei = unpack('l', cfg_ml.b_hosei.raw)[0]
    cfg_ml.gauge_p1 = unpack('l', cfg_ml.b_gauge_p1.raw)[0]
    cfg_ml.gauge_p2 = unpack('l', cfg_ml.b_gauge_p2.raw)[0]
    if unpack('h', cfg_ml.b_ukemi.raw)[0] != 0:
        cfg_ml.ukemi = unpack('h', cfg_ml.b_ukemi.raw)[0]+1

    cfg_ml.ukemi2 = unpack('h', cfg_ml.b_ukemi2.raw)[0]
    cfg_ml.damage = unpack('l', cfg_ml.b_damage.raw)[0]
    cfg_ml.dmy_timer = unpack('l', cfg_ml.b_dmy_timer.raw)[0]
    cfg_ml.dmyend_timer = unpack('l', cfg_ml.b_dmyend_timer.raw)[0]

    if cfg_ml.mf_p1 == 256:
        cfg_ml.mf_p1 = 0

    if cfg_ml.mf_p2 == 256:
        cfg_ml.mf_p2 = 0

    if cfg_ml.noguard_p1 == 77 and cfg_ml.mf_p1 > 1:
        cfg_ml.mf_p1 = 0
        cfg_ml.mftp_p1 = 0

    if cfg_ml.noguard_p2 == 77 and cfg_ml.mf_p2 > 1:
        cfg_ml.mf_p2 = 0
        cfg_ml.mftp_p2 = 0

    if cfg_ml.noguard_p1 == 77 and cfg_ml.mftp_p1 == 21:
        cfg_ml.mf_p1 = 0
        cfg_ml.mftp_p1 = 0

    if cfg_ml.noguard_p2 == 77 and cfg_ml.mftp_p2 == 21:
        cfg_ml.mf_p2 = 0
        cfg_ml.mftp_p2 = 0

    if cfg_ml.noguard_p1 == 77 and cfg_ml.mftp_p1 == 39 and cfg_ml.mftp_p2 != 590:
        cfg_ml.mf_p1 = 0
        cfg_ml.mftp_p1 = 0

    if cfg_ml.noguard_p1 == 77 and cfg_ml.mftp_p1 == 38 and cfg_ml.mftp_p2 != 590:
        cfg_ml.mf_p1 = 0
        cfg_ml.mftp_p1 = 0

    # if cfg_ml.noguard_p1 == 77 and cfg_ml.mftp_p1 == 39:
    #     cfg_ml.mf_p1 = 0
    #     cfg_ml.mftp_p1 = 0

    if (cfg_ml.mftp_p1 == 0 or cfg_ml.mftp_p1 == 10 or
            cfg_ml.mftp_p1 == 11 or cfg_ml.mftp_p1 == 12 or
            cfg_ml.mftp_p1 == 13 or cfg_ml.mftp_p1 == 14 or
            cfg_ml.mftp_p1 == 15 or cfg_ml.mftp_p1 == 18 or
            cfg_ml.mftp_p1 == 40 or cfg_ml.mftp_p1 == 20 or
            cfg_ml.mftp_p1 == 16 or cfg_ml.mftp_p1 == 594 or
            cfg_ml.mftp_p1 == 17):
        cfg_ml.mftp_p1 = 0

    if (cfg_ml.mftp_p2 == 0 or cfg_ml.mftp_p2 == 10 or
            cfg_ml.mftp_p2 == 11 or cfg_ml.mftp_p2 == 12 or
            cfg_ml.mftp_p2 == 13 or cfg_ml.mftp_p2 == 14 or
            cfg_ml.mftp_p2 == 15 or cfg_ml.mftp_p2 == 18 or
            cfg_ml.mftp_p2 == 40 or cfg_ml.mftp_p2 == 20 or
            cfg_ml.mftp_p2 == 16 or cfg_ml.mftp_p2 == 594 or
            cfg_ml.mftp_p2 == 17):
        cfg_ml.mftp_p2 = 0

    if cfg_ml.hitstop_p1 == 65536:
        cfg_ml.hitstop_p1 = 0

    if cfg_ml.hitstop_p2 == 65536:
        cfg_ml.hitstop_p2 = 0


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg_ml.x_p1).rjust(8, " ")
    x_p2 = str(cfg_ml.x_p2).rjust(8, " ")

    zen_P1 = str(cfg_ml.zen_P1).rjust(3, " ")
    zen_P2 = str(cfg_ml.zen_P2).rjust(3, " ")

    gauge_p1 = str('{:.02f}'.format(cfg_ml.gauge_p1 / 100)).rjust(10, " ")
    gauge_p2 = str('{:.02f}'.format(cfg_ml.gauge_p2 / 100)).rjust(10, " ")

    act_P1 = str(cfg_ml.act_P1).rjust(3, " ")
    act_P2 = str(cfg_ml.act_P2).rjust(3, " ")

    yuuriF = str(cfg_ml.yuuriF).rjust(3, " ")
    hosei = str(cfg_ml.hosei).rjust(3, " ")
    ukemi = str(cfg_ml.ukemi).rjust(3, " ")
    ukemi2 = str(cfg_ml.ukemi2).rjust(3, " ")
    kyori = cfg_ml.x_p1 - cfg_ml.x_p2

    cfg_ml.P1_Bar = ""
    cfg_ml.P2_Bar = ""
    for n in cfg_ml.p1_barlist:
        cfg_ml.P1_Bar += n

    for n in cfg_ml.p2_barlist:
        cfg_ml.P2_Bar += n

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += '1P|Position' + x_p1
    state_str += '|FirstActive' + act_P1
    state_str += '|Overall' + zen_P1
    state_str += '|Circuit' + gauge_p1 + '%' + \
        '        Position and moon save F2key Switching moon F3key　' + END

    state_str += '2P|Position' + x_p2
    state_str += '|FirstActive' + act_P2
    state_str += '|Overall' + zen_P2
    state_str += '|Circuit' + gauge_p2 + '%' + END

    state_str += '  ' + '|Advantage   ' + yuuriF
    state_str += '|Proration ' + hosei + "%"
    state_str += '|Untechable' + ukemi + ',' + ukemi2
    state_str += '|Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg_ml.P1_Bar + END
    state_str += '2P|' + cfg_ml.P2_Bar + END
    print(state_str)
    # print("anten2_stop " + str(cfg_ml.anten2_stop).rjust(7, " "))
    # #
    # print("hit_p1 " + str(cfg_ml.hit_p1).rjust(7, " ") + " noguard_p1 " + str(cfg_ml.noguard_debug_p1).rjust(7, " ") + "  mftp_p1 " +
    #       str(cfg_ml.mftp_debug_p1).rjust(7, " ") + "  mf_p1 " + str(cfg_ml.mf_p1).rjust(7, " "))
    # print("hit_p2 " + str(cfg_ml.hit_p2).rjust(7, " ") + " noguard_p2 " + str(cfg_ml.noguard_debug_p2).rjust(7, " ") + "  mftp_p2 " +
    #       str(cfg_ml.mftp_debug_p2).rjust(7, " ") + "  mf_p2 " + str(cfg_ml.mf_p2).rjust(7, " "))


def determineReset():
    bar_ini_flag = 0
    cfg_ml.interval_time = 0
    # 状況でインターバルを変化
    if cfg_ml.Bar_num >= 80:
        cfg_ml.interval_time = 10
    else:
        cfg_ml.interval_time = 40

    # インターバル後の初期化
    if cfg_ml.interval_time <= cfg_ml.interval:
        cfg_ml.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg_ml.bar_ini_flag2 == 1 and cfg_ml.Bar_flag == 1:
        bar_ini_flag = 1

    cfg_ml.interval2 += 1

    # 起き上がりセットプレイ研究用リセット
    if (
        cfg_ml.mftp_p2 == 590 and
        cfg_ml.interval2 > 80
    ):
        bar_ini_flag = 1

    # 1Pがジャンプする際にリセット
    if (
        (
            (cfg_ml.mftp_p1 == 36 and cfg_ml.old_mftp != 36) or
            (cfg_ml.mftp_p1 == 35 and cfg_ml.old_mftp != 35) or
            (cfg_ml.mftp_p1 == 39 and cfg_ml.old_mftp != 39) or
            (cfg_ml.mftp_p1 == 38 and cfg_ml.old_mftp != 38)
        ) and cfg_ml.interval2 > 80
    ):
        bar_ini_flag = 1

    cfg_ml.old_mftp = cfg_ml.mftp_p1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()
