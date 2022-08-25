import os
import time
import ctypes
import copy
import keyboard
from Fighting_Game_Indicator import indicator

from mem_access_util import mem_util

import save_tl
import cfg_tl

cfg = cfg_tl
save = save_tl

windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory


def pause():

    # 一時停止
    cfg.game_data.pause.b_dat = b'\x01'
    cfg.game_data.pause.w_mem()


def play():

    # 再生
    cfg.game_data.pause.b_dat = b'\x00'
    cfg.game_data.pause.w_mem()


def tagCharacterCheck(index):


    d1 = cfg.characters_data_list[index].characters_data
    e1 = cfg.characters_data_list[index].characters_elements

    p1 = d1[0]
    p2 = d1[1]
    p3 = d1[2]
    p4 = d1[3]

    e_p1 = e1[0]
    e_p2 = e1[1]
    e_p3 = e1[2]
    e_p4 = e1[3]

    if p1.tag_flag.val == 1:
        cfg.characters_data_list[index].characters_data = [p3, p2, p1, p4]
        cfg.characters_data_list[index].characters_elements = [e_p3, e_p2, e_p1, e_p4]

    if p2.tag_flag.val == 1:
        cfg.characters_data_list[index].characters_data = [p1, p4, p3, p2]
        cfg.characters_data_list[index].characters_elements = [e_p1, e_p4, e_p3, e_p2]


def situationCheck(index):

    data = cfg.game_data

    characters_data = cfg.characters_data_list[index].characters_data

    for n in data.cont_list:
        n.r_mem()


    for character_data in characters_data:
        for n in character_data.cont_list:
            n.r_mem()


def situationMem(index):
    cfg.mem_index = index
    save.game_data = copy.deepcopy(cfg.game_data)  # 状況を記憶
    save.characters_data_list = copy.deepcopy(cfg.characters_data_list)  # 状況を記憶


def situationWrit():
    data = save.game_data

    check_data_list = save.characters_data_list

    d1 = check_data_list[cfg.mem_index].characters_data

    data.cam.w_mem()  # 状況を再現

    for n in d1:
        n.gauge.w_mem()
        n.moon.w_mem()
        n.moon_st.w_mem()
        n.x_posi.w_mem()


def action_element_cre(n1, n2):
    jmp_number = [34, 35, 36, 37]
    jmp2_number = [39, 38, 40]
    # action_element作成
    n1.action_element.val = 0

    if n1.noguard.val == 77:
        n1.action_element.val = 0

    if n1.noguard.val == 0 and n1.motion_type.val != 0:
        n1.action_element.val = 1

    if n1.noguard.val == 77 and n1.motion_chenge_flag == 0 and n1.ignore_flag == 0:  # ジャンプ後即行動対策
        n1.action_element.val = 1

    if n1.noguard.val == 77 and n1.motion_type.val == 21:
        n1.action_element.val = 0

    for list_a in jmp2_number:
        if n1.motion_type.val == list_a:
            for list_b in jmp_number:
                if n2.motion_type.val == list_b:
                    n1.action_element.val = 0

    if n1.motion_type.val == 21 and n2.motion_type.val == 19:  # 吹き飛ばし対策
        n1.action_element.val = 0

    if n1.ignore_flag == 1:
        n1.action_element.val = 0


def old_index_get(index, max_index):

    old_index = index - 1

    if old_index == -1:
        old_index = max_index - 1

    return old_index


