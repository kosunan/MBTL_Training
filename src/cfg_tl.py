from ctypes import create_string_buffer

pid = 0
h_pro = 0
base_ad = 0

bar80_flag = 0
bar_range = 80
bar_flag = 0
bar_num = 0
bar_ini_flag = 0
bar_ini_flag2 = 0

advantage_calc_flag = 0
interval_time = 0
interval = 0
interval2 = 0
advantage_f = 0
anten = 0
hitstop = 0
anten_flag = 0
reset_flag = 0
debug_flag = 0

temp = create_string_buffer(4)
b_obj = create_string_buffer(24)


STOP_AD = 0x72DA78
MAX_Damage_Pointer_AD = 0x72DC64
PLR_STRUCT_SIZE = 0xC14  # 3084
DAT_P1_AD = 0xB44ED0   # 1Pデータ開始位置


class Flame_info:
    def __init__(self):
        self.atk_flag = 0
        self.action_flag = 0
        self.inv_flag = 0
        self.grd_stun_flag = 0
        self.hit_stun_flag = 0
        self.jmp_flag = 0
        self.air_flag = 0
        self.seeld_flag = 0
        self.bunker_flag = 0


class Para:
    def __init__(self, byte_len, address):
        self.ad = address
        self.num = 0
        self.b_dat = create_string_buffer(byte_len)


class Character_info:
    def __init__(self, size):
        # メモリ変数
        self.motion_type = Para(2, DAT_P1_AD + 0x1C + size)
        self.c_timer = Para(2, DAT_P1_AD + 0x4C + size)

        self.motion = Para(4, DAT_P1_AD + 0x548 + size)
        self.atk = Para(1, DAT_P1_AD + 0x60 + size)
        self.inv = Para(1, DAT_P1_AD + 0x61 + size)
        self.x_posi = Para(4, DAT_P1_AD + 0x64 + size)
        self.y_posi = Para(4, self.x_posi.ad + 4 + size)
        self.air = Para(2, DAT_P1_AD + 0x6B + size)

        self.gauge = Para(4, DAT_P1_AD + 0xA0 + size)
        self.hitstop = Para(1, DAT_P1_AD + 0x298 + size)
        self.seeld = Para(1, DAT_P1_AD + 0x2A0 + size)
        self.tag_flag = Para(1, DAT_P1_AD + 0x2A4 + size)
        self.step_inv = Para(1, DAT_P1_AD + 0x2B8 + size)

        self.air_ukemi_1 = Para(1, DAT_P1_AD + 0x2c2 + size)
        self.air_ukemi_2 = Para(1, DAT_P1_AD + 0x230 + size)

        self.hit = Para(2, DAT_P1_AD + 0x2D8 + size)
        self.ukemi1 = Para(2, DAT_P1_AD + 0x2DC + size)
        self.ukemi2 = Para(2, DAT_P1_AD + 0x2E4 + size)
        self.anten_stop2 = Para(4, DAT_P1_AD + 0x6f0 + size)

        self.moon = Para(4, DAT_P1_AD + 0x928 + size)
        self.moon_st = Para(1, DAT_P1_AD + 0x924 + size)

        self.noguard = Para(1, DAT_P1_AD + 0xB7C + size)

        if size == 0 or size == PLR_STRUCT_SIZE * 2:
            self.anten_stop = Para(1, 0xB46212)
        else:
            self.anten_stop = Para(1, 0xB46215)

        # 処理用変数
        self.c_timer_old = 0
        self.anten_stop2_old = 0
        self.hitstop_old = 0
        self.motion_type_old = 0
        self.motion_type_old2 = 0

        self.motion_num_old = 0
        self.ignore_flag = 0
        self.action_flag = 0
        self.atk_flag = 0
        self.inv_flag = 0
        self.grd_stun_flag = 0
        self.hit_stun_flag = 0
        self.jmp_flag = 0
        self.air_flag = 0
        self.seeld_flag = 0
        self.bunker_flag = 0

        self.motion_chenge_flag = 0
        self.first_active = 0
        self.active = 0
        self.overall = 0
        self.act_flag = 0
        self.bar_1 = ''
        self.bar_2 = ''
        self.barlist_1 = list(range(bar_range))
        self.barlist_2 = list(range(bar_range))
        self.barlist_3 = list(range(bar_range))
        self.barlist_4 = list(range(bar_range))
        self.barlist_5 = list(range(bar_range))
        self.barlist_6 = list(range(bar_range))
        self.barlist_7 = list(range(bar_range))


timer = Para(4, 0x59DAE4)
timer_old = 0
tr_flag = Para(4, 0x6E0D4C)
damage = Para(4, 0x7164B0)
hosei = Para(4, damage.ad - 12)
ukemi = Para(2, damage.ad - 4)  # 受け身不能時間補正
cam = Para(1500, 0x716D90)
start_posi = Para(1, 0x732DC8)
max_damage_pointer = Para(4, 0x72DC74)

P_info_1 = [
    Character_info(0),
    Character_info(PLR_STRUCT_SIZE),
    Character_info(PLR_STRUCT_SIZE * 2),
    Character_info(PLR_STRUCT_SIZE * 3)]

P_info_2 = [
    Character_info(0),
    Character_info(PLR_STRUCT_SIZE),
    Character_info(PLR_STRUCT_SIZE * 2),
    Character_info(PLR_STRUCT_SIZE * 3)]

for info1, info2 in zip(P_info_1, P_info_2):
    for n in range(bar_range):
        info1.barlist_1[n] = ""
        info1.barlist_2[n] = ""
        info1.barlist_3[n] = ""
        info1.barlist_4[n] = ""
        info1.barlist_5[n] = ""
        info1.barlist_6[n] = ""
        info1.barlist_7[n] = ""

        info2.barlist_1[n] = ""
        info2.barlist_2[n] = ""
        info2.barlist_3[n] = ""
        info2.barlist_4[n] = ""
        info2.barlist_5[n] = ""
        info2.barlist_6[n] = ""
        info2.barlist_7[n] = ""


P1 = P_info_1[0]
P2 = P_info_1[1]
P3 = P_info_1[2]
P4 = P_info_1[3]

p1 = P_info_2[0]
p2 = P_info_2[1]
p3 = P_info_2[2]
p4 = P_info_2[3]
