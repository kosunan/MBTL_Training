from ctypes import windll,  wintypes, byref
from struct import unpack, pack
import psutil
import cfg_ml
import ad_ml
cfg = cfg_ml
ad = ad_ml
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


def situationMem():
    # 状況を記憶
    ReadMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    ReadMem(cfg.h_pro, ad.X_P1_AD, cfg.b_dat_p1, 4, None)
    ReadMem(cfg.h_pro, ad.X_P2_AD, cfg.b_dat_p2, 4, None)
    ReadMem(cfg.h_pro, ad.X_P3_AD, cfg.b_dat_p3, 4, None)
    ReadMem(cfg.h_pro, ad.X_P4_AD, cfg.b_dat_p4, 4, None)
    ReadMem(cfg.h_pro, ad.M_ST_P1_AD, cfg.b_m_st_p1, 1, None)
    ReadMem(cfg.h_pro, ad.M_ST_P2_AD, cfg.b_m_st_p2, 1, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P1_AD, cfg.b_m_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P2_AD, cfg.b_m_gauge_p2, 4, None)


def situationWrit():
    # 状況を再現
    WriteMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    WriteMem(cfg.h_pro, ad.X_P1_AD, cfg.b_dat_p1, 4, None)
    WriteMem(cfg.h_pro, ad.X_P2_AD, cfg.b_dat_p2, 4, None)
    WriteMem(cfg.h_pro, ad.X_P3_AD, cfg.b_dat_p3, 4, None)
    WriteMem(cfg.h_pro, ad.X_P4_AD, cfg.b_dat_p4, 4, None)
    WriteMem(cfg.h_pro, ad.M_ST_P1_AD, cfg.b_m_st_p1, 1, None)
    WriteMem(cfg.h_pro, ad.M_ST_P2_AD, cfg.b_m_st_p2, 1, None)
    WriteMem(cfg.h_pro, ad.M_GAUGE_P1_AD, cfg.b_m_gauge_p1, 4, None)
    WriteMem(cfg.h_pro, ad.M_GAUGE_P2_AD, cfg.b_m_gauge_p2, 4, None)