def content_creation(current_index):
    tagCharacterCheck(current_index)
    check_data_list = cfg.characters_data_list

    ignore_number = [0, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 44, 594, 596]
    stun_number = [620, 621, 624]
    jmp_number = [34, 35, 36, 37]
    jmp2_number = [39, 38, 40]
    list_len = len(check_data_list)

    old_index_1 = old_index_get(current_index, list_len)
    old_index_2 = old_index_get(old_index_1, list_len)

    d1 = check_data_list[current_index].characters_data
    d2 = check_data_list[old_index_1].characters_data
    d3 = check_data_list[old_index_2].characters_data

    p1 = d1[0]
    p2 = d1[1]
    # p3 = d1[2]
    # p4 = d1[3]

    p1_old = d2[0]
    p2_old = d2[1]

    p1_old2 = d3[0]
    p2_old2 = d3[1]

    # hitstop作成
    if p1.hitstop.val != 0 and p2.hitstop.val != 0:
        cfg.hitstop += 1
    elif p1.hitstop.val == 0 or p2.hitstop.val == 0:
        cfg.hitstop = 0

    # anten作成
    if p1.anten_stop.val == 16:  # 暗転しているとき
        cfg.anten += 1

    elif abs(p2.anten_stop.val) == 128:  # 暗転しているとき
        cfg.anten += 1

    elif p1_old.c_timer.val == p1.c_timer.val and p1.hit.val == 0 and p2.hit.val == 0 and p1.motion_type.val != 621 and p2.motion_type.val != 621:
        cfg.anten += 1

    elif p2_old.c_timer.val == p2.c_timer.val and p2.hit.val == 0 and p1.hit.val == 0 and p1.motion_type.val != 621 and p2.motion_type.val != 621:
        cfg.anten += 1

    elif p1_old.c_timer.val == p1.c_timer.val and p2_old.c_timer.val == p2.c_timer.val and p1.motion_type.val != 621 and p2.motion_type.val != 621:
        cfg.anten += 1

    # elif p2_old.c_timer.val == p2.c_timer.val and p1.motion_type.val != 621 and p2.motion_type.val != 621:
    #     cfg.anten += 1

    else:
        cfg.anten = 0

    if cfg.anten >= 1:
        if p1.anten_stop.val == 16 and p1.noguard.val == 77:  # ムーンドライブ対策
            cfg.anten = 0

        if p1_old2.motion_type.val == 147 or p1_old2.motion_type.val == 148:  # ムーンドライブ対策
            if p2.hit.val != 0:
                if p1_old2.motion_type.val != p1.motion_type.val:
                    cfg.anten = 0

        if abs(p2.anten_stop.val) == 128 and p2.noguard.val == 77:  # ムーンドライブ対策
            cfg.anten = 0

        if p2_old2.motion_type.val == 147 or p2_old2.motion_type.val == 148:  # ムーンドライブ対策
            if p1.hit.val != 0:
                if p2_old2.motion_type.val != p2.motion_type.val:
                    cfg.anten = 0

    if cfg.anten >= 2 or cfg.hitstop >= 2:
        cfg.stop_flag = 1

    else:
        cfg.stop_flag = 0

    for n1, n2, n3 in zip(d1, d2, d3):
        n1.overall = n2.overall
        n1.first_active = n2.first_active
        n1.active = n2.active
        n1.act_flag = n2.act_flag
        n1.koutyoku_f = n2.koutyoku_f
        n1.stun_f = n2.stun_f
        n1.jmp_f = n2.jmp_f
        n1.inv_f = n2.inv_f
        n1.hitstop_f = n2.hitstop_f

        n1.motion.val = 256 - n1.motion.val
        if n1.motion.val == 256:
            n1.motion.val = 0

        if n1.hitstop.val == 65536:
            n1.hitstop.val = 0

        for m in n1.elements:
            if n1.motion.val != 0:
                m.num = n1.motion.val
            else:
                m.num = n1.motion_type.val

        if cfg.stop_flag != 0:
            n1.hitstop_element.val = 1
            n1.hitstop_f += 1
            n1.hitstop_element.num = n1.hitstop_f
        else:
            n1.hitstop_element.val = 0
            n1.hitstop_element.num = 0
            n1.hitstop_f = 0

        # motion_chenge_flag作成
        n1.motion_chenge_flag = 0

        if n1.motion_type.val == n2.motion_type.val or (n1.motion.val == n2.motion.val + 1 and n2.motion.val != 0):
            n1.motion_chenge_flag += 1
        else:
            n1.motion_chenge_flag = 0

        if n2.motion.val != 0:
            if n1.motion.val == 0:  # !0→0
                n1.motion_chenge_flag = 0
            elif n1.motion.val == 1:  # !0→1
                n1.motion_chenge_flag = 0

        elif n2.motion.val == 0:
            if n1.motion.val == 1:  # 0→1
                n1.motion_chenge_flag = 0
            elif n1.motion.val == 0:  # 0→0
                if n2.motion_type.val != n1.motion_type.val:
                    n1.motion_chenge_flag = 0

        # ignore_flag作成
        n1.ignore_flag = 0

        for list_a in ignore_number:
            if n1.motion_type.val == list_a:
                n1.ignore_flag = 1
                break

        action_element_cre(n1, n2)

        # jmp_element作成
        n1.jmp_element.val = 0

        if n1.action_element.val == 1:
            for list_a in jmp_number:  # ジャンプ移行中
                if n1.motion_type.val == list_a:
                    n1.jmp_element.val = 1

            for list_a in jmp2_number:  # ジャンプ２
                if n1.motion_type.val == list_a:
                    n1.jmp_element.val = 1

        if n1.jmp_element.val == 1:
            n1.jmp_f += 1
            n1.jmp_element.num = n1.jmp_f
        else:
            n1.jmp_f = 0
            n1.jmp_element.num = 0

        # atk_element作成
        n1.atk_element.val = 0
        if n1.atk.val != 0:  # 攻撃判定を出しているとき
            n1.atk_element.val = 1

        # 攻撃判定持続計算
        if n1.atk_element.val == 1 and cfg.anten == 0 and cfg.hitstop == 0 and n1.c_timer.val != n2.c_timer.val:  # 攻撃判定を出しているとき
            if n1.hitstop_element.val == 0:
                n1.active += 1

        elif n1.atk_element.val == 0:  # 攻撃判定を出してないとき
            n1.active = 0

        n1.atk_element.num = n1.active

        if n1.active == 0:
            n1.atk_element.num = ""

        # stun_element作成
        n1.grd_stun_element.val = 0
        n1.hit_stun_element.val = 0

        if n1.hit.val != 0:  # ガードorヒット硬直中
            n1.grd_stun_element.val = 1
            n1.hit_stun_element.val = 1
        else:
            n1.hit_stun_element.num = 0
            n1.grd_stun_element.val = 0

        for list_a in stun_number:  # ガードorヒット硬直中
            if n1.motion_type.val == list_a:
                n1.grd_stun_element.val = 1
                n1.hit_stun_element.val = 1

        if n1.hit_stun_element.val == 1:
            if cfg.stop_flag == 0:
                n1.stun_f += 1
            elif cfg.stop_flag == 1:
                n1.stun_f = 0
            else:
                n1.stun_f += 0
            n1.hit_stun_element.num = n1.stun_f
        else:
            n1.stun_f = 0

        # inv_element作成
        n1.inv_element.val = 0

        if n1.inv.val == 0 and n1.motion.val != 0:  # 無敵中 # バックステップ無敵中# ムーンドライブ無敵
            n1.inv_element.val = 1

        if n1.step_inv.val != 0 and n1.motion_type.val == 46:
            n1.inv_element.val = 1

        if n1.air_ukemi_1.val != 0 and n1.air_ukemi_2.val != 0 and n1.hit_stun_element.val == 0:
            n1.inv_element.val = 1

        if n1.motion_type.val == 147 or n1.motion_type.val == 148:
            if n1.action_element.val == 1:
                n1.inv_element.val = 1

        if n1.inv_element.val == 1:
            if cfg.stop_flag == 0:
                n1.inv_f += 1
                n1.inv_element.num = n1.inv_f
            else:
                n1.inv_f += 0
                n1.inv_element.num = n1.inv_f
        else:
            n1.inv_f = 0
            n1.inv_element.num = 0

        # wake_up_element作成
        n1.wake_up_element.val = 0

        if n1.motion_type.val == 593:
            n1.wake_up_element.val = 1
            n1.wake_up_element.num = 0
        # air_element作成
        n1.air_element.val = 0
        if n1.air.val == 255:  # 空中にいる場合:
            n1.air_element.val = 1
            n1.air_element.num = "^"

        # seeld_element作成
        n1.seeld_element.val = 0
        if n1.seeld.val == 2 or n1.seeld.val == 3:  # シールド中
            n1.seeld_element.val = 1

        # bunker_element作成
        n1.bunker_element.val = 0

        if (n1.action_element.val == 1 and
            n1.motion.val == 0 and
            n1.inv_element.val == 0 and
            n1.jmp_element.val == 0 and
                n1.seeld_element.val == 0):

            n1.koutyoku_element.val = 1
            n1.koutyoku_f += 1
            n1.koutyoku_element.num = n1.koutyoku_f
        else:
            n1.koutyoku_element.val = 0
            n1.koutyoku_element.num = 0
            n1.koutyoku_f = 0

        if cfg.debug_flag == 1:
            n1.line_3_element.num = n1.motion_type.val
            n1.line_4_element.num = n1.motion.val
            n1.line_5_element.num = n1.noguard.val
            n1.line_6_element.num = n1.action_element.val
            n1.line_7_element.num = n1.c_timer.val
            n1.line_8_element.num = n1.ignore_flag
            n1.line_9_element.num = n1.hit.val
            n1.line_10_element.num = n1.motion_chenge_flag

    # 技の発生フレームの取得
    firstActive_calc(p1, p2, p1_old, p2_old)

    # 全体フレームの取得
    overall_calc(p1, p2)

    # 硬直差の取得
    advantage_calc(p1, p2)

    if cfg.advantage_calc_flag == 1:
        p1.adv_element.val = 1
        p1.adv_element.num = abs(cfg.advantage_f)

        p2.adv_element.val = 1
        p2.adv_element.num = abs(cfg.advantage_f)
    elif cfg.advantage_calc_flag == 0:
        p1.adv_element.val = 0
        p1.adv_element.num = 0

        p2.adv_element.val = 0
        p2.adv_element.num = 0

    # p3.adv_element.num = ""
    # p4.adv_element.num = ""


