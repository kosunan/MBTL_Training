from ctypes import windll
import os
import time
import subprocess
import pygetwindow as gw


from Fighting_Game_Indicator import indicator
from mem_access_util import mem_util

import cfg_tl
import sub_tl

cfg = cfg_tl
sub = sub_tl

windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする
indicator.ex_cmd_enable()

# 画面をクリアする
subprocess.run("cls", shell=True)


# タイトルを設定する
title = "MBTL_Training 1.12.1"
subprocess.run("title "+title, shell=True)

# タイトルに合致するウィンドウを取得するまで待機
max_attempts = 100  # 最大試行回数
attempt = 0
cmd_window = None

while attempt < max_attempts:
    cmd_window = gw.getWindowsWithTitle(title)
    if cmd_window:
        cmd_window = cmd_window[0]  # リストからウィンドウを取得
        break
    else:
        attempt += 1
        time.sleep(0.1)  # 0.1秒待機して再試行

# ウィンドウが見つかった場合にサイズを設定
if cmd_window:
    time.sleep(0.1)
    def resize_windows_with_title(title, width, height):
        # 指定したタイトルを持つすべてのウィンドウを取得
        windows = gw.getWindowsWithTitle(title)
        
        if windows:
            for window in windows:
                # ウィンドウのサイズを変更
                window.resizeTo(width, height)

    # タイトルと変更後の幅・高さを指定してウィンドウのサイズを変更
    title_to_resize = title
    new_width = 1525  # 変更後の幅
    new_height = 200  # 変更後の高さ

    resize_windows_with_title(title_to_resize, new_width, new_height)



# ベースアドレス取得 # Get base address
mem_util.get_connection("MBTL.exe")
mem_util.changeFontSize(7, 14)

data_index = 0
# check_data格納用オブジェクト作成 # Create storage object
cfg.game_data = cfg.Game_Data_Class()
for n in range(3):  # 3フレーム分のデータ格納領域作成 # Create data storage area for 3 frames
    cfg.characters_data_list.append(cfg.Characters_Data_Class())

list_len = len(cfg.characters_data_list)
timer = 0
timer_old = 0
tr_flag = 0

while True:

    time.sleep(0.001)

    # トレーニングモードチェック # Training mode check
    tr_flag = cfg.game_data.tr_flag.r_mem()

    # トレーニングモードではない場合
    if tr_flag != 300 and tr_flag != 103:
        print("Waiting for training mode to start ")
        time.sleep(0.5)
        os.system("cls")
        cfg.save_flag = 0

    # トレーニングモードの場合
    elif tr_flag == 300 or tr_flag == 103:
        sub.function_key(data_index)

        # タイマーチェック
        timer = cfg.game_data.timer.r_mem()
        # timer_2 = cfg.game_data.timer_2.r_mem()

        # cfg.loop_num += 1

        # フレームの切り替わりを監視
        if timer != timer_old:
            timer_old = timer
            time.sleep(0.009)  # データが安定するまで待機

            sub.situationCheck(data_index)  # 各種数値の取得

            sub.content_creation(data_index)  # 各種データ作成
            characters_elements = cfg.characters_data_list[
                data_index
            ].characters_elements
            characters_debug_elements = cfg.characters_data_list[
                data_index
            ].characters_debug_elements

            view_data, debug_data = indicator.frame_circulation_indicator(
                characters_elements,
                characters_debug_elements,
                cfg.stop_flag,
                cfg.debug_flag,
            )

            sub.view(view_data, debug_data, data_index)
            # cfg.loop_num = 0
            if cfg.save_flag == 1:
                # リセット時の開始位置固定化
                sub.startposi(data_index)

            if timer <= 3:
                indicator.bar_ini()
                if cfg.save_flag == 1:
                    sub.situationWrit()  # 状況再現

            data_index += 1

            if data_index == list_len:
                data_index = 0
