from ctypes import windll
from struct import unpack
import os

import time
import keyboard
import ad_ml

import cfg_ml
import sub_ml

sub_ml.ex_cmd_enable()
os.system('mode con: cols=166 lines=9')
os.system('cls')

print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
save_flag = 0
f_timer = 0
flag1 = 0

###############################################################
# メイン関数
###############################################################

start_time = time.time()
# sub_ml.pidget()

long_x = 0
while 1:
    time.sleep(0.001)

    # 各種数値の取得
    sub_ml.situationCheck()
    # 各種数値の取得
    sub_ml.get_values()

    if unpack('b', cfg_ml.b_tr_flag)[0] == 44:

        # フレームの切り替わりを監視
        if cfg_ml.f_timer != cfg_ml.f_timer2:
            cfg_ml.f_timer2 = cfg_ml.f_timer
            cfg_ml.kaisuu = 0

        elif cfg_ml.f_timer == cfg_ml.f_timer2:
            cfg_ml.kaisuu += 1

        if cfg_ml.kaisuu == 6:
            # ゲーム状況の取得
            sub_ml.view_st()

        sub_ml.view()

        f_timer = cfg_ml.f_timer

        # 状況記憶
        if keyboard.is_pressed("F2"):
            if flag1 == 0:
                sub_ml.pause()
                time.sleep(1)
                sub_ml.situationMem()
                save_flag = 1
                flag1 = 1
        # 状況再現
        elif keyboard.is_pressed("F4"):
            if flag1 == 0:
                sub_ml.bar_ini()
                print("1")
                sub_ml.pause()
                time.sleep(1)
                sub_ml.situationWrit()
                flag1 = 1
        # # ダミー自動リセット
        # elif cfg_ml.dmy_timer >= cfg_ml.dmyend_timer and cfg_ml.hit_p2 != 0:
        #     sub_ml.situationWrit()

        # moon切り替え
        elif keyboard.is_pressed("F3"):
            if flag1 == 0:
                flag1 = 1
                sub_ml.moon_change()

        elif flag1 == 1:
            flag1 = 0
            sub_ml.play()