def advantage_calc(p1, p2):

    if p1.hit.val == 0 and p2.hit.val == 0 and p1.action_element.val == 0 and p2.action_element.val == 0:
        cfg.advantage_calc_flag = 0

    elif (p1.hit.val != 0 or p1.action_element.val == 1) and (p2.hit.val != 0 or p2.action_element.val == 1):
        cfg.advantage_calc_flag = 1
        cfg.advantage_f = 0

    if cfg.advantage_calc_flag == 1:

        # 有利フレーム検証
        if (p1.hit.val == 0 and p1.action_element.val == 0) and (p2.hit.val != 0 or p2.action_element.val == 1):
            cfg.advantage_f += 1

        # 不利フレーム検証
        if (p1.hit.val != 0 or p1.action_element.val == 1) and (p2.hit.val == 0 and p2.action_element.val == 0):
            cfg.advantage_f -= 1


def overall_calc(p1, p2):

    if p1.motion.val != 0:  # 全体フレームの取得
        p1.overall = p1.motion.val

    if p2.motion.val != 0:
        p2.overall = p2.motion.val


def firstActive_calc(p1, p2, p1_old, p2_old):
    # 計測開始の確認
    if p2.hitstop.val != 0 and p1.act_flag == 0 and p1.hit.val == 0:
        p1.first_active = p1_old.overall
        p1.act_flag = 1

    if p1.hitstop.val != 0 and p2.act_flag == 0 and p2.hit.val == 0:
        p1.first_active = p2_old.overall
        p2.act_flag = 1

    if p1.motion.val == 0 and p1.atk.val == 0 and p2.grd_stun_element.val == 0:
        p1.act_flag = 0

    if p2.motion.val == 0 and p2.atk.val == 0 and p1.grd_stun_element.val == 0:
        p2.act_flag = 0


