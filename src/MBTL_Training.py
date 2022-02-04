from ctypes import windll
from struct import unpack
import os
import time
import keyboard

import ad_ml
import cfg_ml
import sub_ml

cfg = cfg_ml
sub = sub_ml

sub.ex_cmd_enable()
os.system('mode con: cols=166 lines=10')
os.system('cls')
os.system('title MBTL_Training 1.4')
print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
save_flag = 0
flag1 = 0
start_time = time.time()

###############################################################
# メイン関数
###############################################################

while 1:
    time.sleep(0.003)

    # トレーニングモードチェック
    sub.tr_flag_check()
    if unpack('l', cfg.b_tr_flag)[0] == 300:
    # if 1:

        # セーブデータリセット
        if keyboard.is_pressed("F1"):
            if flag1 == 0:
                flag1 = 1
                save_flag = 0

        # 状況記憶
        elif keyboard.is_pressed("F2"):
            if flag1 == 0:
                sub.pause()
                sub.situationMem()
                save_flag = 1
                flag1 = 1

        # 月切り替え
        elif keyboard.is_pressed("F3"):
            if flag1 == 0:
                flag1 = 1
                sub.moon_change()

        # 最大ダメージ初期化
        elif keyboard.is_pressed("F4"):
            if flag1 == 0:
                flag1 = 1
                sub.MAX_Damage_ini()

        elif flag1 == 1:
            flag1 = 0
            sub.play()

        # タイマーチェック
        sub.timer_check()

        # フレームの切り替わりを監視
        if (cfg.f_timer != cfg.f_timer2):

            cfg.f_timer2 = cfg.f_timer

            time.sleep(0.001)

            # 各種数値の取得
            sub.situationCheck()

            # 各種数値の取得
            sub.get_values()

            # ゲーム状況の取得
            sub.view_st()
            sub.view()

            if save_flag == 1:
                # リセット時の開始位置固定化
                sub.startposi()

            if cfg_ml.f_timer <= 1:
                sub.bar_ini()

                if save_flag == 1:
                    # 状況再現
                    sub.situationWrit()
