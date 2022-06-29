import os
import time
import ctypes
import psutil
from ctypes import windll,  byref
from struct import unpack, pack

import copy
import keyboard

import save_tl
import cfg_tl
import util_sub

cfg = cfg_tl
save = save_tl

windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory


def pause():

    # 一時停止
    util_sub.w_mem(cfg.STOP_AD, b'\x01')


def play():

    # 再生
    util_sub.w_mem(cfg.STOP_AD, b'\x00')


def tagCharacterCheck():
    if cfg.P1.tag_flag.num == 0:
        cfg.p_info[0] = cfg.p1 = cfg.P1
        cfg.p_info[2] = cfg.p3 = cfg.P3

    elif cfg.P1.tag_flag.num == 1:
        cfg.p_info[0] = cfg.p1 = cfg.P3
        cfg.p_info[2] = cfg.p3 = cfg.P1

    if cfg.P2.tag_flag.num == 0:
        cfg.p_info[1] = cfg.p2 = cfg.P2
        cfg.p_info[3] = cfg.p4 = cfg.P4

    elif cfg.P2.tag_flag.num == 1:
        cfg.p_info[3] = cfg.p2 = cfg.P4
        cfg.p_info[1] = cfg.p4 = cfg.P2


def situationCheck():
    jmp_number = [34, 35, 36, 37]
    jmp2_number = [39, 38, 40]

    ignore_number = [0, 10, 11, 12, 13, 14, 15, 16, 20, 44, 98,  171, 594]
# 87 空中ダッシュ 39 空中垂直ジャンプ　38 空中前ジャンプ　　40 空中前ジャンプ
# 80, 81　シールド
    for n in cfg.P_info:
        if n.motion_type.num != 0:
            n.motion_type_old = n.motion_type.num
        n.hitstop_old = n.hitstop.num
        n.anten_stop2_old = n.anten_stop2.num
        n.c_timer_old = n.c_timer.num
        util_sub.para_read(n.c_timer)
        util_sub.para_read(n.anten_stop)
        util_sub.para_read(n.anten_stop2)
        util_sub.para_read(n.atk)
        util_sub.para_read(n.gauge)
        util_sub.para_read(n.hit)
        util_sub.para_read(n.hitstop)
        util_sub.para_read(n.inv)
        util_sub.para_read(n.moon)
        util_sub.para_read(n.moon_st)
        util_sub.para_read(n.motion)
        util_sub.para_read(n.motion_type)
        util_sub.para_read(n.noguard)
        util_sub.para_read(n.seeld)
        util_sub.para_read(n.step_inv)
        util_sub.para_read(n.tag_flag)
        util_sub.para_read(n.ukemi1)
        util_sub.para_read(n.ukemi2)
        util_sub.para_read(n.x_posi)
        util_sub.para_read(n.y_posi)
        util_sub.para_read(n.air_flag)

        n.motion.num = 256 - n.motion.num
        if n.motion.num == 256:
            n.motion.num = 0

        if n.hitstop.num == 65536:
            n.hitstop.num = 0

        if n.motion_type_old == n.motion_type.num:
            n.motion_chenge_flag += 1
        else:
            n.motion_chenge_flag = 0

        n.ignore_flag = 0
        n.action_flag = 0
        for list_a in ignore_number:
            n.ignore_flag = 0
            if n.motion_type.num == list_a:
                n.ignore_flag = 1
                break

        if n.noguard.num == 0:
            n.action_flag = 1

        if n.noguard.num == 77 and n.motion_chenge_flag == 0 and n.motion_type.num != 21:
            if n.ignore_flag == 0:
                n.action_flag = 1

        elif n.noguard.num == 77 and n.motion_type.num != 0:
            n.action_flag = 0

        elif n.noguard.num != 77 and n.motion_type.num != 0:
            n.action_flag = 1

        for list_a in jmp2_number:
            if n.motion_type.num == list_a:
                for list_a in jmp_number:
                    if n.motion_type_old == list_a:
                        n.action_flag = 0
                        break
                break

        if n.motion_type.num == 21:
            if n.motion_type_old == 19:
                n.action_flag = 0

    util_sub.para_read(cfg.timer)
    util_sub.para_read(cfg.hosei)
    util_sub.para_read(cfg.damage)
    util_sub.para_read(cfg.start_posi)
    util_sub.para_read(cfg.ukemi)

    tagCharacterCheck()