def cursor_move(line, index):
    return "\x1b[" + str(line) + ";" + str(index) + "H"


def template_view():
    state_str = ""
    if cfg.template_view_flag == 0:
        cfg.template_view_flag = 1

        fini = '\x1b[0m'

        #                                        10        20        30        40        50        60        70        80        90       100
        #                               123456789112345678921234567893123456789412345678951234567896123456789712345678981234567899123456789912345678991
        state_str += cursor_move(1, 3) + '|firstAct|adv|proration|  untec|  range|position -000000|circuit 000.00%|moon 000.00%|speed x 0000|y 0000|health 00000|'
        state_str += cursor_move(2, 3) + '|      00|-00|     000%|000,000| 000000|         -000000|        000.00%|     000.00%|        0000|  0000|       00000|'

        state_str += cursor_move(1, 122)
        state_str += 'motion ' + cfg.G_mot + '01' + fini
        state_str += '  atk ' + cfg.G_atk + '01' + fini
        state_str += '  stun ' + cfg.G_grd_stun + '01' + fini
        state_str += '  jmp ' + cfg.G_jmp + '01' + fini
        state_str += ' air ' + '01' + fini

        state_str += cursor_move(2, 122)
        state_str += ' seeld ' + cfg.G_seeld + '01' + fini
        state_str += '  inv ' + cfg.G_inv + '01' + fini
        state_str += '  stop ' + cfg.G_hit_stop + '01' + fini

        state_str += '              ^'

    return state_str


