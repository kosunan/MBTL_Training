from ctypes import windll
from struct import unpack
import os
import time
import keyboard

import cfg_tl
import sub_tl
import util_sub

cfg = cfg_tl
sub = sub_tl
util_sub.ex_cmd_enable()

os.system('mode con: cols=166 lines=10')

os.system('cls')
os.system('title MBTL_Training 1.8.1')
print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
save_flag = 0
flag1 = 0
start_time = time.time()

def function_key():
    global flag1
    global save_flag

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

    # デバッグ表示
    elif (keyboard.is_pressed("9"))and(keyboard.is_pressed("0")):
        if cfg.debug_flag == 0:
            cfg.debug_flag = 1
            os.system('mode con: cols=180 lines=23')

        elif cfg.debug_flag == 1:
            cfg.debug_flag = 0
            os.system('mode con: cols=166 lines=10')

        time.sleep(0.3)

    elif flag1 == 1:
        flag1 = 0
        sub.play()
###############################################################
# メイン関数
###############################################################
# ベースアドレス取得
res = util_sub.get_connection("MBTL.exe")
cfg.pid = res[0]
cfg.h_pro = res[1]
cfg.base_ad = res[2]


while 1:
    time.sleep(0.003)

    # トレーニングモードチェック
    sub.tr_flag_check()

    # トレーニングモードではない場合
    if cfg.tr_flag.num != 300:
        print("Waiting for training mode to start ")
        time.sleep(0.2)
        os.system('cls')

    # トレーニングモードの場合
    elif cfg.tr_flag.num == 300:
        function_key()
        # タイマーチェック
        sub.timer_check()

        # フレームの切り替わりを監視
        if (cfg.timer_old != cfg.timer.num):

            cfg.timer_old = cfg.timer.num
            time.sleep(0.001)

            # 各種数値の取得
            sub.situationCheck()


            # ゲーム状況の取得
            sub.view_st()

            if save_flag == 1:
                # リセット時の開始位置固定化
                sub.startposi()

            if cfg.timer.num <= 1:
                sub.bar_ini()

                if save_flag == 1:
                    # 状況再現
                    sub.situationWrit()
        sub.view()