def situationMem():
    # 状況を記憶
    util_sub.para_read(cfg.cam)
    save.P_info = copy.deepcopy(cfg.P_info)


def situationWrit():
    # 状況を再現
    util_sub.para_write(cfg.cam)

    for n in save.P_info:
        util_sub.para_write(n.gauge)
        util_sub.para_write(n.moon)
        util_sub.para_write(n.moon_st)
        util_sub.para_write(n.x_posi)


def moon_change():

    if cfg.P_info[0].moon_st.num == 0:
        for n in cfg.P_info:
            util_sub.w_mem(n.moon_st.ad, b'\x01')

    elif cfg.P_info[0].moon_st.num == 1:
        for n in cfg.P_info:
            util_sub.w_mem(n.moon_st.ad, b'\00')

    for n in cfg.P_info:
        util_sub.w_mem(n.moon.ad, b'\x10\x27')


def MAX_Damage_ini():
    util_sub.para_read(cfg.max_damage_pointer)
    addres = cfg.max_damage_pointer.num + 0x34

    WriteMem(cfg.h_pro, addres, b'\x01', 1, None)


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (
        cfg.p1.ignore_flag == 0 or
        cfg.p2.ignore_flag == 0 or
        cfg.p1.hitstop.num != 0 or
        cfg.p2.hitstop.num != 0 or
        cfg.p1.hit.num != 0 or
        cfg.p2.hit.num != 0
    ):
        cfg.reset_flag = 0
        cfg.bar_flag = 1
        cfg.interval = 0

    else:
        cfg.bar_flag = 0
        cfg.interval += 1

    # バーリセット判定
    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.reset_flag == 0:
        if cfg.bar80_flag == 0:
            cfg.bar_flag = 1

    # ヒットストップ処理
    if (cfg.p1.hitstop.num != 0 and cfg.p2.hitstop.num != 0):
        cfg.hitstop += 1
    elif (cfg.p1.hitstop.num == 0 or cfg.p2.hitstop.num == 0):
        cfg.hitstop = 0

    if cfg.p1.anten_stop.num == 16:  # 暗転しているとき
        cfg.anten += 1
    elif cfg.p2.anten_stop.num == 128:  # 暗転しているとき
        cfg.anten += 1
    elif cfg.p1.c_timer_old == cfg.p1.c_timer.num and cfg.p1.hit.num == 0 and cfg.p2.hit.num == 0 and cfg.p1.motion_type.num != 621 and cfg.p2.motion_type.num != 621:
        cfg.anten += 1
    elif cfg.p2.c_timer_old == cfg.p2.c_timer.num and cfg.p1.hit.num == 0 and cfg.p2.hit.num == 0 and cfg.p1.motion_type.num != 621 and cfg.p2.motion_type.num != 621:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # 攻撃判定持続計算
    for n in cfg.p_info:
        if n.atk.num != 0 and cfg.anten == 0 and cfg.hitstop == 0:  # 攻撃判定を出しているとき
            n.active += 1
        elif n.atk.num == 0 and cfg.anten == 0 and cfg.hitstop <= 1:  # 攻撃判定を出してないとき
            n.active = 0

    if cfg.anten <= 1 and cfg.hitstop <= 1 and cfg.bar_flag == 1:
        cfg.bar_num += 1
        if cfg.bar_num == cfg.bar_range:  # バーの繰り返し判定
            cfg.bar_num = 0
            cfg.bar80_flag = 1

    # バー追加処理
    if cfg.bar_flag == 1:
        bar_add()