def view(view_data, debug_data, current_index):
    DEF = '\x1b[0m'
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    state_str = '\x1b[1;1H' + '\x1b[?25l'

    if cfg.light_mode_flag == 0:
        state_str += template_view()

        data = cfg.game_data
        d1 = cfg.characters_data_list[current_index].characters_data
        p1 = d1[0]
        p2 = d1[1]

        state_str += cursor_move(2, 10) + str(p1.first_active).rjust(2, " ")
        state_str += cursor_move(2, 13) + str(cfg.advantage_f).rjust(3, " ")
        state_str += cursor_move(2, 22) + str(data.hosei.val).rjust(3, " ")

        state_str += cursor_move(2, 27) + str(data.ukemi.val).rjust(3, " ")

        if p2.ukemi2.val != 0:
            state_str += cursor_move(2, 31) + str(p2.ukemi2.val + 1).rjust(3, " ")
        Range = p1.x_posi.val - p2.x_posi.val

        state_str += cursor_move(2, 36) + str(abs(Range)).rjust(6, " ")
        state_str += cursor_move(1, 52) + str(p1.x_posi.val).rjust(7, " ")
        state_str += cursor_move(2, 52) + str(p2.x_posi.val).rjust(7, " ")
        state_str += cursor_move(1, 68) + str('{:.02f}'.format(p1.gauge.val / 100)).rjust(6, " ")
        state_str += cursor_move(2, 68) + str('{:.02f}'.format(p2.gauge.val / 100)).rjust(6, " ")
        state_str += cursor_move(1, 81) + str('{:.02f}'.format(p1.moon.val / 100)).rjust(6, " ")
        state_str += cursor_move(2, 81) + str('{:.02f}'.format(p2.moon.val / 100)).rjust(6, " ")

        state_str += cursor_move(1, 96) + str(abs(p1.x_speed.val)).rjust(5, " ")
        state_str += cursor_move(2, 96) + str(abs(p2.x_speed.val)).rjust(5, " ")
        state_str += cursor_move(1, 103) + str(p1.y_speed.val).rjust(5, " ")
        state_str += cursor_move(2, 103) + str(p2.y_speed.val).rjust(5, " ")
        state_str += cursor_move(1, 116) + str(p1.health.val).rjust(5, " ")
        state_str += cursor_move(2, 116) + str(p2.health.val).rjust(5, " ")

        # state_str += cursor_move(2, 4) + str(cfg.loop_num).rjust(4, " ")

        state_str += cursor_move(3, 1) + view_data
    elif cfg.light_mode_flag == 1:
        cfg.template_view_flag = 0
        state_str += cursor_move(1, 1) + view_data

    if cfg.debug_flag == 1:
        state_str += debug_data

    state_str += "\x1b[1;1H"
    print(state_str)