def situationCheck():
    # タッグキャラ対策
    ReadMem(cfg.h_pro, ad.HI_KO_P1_AD, cfg.b_hi_ko_flag_p1, 1, None)
    ReadMem(cfg.h_pro, ad.HI_KO_P2_AD, cfg.b_hi_ko_flag_p2, 1, None)
    hi_ko_flag1 = unpack('b', cfg.b_hi_ko_flag_p1.raw)[0]
    hi_ko_flag2 = unpack('b', cfg.b_hi_ko_flag_p2.raw)[0]

    if hi_ko_flag1 == 0:  # 翡翠
        ReadMem(cfg.h_pro, ad.X_P1_AD, cfg.b_x_p1, 4, None)
        ReadMem(cfg.h_pro, ad.ATK_P1_AD, cfg.b_atk_p1, 4, None)
        ReadMem(cfg.h_pro, ad.HITSTOP_P1_AD, cfg.b_hitstop_p1, 4, None)
        ReadMem(cfg.h_pro, ad.HIT_P1_AD, cfg.b_hit_p1, 2, None)
        ReadMem(cfg.h_pro, ad.NOGUARD_P1_AD, cfg.b_noguard_p1, 1, None)
        ReadMem(cfg.h_pro, ad.MOTION_TYPE_P1_AD, cfg.b_mftp_p1, 2, None)
        ReadMem(cfg.h_pro, ad.MOTION_P1_AD, cfg.b_mf_p1, 4, None)
        ReadMem(cfg.h_pro, ad.GAUGE_P1_AD, cfg.b_gauge_p1, 4, None)
        ReadMem(cfg.h_pro, ad.ANTEN_STOP_AD, cfg.b_anten_stop, 1, None)

    elif hi_ko_flag1 == 1:  # 琥珀
        ReadMem(cfg.h_pro, ad.X_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_x_p1, 4, None)
        ReadMem(cfg.h_pro, ad.ATK_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_atk_p1, 4, None)
        ReadMem(cfg.h_pro, ad.HITSTOP_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_hitstop_p1, 4, None)
        ReadMem(cfg.h_pro, ad.HIT_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_hit_p1, 2, None)
        ReadMem(cfg.h_pro, ad.NOGUARD_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_noguard_p1, 1, None)
        ReadMem(cfg.h_pro, ad.MOTION_TYPE_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_mftp_p1, 2, None)
        ReadMem(cfg.h_pro, ad.MOTION_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_mf_p1, 4, None)
        ReadMem(cfg.h_pro, ad.GAUGE_P1_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_gauge_p1, 4, None)
        ReadMem(cfg.h_pro, ad.ANTEN_STOP_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_anten_stop, 1, None)

    if hi_ko_flag2 == 0:  # 翡翠
        ReadMem(cfg.h_pro, ad.X_P2_AD, cfg.b_x_p2, 4, None)
        ReadMem(cfg.h_pro, ad.ATK_P2_AD, cfg.b_atk_p2, 4, None)
        ReadMem(cfg.h_pro, ad.HIT_P2_AD, cfg.b_hit_p2, 2, None)
        ReadMem(cfg.h_pro, ad.HITSTOP_P2_AD, cfg.b_hitstop_p2, 4, None)
        ReadMem(cfg.h_pro, ad.NOGUARD_P2_AD, cfg.b_noguard_p2, 1, None)
        ReadMem(cfg.h_pro, ad.MOTION_TYPE_P2_AD, cfg.b_mftp_p2, 2, None)
        ReadMem(cfg.h_pro, ad.MOTION_P2_AD, cfg.b_mf_p2, 4, None)
        ReadMem(cfg.h_pro, ad.ANTEN2_STOP_AD, cfg.b_anten2_stop, 1, None)
        ReadMem(cfg.h_pro, ad.GAUGE_P2_AD, cfg.b_gauge_p2, 4, None)
        ReadMem(cfg.h_pro, ad.UKEMI_AD, cfg.b_ukemi, 2, None)

    elif hi_ko_flag2 == 1:  # 琥珀
        ReadMem(cfg.h_pro, ad.X_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_x_p2, 4, None)
        ReadMem(cfg.h_pro, ad.ATK_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_atk_p2, 4, None)
        ReadMem(cfg.h_pro, ad.HIT_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_hit_p2, 2, None)
        ReadMem(cfg.h_pro, ad.HITSTOP_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_hitstop_p2, 4, None)
        ReadMem(cfg.h_pro, ad.NOGUARD_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_noguard_p2, 1, None)
        ReadMem(cfg.h_pro, ad.MOTION_TYPE_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_mftp_p2, 2, None)
        ReadMem(cfg.h_pro, ad.MOTION_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_mf_p2, 4, None)
        ReadMem(cfg.h_pro, ad.ANTEN2_STOP_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_anten2_stop, 1, None)
        ReadMem(cfg.h_pro, ad.GAUGE_P2_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_gauge_p2, 4, None)
        ReadMem(cfg.h_pro, ad.UKEMI_AD + (ad.PLR_STRUCT_SIZE * 2), cfg.b_ukemi, 2, None)

    # 状況チェック
    ReadMem(cfg.h_pro, ad.TIMER_AD, cfg.b_f_timer, 4, None)
    ReadMem(cfg.h_pro, ad.HOSEI_AD, cfg.b_hosei, 4, None)
    ReadMem(cfg.h_pro, ad.UKEMI2_AD, cfg.b_ukemi2, 2, None)
    ReadMem(cfg.h_pro, ad.TR_FLAG_AD, cfg.b_tr_flag, 1, None)
    ReadMem(cfg.h_pro, ad.DAMAGE_AD, cfg.b_damage, 4, None)
    ReadMem(cfg.h_pro, ad.DMY_TIMER_AD, cfg.b_dmy_timer, 4, None)
    ReadMem(cfg.h_pro, ad.DMYEND_TIMER_AD, cfg.b_dmyend_timer, 4, None)