def advantage_calc():

    if cfg.p1.hit.num == 0 and cfg.p2.hit.num == 0 and cfg.p1.action_flag == 0 and cfg.p2.action_flag == 0:
        cfg.advantage_calc_flag = 0

    elif (cfg.p1.hit.num != 0 or cfg.p1.action_flag == 1) and (cfg.p2.hit.num != 0 or cfg.p2.action_flag == 1):
        cfg.advantage_calc_flag = 1
        cfg.advantage_f = 0

    if cfg.advantage_calc_flag == 1:

        # 有利フレーム検証
        if (cfg.p1.hit.num == 0 and cfg.p1.action_flag == 0) and (cfg.p2.hit.num != 0 or cfg.p2.action_flag == 1):
            cfg.advantage_f += 1

        # 不利フレーム検証
        if (cfg.p1.hit.num != 0 or cfg.p1.action_flag == 1) and (cfg.p2.hit.num == 0 and cfg.p2.action_flag == 0):
            cfg.advantage_f -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg.p1.motion.num != 0:
        cfg.p1.zen = cfg.p1.motion.num

    if cfg.p2.motion.num != 0:
        cfg.p2.zen = cfg.p2.motion.num


def bar_add():

    DEF = '\x1b[0m'
    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    DEF = '\x1b[0m'
    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    atk = util_sub.get_font((255, 255, 255), (255, 0, 0))
    mot = util_sub.get_font((255, 255, 255), (65, 200, 0))
    mot2 = util_sub.get_font((255, 255, 255), (35, 158, 0))

    grd_stun = util_sub.get_font((255, 255, 255), (170, 170, 170))
    hit_stun = util_sub.get_font((255, 255, 255), (170, 170, 170))
    fre = util_sub.get_font((92, 92, 92), (0, 0, 0))
    jmp = util_sub.get_font((177, 177, 177), (241, 224, 132))
    seeld = util_sub.get_font((255, 255, 255), (145, 194, 255))
    inv = util_sub.get_font((200, 200, 200), (255, 255, 255))
    adv = util_sub.get_font((255, 255, 255), (0, 0, 0))
    bunker = util_sub.get_font((255, 255, 255), (225, 184, 0))
    air = util_sub.get_font((125, 127, 168), (125, 127, 168))

    jmp_number = [34, 35, 36, 37]

    ignore_number = [0, 10, 11, 12, 13, 14, 15, 16, 20, 44, 98, 149, 171, 594]

    for n in cfg.p_info:
        # バー１段目
        font = ""
        num = ""
        if (n.inv.num == 0 and n.motion.num != 0) or (n.step_inv.num != 0 and n.motion_type.num == 46):  # 無敵中
            font = inv

        elif n.seeld.num == 2 or n.seeld.num == 3:  # シールド中
            font = seeld

        elif n.hit.num != 0 or n.motion_type.num == 621:  # ガードorヒット硬直中
            font = grd_stun

        elif n.motion.num != 0:  # モーション途中
            font = mot

        elif n.action_flag == 1:
            font = mot

        elif n.action_flag == 0:
            font = fre

        for list_a in jmp_number:  # ジャンプ移行中
            if n.motion_type.num == list_a:
                font = jmp
                break

        # 起き上がり中
        if n.motion_type.num == 593:
            font = "\x1b[38;5;255m" + "\x1b[48;5;055m"

            num = ""
        if n.hit.num != 0:
            num = str(n.hit.num)
        elif n.action_flag == 0:
            num = str("")
        elif n.motion.num != 0:
            num = str(n.motion.num)
        elif n.motion_type.num != 0:
            num = str(n.motion_type.num)

        if cfg.advantage_calc_flag == 1 and n.hit.num == 0 and n.action_flag == 0:
            if n == cfg.p_info[0] or n == cfg.p_info[1]:
                font = adv
                num = str(abs(cfg.advantage_f))

        n.barlist_1[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 1段目

        # バー２段目
        font = ""
        num = ""

        if n.air_flag.num == 0:  # 地上にいる場合
            num = ""
        elif n.air_flag.num == 255:  # 空中にいる場合:
            num = "^"

        if n.atk.num != 0:  # 攻撃判定を出しているとき
            font = atk
            num = str(n.active)
            if n.air_flag.num == 255:  # 空中にいる場合:
                font += "\x1b[4m"

        n.barlist_2[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 2段目

        num = str(n.motion_type.num)
        n.barlist_3[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 3段目

        num = str(n.noguard.num)
        n.barlist_4[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 4段目

        num = str(n.ignore_flag)
        n.barlist_5[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 5段目

        num = str(n.action_flag)
        n.barlist_6[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 6段目

        num = str(n.motion_chenge_flag)
        n.barlist_7[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF  # 6段目


def bar_ini():
    cfg.reset_flag = 1

    cfg.p1.bar_1 = ""
    cfg.p2.bar_1 = ""
    cfg.p3.bar_1 = ""
    cfg.p4.bar_1 = ""

    cfg.p1.bar_2 = ""
    cfg.p2.bar_2 = ""
    cfg.p3.bar_2 = ""
    cfg.p4.bar_2 = ""

    cfg.p1.bar_3 = ""
    cfg.p2.bar_3 = ""
    cfg.p3.bar_3 = ""
    cfg.p4.bar_3 = ""

    cfg.p1.bar_4 = ""
    cfg.p2.bar_4 = ""
    cfg.p3.bar_4 = ""
    cfg.p4.bar_4 = ""

    cfg.p1.bar_5 = ""
    cfg.p2.bar_5 = ""
    cfg.p3.bar_5 = ""
    cfg.p4.bar_5 = ""

    cfg.p1.bar_6 = ""
    cfg.p2.bar_6 = ""
    cfg.p3.bar_6 = ""
    cfg.p4.bar_6 = ""

    cfg.p1.bar_7 = ""
    cfg.p2.bar_7 = ""
    cfg.p3.bar_7 = ""
    cfg.p4.bar_7 = ""

    cfg.st_bar = ""
    cfg.bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.bar80_flag = 0
    cfg.interval_time = 80

    for n in range(cfg.bar_range):
        cfg.p1.barlist_1[n] = ""
        cfg.p2.barlist_1[n] = ""
        cfg.p3.barlist_1[n] = ""
        cfg.p4.barlist_1[n] = ""

        cfg.p1.barlist_2[n] = ""
        cfg.p2.barlist_2[n] = ""
        cfg.p3.barlist_2[n] = ""
        cfg.p4.barlist_2[n] = ""

        cfg.p1.barlist_3[n] = ""
        cfg.p2.barlist_3[n] = ""
        cfg.p3.barlist_3[n] = ""
        cfg.p4.barlist_3[n] = ""

        cfg.p1.barlist_4[n] = ""
        cfg.p2.barlist_4[n] = ""
        cfg.p3.barlist_4[n] = ""
        cfg.p4.barlist_4[n] = ""

        cfg.p1.barlist_5[n] = ""
        cfg.p2.barlist_5[n] = ""
        cfg.p3.barlist_5[n] = ""
        cfg.p4.barlist_5[n] = ""

        cfg.p1.barlist_6[n] = ""
        cfg.p2.barlist_6[n] = ""
        cfg.p3.barlist_6[n] = ""
        cfg.p4.barlist_6[n] = ""

        cfg.p1.barlist_7[n] = ""
        cfg.p2.barlist_7[n] = ""
        cfg.p3.barlist_7[n] = ""
        cfg.p4.barlist_7[n] = ""

        cfg.st_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg.p2.hitstop.num != 0 and cfg.p1.act_flag == 0 and cfg.p1.hit.num == 0:
        cfg.p1.first_active = cfg.p1.zen
        cfg.p1.act_flag = 1

    if cfg.p1.hitstop.num != 0 and cfg.p2.act_flag == 0 and cfg.p2.hit.num == 0:
        cfg.p2.first_active = cfg.p2.zen
        cfg.p2.act_flag = 1

    if cfg.p1.motion.num == 0 and cfg.p1.atk.num == 0:
        cfg.p1.act_flag = 0

    if cfg.p2.motion.num == 0 and cfg.p2.atk.num == 0:
        cfg.p2.act_flag = 0


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg.p1.x_posi.num).rjust(8, " ")
    x_p2 = str(cfg.p2.x_posi.num).rjust(8, " ")
    act_P1 = str(cfg.p1.first_active).rjust(3, " ")
    act_P2 = str(cfg.p2.first_active).rjust(3, " ")
    zen_P1 = str(cfg.p1.zen).rjust(3, " ")
    zen_P2 = str(cfg.p2.zen).rjust(3, " ")
    gauge_p1 = str('{:.02f}'.format(cfg.p1.gauge.num / 100)).rjust(7, " ")
    gauge_p2 = str('{:.02f}'.format(cfg.p2.gauge.num / 100)).rjust(7, " ")
    m_gauge_p1 = str('{:.02f}'.format(cfg.p1.moon.num / 100)).rjust(7, " ")
    m_gauge_p2 = str('{:.02f}'.format(cfg.p2.moon.num / 100)).rjust(7, " ")

    ukemi = str(cfg.ukemi.num).rjust(3, " ")
    ukemi2 = str(0).rjust(3, " ")

    if cfg.p2.ukemi2.num != 0:
        ukemi2 = str(cfg.p2.ukemi2.num + 1).rjust(3, " ")

    advantage_f = str(cfg.advantage_f).rjust(7, " ")

    hosei = str(cfg.hosei.num).rjust(4, " ")

    kyori = cfg.p1.x_posi.num - cfg.p2.x_posi.num

    # damage = cfg.damage
    # kouritu = "0".rjust(8, " ")
    # # if damage != 0:
    # #     kouritu = damage / (100 - cfg.hosei)
    # #     kouritu = str('{:.02f}'.format(kouritu)).rjust(8, " ")

    cfg.p1.bar_1 = ""
    cfg.p2.bar_1 = ""
    cfg.p3.bar_1 = ""
    cfg.p4.bar_1 = ""

    cfg.p1.bar_2 = ""
    cfg.p2.bar_2 = ""
    cfg.p3.bar_2 = ""
    cfg.p4.bar_2 = ""

    cfg.p1.bar_3 = ""
    cfg.p2.bar_3 = ""
    cfg.p3.bar_3 = ""
    cfg.p4.bar_3 = ""

    cfg.p1.bar_4 = ""
    cfg.p2.bar_4 = ""
    cfg.p3.bar_4 = ""
    cfg.p4.bar_4 = ""

    cfg.p1.bar_5 = ""
    cfg.p2.bar_5 = ""
    cfg.p3.bar_5 = ""
    cfg.p4.bar_5 = ""

    cfg.p1.bar_6 = ""
    cfg.p2.bar_6 = ""
    cfg.p3.bar_6 = ""
    cfg.p4.bar_6 = ""

    cfg.p1.bar_7 = ""
    cfg.p2.bar_7 = ""
    cfg.p3.bar_7 = ""
    cfg.p4.bar_7 = ""

    cfg.st_bar = ""

    temp = cfg.bar_num

    for n in range(cfg.bar_range):
        temp += 1
        if temp == cfg.bar_range:
            temp = 0
        cfg.p1.bar_1 += cfg.p1.barlist_1[temp]
        cfg.p2.bar_1 += cfg.p2.barlist_1[temp]
        cfg.p3.bar_1 += cfg.p3.barlist_1[temp]
        cfg.p4.bar_1 += cfg.p4.barlist_1[temp]

        cfg.p1.bar_2 += cfg.p1.barlist_2[temp]
        cfg.p2.bar_2 += cfg.p2.barlist_2[temp]
        cfg.p3.bar_2 += cfg.p3.barlist_2[temp]
        cfg.p4.bar_2 += cfg.p4.barlist_2[temp]

        cfg.p1.bar_3 += cfg.p1.barlist_3[temp]
        cfg.p2.bar_3 += cfg.p2.barlist_3[temp]
        cfg.p3.bar_3 += cfg.p3.barlist_3[temp]
        cfg.p4.bar_3 += cfg.p4.barlist_3[temp]

        cfg.p1.bar_4 += cfg.p1.barlist_4[temp]
        cfg.p2.bar_4 += cfg.p2.barlist_4[temp]
        cfg.p3.bar_4 += cfg.p3.barlist_4[temp]
        cfg.p4.bar_4 += cfg.p4.barlist_4[temp]

        cfg.p1.bar_5 += cfg.p1.barlist_5[temp]
        cfg.p2.bar_5 += cfg.p2.barlist_5[temp]
        cfg.p3.bar_5 += cfg.p3.barlist_5[temp]
        cfg.p4.bar_5 += cfg.p4.barlist_5[temp]

        cfg.p1.bar_6 += cfg.p1.barlist_6[temp]
        cfg.p2.bar_6 += cfg.p2.barlist_6[temp]
        cfg.p3.bar_6 += cfg.p3.barlist_6[temp]
        cfg.p4.bar_6 += cfg.p4.barlist_6[temp]

        cfg.p1.bar_7 += cfg.p1.barlist_7[temp]
        cfg.p2.bar_7 += cfg.p2.barlist_7[temp]
        cfg.p3.bar_7 += cfg.p3.barlist_7[temp]
        cfg.p4.bar_7 += cfg.p4.barlist_7[temp]

        cfg.st_bar += cfg.st_barlist[temp]

    if kyori < 0:
        kyori = kyori * -1
    # kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += f'1P|Position{x_p1}'
    state_str += f' FirstActive{act_P1}'
    state_str += f' Overall{zen_P1}'
    state_str += f' Circuit{gauge_p1}%'
    state_str += f' Moon{m_gauge_p1}%'

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

    state_str += f'2P|Position{x_p2}'
    state_str += f' FirstActive{act_P2}'
    state_str += f' Overall{zen_P2}'
    state_str += f' Circuit{gauge_p2}%'
    state_str += f' Moon{m_gauge_p2}%' + END

    state_str += '  |Advantage' + advantage_f
    state_str += ' Proration' + hosei + "%"
    state_str += ' Untec' + ukemi2 + ',' + ukemi
    state_str += '  Range ' + kyori + ' ' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.p1.bar_1 + END
    state_str += '  |' + cfg.p1.bar_2 + END
    state_str += '2P|' + cfg.p2.bar_1 + END
    state_str += '  |' + cfg.p2.bar_2 + END

    if cfg.debug_flag == 1:
        state_str = degug_view(state_str)

    print(state_str)


def degug_view(state_str):
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    debug_str_p1 = ""
    debug_str_p2 = ""

    debug_str_p1 = "timer   " + str(cfg.timer.num).rjust(6, " ")
    debug_str_p2 = "bar_num " + str(cfg.bar_num).rjust(6, " ")

    debug_str_p1 += "motion_type " + str(cfg.p1.motion_type.num).rjust(6, " ")
    debug_str_p2 += "motion_type " + str(cfg.p2.motion_type.num).rjust(6, " ")
    debug_str_p1 += "motion " + str(cfg.p1.motion.num).rjust(6, " ")
    debug_str_p2 += "motion " + str(cfg.p2.motion.num).rjust(6, " ")
    debug_str_p1 += "noguard " + str(cfg.p1.noguard.num).rjust(6, " ")
    debug_str_p2 += "noguard " + str(cfg.p2.noguard.num).rjust(6, " ")
    debug_str_p1 += "motion_chenge_flag " + str(cfg.p1.motion_chenge_flag).rjust(6, " ")
    debug_str_p2 += "motion_chenge_flag " + str(cfg.p2.motion_chenge_flag).rjust(6, " ")
    debug_str_p1 += "ignore_flag " + str(cfg.p1.ignore_flag).rjust(6, " ")
    debug_str_p2 += "ignore_flag " + str(cfg.p2.ignore_flag).rjust(6, " ")
    debug_str_p1 += "action_flag " + str(cfg.p1.action_flag).rjust(6, " ")
    debug_str_p2 += "action_flag " + str(cfg.p2.action_flag).rjust(6, " ")
    debug_str_p1 += "hit " + str(cfg.p1.hit.num).rjust(6, " ")
    debug_str_p2 += "hit " + str(cfg.p2.hit.num).rjust(6, " ")
    debug_str_p1 += "advantage_calc_flag " + str(cfg.advantage_calc_flag).rjust(6, " ")

    # debug_str_p2 += "bar80_flag　　　　　 " + str(cfg.bar80_flag).rjust(6, " ")
    # debug_str_p1 += "interval_time " + str(cfg.interval_time).rjust(6, " ")
    # debug_str_p2 += "interval　　　 " + str(cfg.interval).rjust(6, " ")
    # debug_str_p1 += "bar_flag " + str(cfg.bar_flag).rjust(6, " ")

    # debug_str_p1 += "anten_stop2 " + str(cfg.p1.anten_stop2.num).rjust(6, " ")
    # debug_str_p2 += "anten_stop2 " + str(cfg.p2.anten_stop2.num).rjust(6, " ")

    # debug_str_p1 += "hitstop " + str(cfg.p1.hitstop.num).rjust(6, " ")
    # debug_str_p2 += "hitstop " + str(cfg.p2.hitstop.num).rjust(6, " ")

    # debug_str_p1 += "hitstop_old " + str(cfg.p1.hitstop_old).rjust(6, " ")
    # debug_str_p2 += "hitstop_old " + str(cfg.p2.hitstop_old).rjust(6, " ")
    # debug_str_p1 += "tag_flag " + str(cfg.P1.tag_flag.num).rjust(6, " ")
    # debug_str_p2 += "tag_flag " + str(cfg.P2.tag_flag.num).rjust(6, " ")

    state_str += 'mt|' + cfg.p1.bar_3 + END
    state_str += 'ng|' + cfg.p1.bar_4 + END
    state_str += 'ig|' + cfg.p1.bar_5 + END
    state_str += 'ac|' + cfg.p1.bar_6 + END
    state_str += 'mc|' + cfg.p1.bar_7 + END
    state_str += '  |' + END
    state_str += 'mt|' + cfg.p2.bar_3 + END
    state_str += 'ng|' + cfg.p2.bar_4 + END
    state_str += 'ig|' + cfg.p2.bar_5 + END
    state_str += 'ac|' + cfg.p2.bar_6 + END
    state_str += 'mc|' + cfg.p2.bar_7 + END

    state_str += debug_str_p1 + END
    state_str += debug_str_p2 + END

    return state_str


def determineReset():
    bar_ini_flag = 0

    if cfg.bar80_flag == 1:
        cfg.interval_time = 1

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.bar_flag == 1:
        bar_ini_flag = 1

    cfg.interval2 += 1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()


def timer_check():
    util_sub.para_read(cfg.timer)


def tr_flag_check():
    util_sub.para_read(cfg.tr_flag)


def startposi():
    x_p1 = cfg.p1.x_posi.num
    x_p2 = cfg.p2.x_posi.num

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

    util_sub.w_mem(cfg.start_posi.ad, b_ini_posi_flag)