def degug_view(debug_data):
    print(debug_data)


def moon_change():

    characters_data = cfg.characters_data_list[0].characters_data
    p1 = characters_data[0]
    p2 = characters_data[1]

    for n in characters_data:
        n.moon.b_dat = b'\x10\x27'
        n.moon.w_mem()

    if p1.moon_st.val == 0:
        p1.moon_st.b_dat = b'\x01'
        p1.moon_st.w_mem()

        p2.moon_st.b_dat = b'\x01'
        p2.moon_st.w_mem()

    elif p1.moon_st.val == 1:
        p1.moon_st.b_dat = b'\x00'
        p1.moon_st.w_mem()

        p2.moon_st.b_dat = b'\x00'
        p2.moon_st.w_mem()


def max_damage_ini():

    addres = cfg.game_data.max_damage_pointer.val + 0x1C + 0x24

    mem_util.w_mem_abs_addres(addres, b'\x01')


def function_key(data_index):

    # セーブデータリセット
    if keyboard.is_pressed("F1"):
        if cfg.on_flag == 0:
            cfg.on_flag = 1
            cfg.save_flag = 0

    # 状況記憶
    elif keyboard.is_pressed("F2"):
        if cfg.on_flag == 0:
            cfg.save_flag = 1
            cfg.on_flag = 1
            pause()
            situationMem(data_index)

    # # 月切り替え
    # elif keyboard.is_pressed("F12"):
    #     if cfg.on_flag == 0:
    #         cfg.on_flag = 1
    #         moon_change()

    # 簡易表示切り替え
    elif keyboard.is_pressed("F3"):
        if cfg.on_flag == 0:
            cfg.on_flag = 1
            cfg.debug_flag = 0
            if cfg.light_mode_flag == 0:
                cfg.light_mode_flag = 1
                os.system('cls')
                os.system('mode con: cols=164 lines=5')

            elif cfg.light_mode_flag == 1:
                cfg.light_mode_flag = 0
                os.system('cls')
                os.system('mode con: cols=164 lines=7')

    # 最大ダメージ初期化
    elif keyboard.is_pressed("F4"):
        if cfg.on_flag == 0:
            cfg.on_flag = 1
            max_damage_ini()

    # デバッグ表示
    elif (keyboard.is_pressed("9")) and (keyboard.is_pressed("0")):
        if cfg.debug_flag == 0:
            cfg.debug_flag = 1
            cfg.template_view_flag = 0
            os.system('mode con: cols=180 lines=30')

        elif cfg.debug_flag == 1:
            cfg.debug_flag = 0
            cfg.template_view_flag = 0
            os.system('mode con: cols=165 lines=8')
        time.sleep(0.3)

    elif cfg.on_flag == 1:
        cfg.on_flag = 0
        play()


def startposi(current_index):
    data = save.game_data
    d1 = save.characters_data_list[cfg.mem_index].characters_data

    x_p1 = d1[0].x_posi.val
    x_p2 = d1[1].x_posi.val

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

    data.start_posi.b_dat = b_ini_posi_flag
    data.start_posi.w_mem()