def change():

    cfg.x_p1.raw = pack('l', unpack('l', cfg.b_x_p1.raw)[0] * -1)
    cfg.x_p2.raw = pack('l', unpack('l', cfg.b_x_p2.raw)[0] * -1)
    cfg.cam_1.raw = pack('l', unpack('l', cfg.b_cam_1.raw)[0] * -1)
    cfg.cam_2.raw = pack('l', unpack('l', cfg.b_cam_2.raw)[0] * -1)
    cfg.cam_3.raw = pack('l', unpack('l', cfg.b_cam_3.raw)[0] * -1)

    WriteMem(cfg.h_pro, ad.X_P1_AD, cfg.b_x_p1.raw, 4, None)
    WriteMem(cfg.h_pro, ad.X_P2_AD, cfg.b_x_p2.raw, 4, None)
    WriteMem(cfg.h_pro, ad.CAM_1_AD, cfg.b_cam_1.raw, 4, None)
    WriteMem(cfg.h_pro, ad.CAM_2_AD, cfg.b_cam_2.raw, 4, None)
    WriteMem(cfg.h_pro, ad.CAM_3_AD, cfg.b_cam_3.raw, 4, None)


def moon_change():
    if cfg.moonchange_flag == 0:
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD, b'\x01', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD, b'\x01', 1, None)
        cfg.moonchange_flag = 1
    else:
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD, b'\x00', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD, b'\x00', 1, None)
        cfg.moonchange_flag = 0


def MAX_Damage_ini():
    temp = b'\x00\x00\x00\x00'
    WriteMem(cfg.h_pro, ad.MAX_Damage_AD, temp, 4, None)


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
        cfg.Bar_flag = 1
        cfg.interval = 0
    else:
        cfg.Bar_flag = 0
        cfg.interval += 1

    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.Bar_num != 0:
        cfg.Bar_flag = 1

    # 暗転判定処理
    if cfg.anten_stop == 128 or cfg.anten2_stop == 128:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # バー追加処理
    if cfg.Bar_num <= 80 and cfg.Bar_flag == 1:
        if ((cfg.hitstop_p1 != 0 and cfg.hitstop_p2 != 0) == False):
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

    cfg.p1_barlist[cfg.Bar_num] = P1_b_c + p1num.rjust(2, " ")[-2:]
    cfg.p2_barlist[cfg.Bar_num] = P2_b_c + p2num.rjust(2, " ")[-2:]
    if cfg.anten <= 1:
        cfg.Bar_num += 1


def bar_ini():
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
    if cfg.hitstop_p2 != 0 and cfg.act_flag_P1 == 0:
        cfg.act_P1 = cfg.zen_P1
        cfg.act_flag_P1 = 1

    if cfg.hitstop_p1 != 0 and cfg.act_flag_P2 == 0:
        cfg.act_P2 = cfg.zen_P2
        cfg.act_flag_P2 = 1

    if cfg.mf_p1 == 0 and cfg.atk_p1 == 0:
        cfg.act_flag_P1 = 0

    if cfg.mf_p2 == 0 and cfg.atk_p2 == 0:
        cfg.act_flag_P2 = 0


