from ctypes import windll
from struct import unpack
import os
import time
import keyboard

from Fighting_Game_Indicator import indicator
from mem_access_util import mem_util

import cfg_tl
import sub_tl
import util_sub

cfg = cfg_tl
sub = sub_tl

windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする
indicator.ex_cmd_enable()
os.system('mode con: cols=166 lines=10')
os.system('cls')
os.system('title MBTL_Training 1.8.1')
print('\x1b[1;1H' + '\x1b[?25l')

# ベースアドレス取得
mem_util.get_connection("MBTL.exe")

data_index = 0
# check_data格納用オブジェクト作成
cfg.game_data = cfg.Game_Data_Class()
for n in range(3):  # 3フレーム分のデータ格納領域作成
    cfg.characters_data_list.append(cfg.Characters_Data_Class())

list_len = len(cfg.characters_data_list)
timer = 0
timer_old = 0
tr_flag = 0

while 1:
    time.sleep(0.001)

    # トレーニングモードチェック
    tr_flag = cfg.game_data.tr_flag.r_mem()

    # トレーニングモードではない場合
    if tr_flag != 300:
        print("Waiting for training mode to start ")
        time.sleep(0.5)
        os.system('cls')

    # トレーニングモードの場合
    elif tr_flag == 300:
        sub.function_key(data_index)

        # タイマーチェック
        timer = cfg.game_data.timer.r_mem()

        # フレームの切り替わりを監視
        if timer != timer_old:
            timer_old = timer
            time.sleep(0.006)  # データが安定するまで待機

            sub.situationCheck(data_index)  # 各種数値の取得

            sub.content_creation(data_index)  # 各種データ作成
            characters_elements = cfg.characters_data_list[data_index].characters_elements

            view_data = indicator.frame_circulation_indicator(characters_elements, cfg.stop_flag)

            sub.view(view_data, data_index)
            # print('\x1b[1;1H' + '\x1b[?25l'+view_data)
            if cfg.save_flag == 1:
                # リセット時の開始位置固定化
                sub.startposi(data_index)

            if timer <= 1:
                indicator.bar_ini()
                if cfg.save_flag == 1:
                    sub.situationWrit()  # 状況再現

            data_index += 1

            if data_index == list_len:
                data_index = 0