def get_values():
    cfg.f_timer = unpack('l', cfg.b_f_timer.raw)[0]
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
    cfg.anten_stop = unpack('B', cfg.b_anten_stop.raw)[0]
    cfg.anten2_stop = unpack('B', cfg.b_anten2_stop.raw)[0]

    cfg.hosei = unpack('l', cfg.b_hosei.raw)[0]
    cfg.gauge_p1 = unpack('l', cfg.b_gauge_p1.raw)[0]
    cfg.gauge_p2 = unpack('l', cfg.b_gauge_p2.raw)[0]
    if unpack('h', cfg.b_ukemi.raw)[0] != 0:
        cfg.ukemi = unpack('h', cfg.b_ukemi.raw)[0] + 1

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

    # if cfg.noguard_p1 == 77 and cfg.mftp_p1 == 39:
    #     cfg.mf_p1 = 0
    #     cfg.mftp_p1 = 0

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

    gauge_p1 = str('{:.02f}'.format(cfg.gauge_p1 / 100)).rjust(10, " ")
    gauge_p2 = str('{:.02f}'.format(cfg.gauge_p2 / 100)).rjust(10, " ")

    act_P1 = str(cfg.act_P1).rjust(3, " ")
    act_P2 = str(cfg.act_P2).rjust(3, " ")

    yuuriF = str(cfg.yuuriF).rjust(3, " ")
    hosei = str(cfg.hosei).rjust(3, " ")
    ukemi = str(cfg.ukemi).rjust(3, " ")
    ukemi2 = str(cfg.ukemi2).rjust(3, " ")
    kyori = cfg.x_p1 - cfg.x_p2

    cfg.P1_Bar = ""
    cfg.P2_Bar = ""
    for n in cfg.p1_barlist:
        cfg.P1_Bar += n

    for n in cfg.p2_barlist:
        cfg.P2_Bar += n

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += '1P|Position' + x_p1
    state_str += '|FirstActive' + act_P1
    state_str += '|Overall' + zen_P1
    state_str += '|Circuit' + gauge_p1 + '%' + \
        '   F1key Reset    F2key Position and moon save    F3key Switching moon' + END

    state_str += '2P|Position' + x_p2
    state_str += '|FirstActive' + act_P2
    state_str += '|Overall' + zen_P2
    state_str += '|Circuit' + gauge_p2 + '%' + END

    state_str += '  ' + '|Advantage   ' + yuuriF
    state_str += '|Proration ' + hosei + "%"
    state_str += '|Untechable' + ukemi + ',' + ukemi2
    state_str += '|Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.P1_Bar + END
    state_str += '2P|' + cfg.P2_Bar + END
    print(state_str)
    # print("anten2_stop " + str(cfg.anten2_stop).rjust(7, " "))
    # #
    # print("hit_p1 " + str(cfg.hit_p1).rjust(7, " ") + " noguard_p1 " + str(cfg.noguard_debug_p1).rjust(7, " ") + "  mftp_p1 " +
    #       str(cfg.mftp_debug_p1).rjust(7, " ") + "  mf_p1 " + str(cfg.mf_p1).rjust(7, " "))
    # print("hit_p2 " + str(cfg.hit_p2).rjust(7, " ") + " noguard_p2 " + str(cfg.noguard_debug_p2).rjust(7, " ") + "  mftp_p2 " +
    #       str(cfg.mftp_debug_p2).rjust(7, " ") + "  mf_p2 " + str(cfg.mf_p2).rjust(7, " "))


def determineReset():
    bar_ini_flag = 0
    cfg.interval_time = 0
    # 状況でインターバルを変化
    if cfg.Bar_num >= 80:
        cfg.interval_time = 10
    else:
        cfg.interval_time = 40

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.Bar_flag == 1:
        bar_ini_flag = 1

    cfg.interval2 += 1

    # 起き上がりセットプレイ研究用リセット
    if (
        cfg.mftp_p2 == 590 and
        cfg.interval2 > 80
    ):
        bar_ini_flag = 1

    # 1Pがジャンプする際にリセット
    if (
        (
            (cfg.mftp_p1 == 36 and cfg.old_mftp != 36) or
            (cfg.mftp_p1 == 35 and cfg.old_mftp != 35) or
            (cfg.mftp_p1 == 39 and cfg.old_mftp != 39) or
            (cfg.mftp_p1 == 38 and cfg.old_mftp != 38)
        ) and cfg.interval2 > 80
    ):
        bar_ini_flag = 1

    cfg.old_mftp = cfg.mftp_p1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()
