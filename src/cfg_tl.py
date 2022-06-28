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


STOP_AD = 0x72DA68
MAX_Damage_Pointer_AD = 0x72DC64
PLR_STRUCT_SIZE = 0xC14  # 3084
DAT_P1_AD = 0xB44EC0   # 1Pデータ開始位置


class para:
    def __init__(self, byte_len, address):
        self.ad = address
        self.num = 0
        self.b_dat = create_string_buffer(byte_len)


timer = para(4, 0x59DA24)
timer_old = 0
tr_flag = para(4, 0x6E0D3C)
damage = para(4, 0x7164A0)
hosei = para(4, damage.ad - 12)
ukemi = para(2, damage.ad - 4)  # 受け身不能時間補正
cam = para(1500, 0x716D80)
start_posi = para(1, 0x732DB8)
max_damage_pointer = para(4, 0x72DC64)


class Character_info:
    def __init__(self, size):
        # メモリ変数
        self.motion_type = para(2, DAT_P1_AD + 0x40 + size)
        self.c_timer = para(2, DAT_P1_AD + 0x4C + size)

        self.motion = para(4, DAT_P1_AD + 0x548 + size)
        self.atk = para(1, DAT_P1_AD + 0x60 + size)
        self.inv = para(1, DAT_P1_AD + 0x61 + size)
        self.x_posi = para(4, DAT_P1_AD + 0x64 + size)
        self.y_posi = para(4, self.x_posi.ad + 4 + size)
        self.air_flag = para(2, DAT_P1_AD + 0x6B + size)

        self.gauge = para(4, DAT_P1_AD + 0xA0 + size)
        self.hitstop = para(1, DAT_P1_AD + 0x298 + size)
        self.seeld = para(1, DAT_P1_AD + 0x2A0 + size)
        self.tag_flag = para(1, DAT_P1_AD + 0x2A4 + size)
        self.step_inv = para(1, DAT_P1_AD + 0x2B8 + size)
        self.hit = para(2, DAT_P1_AD + 0x2D8 + size)
        self.ukemi1 = para(2, DAT_P1_AD + 0x2DC + size)
        self.ukemi2 = para(2, DAT_P1_AD + 0x2E4 + size)
        self.anten_stop2 = para(4, DAT_P1_AD + 0x6f0 + size)

        self.moon = para(4, DAT_P1_AD + 0x928 + size)
        self.moon_st = para(1, DAT_P1_AD + 0x924 + size)

        self.noguard = para(1, DAT_P1_AD + 0xB7C + size)

        if size == 0 or size == PLR_STRUCT_SIZE * 2:
            self.anten_stop = para(1, 0xB46202)
        else:
            self.anten_stop = para(1, 0xB46205)

        # 処理用変数
        self.c_timer_old = 0
        self.anten_stop2_old = 0
        self.hitstop_old = 0
        self.motion_type_old = 0
        self.ignore_flag = 0
        self.action_flag = 0

        self.motion_chenge_flag = 0
        self.first_active = 0
        self.active = 0
        self.zen = 0
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


P_info = [Character_info(0), Character_info(PLR_STRUCT_SIZE),
          Character_info(PLR_STRUCT_SIZE * 2), Character_info(PLR_STRUCT_SIZE * 3)]

p_info = [Character_info(0), Character_info(PLR_STRUCT_SIZE),
          Character_info(PLR_STRUCT_SIZE * 2), Character_info(PLR_STRUCT_SIZE * 3)]
for info1, info2 in zip(P_info, p_info):
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


P1 = P_info[0]
P2 = P_info[1]
P3 = P_info[2]
P4 = P_info[3]

p1 = p_info[0]
p2 = p_info[1]
p3 = p_info[2]
p4 = p_info[3]

st_barlist = list(range(bar_range))

for n in range(bar_range):
    st_barlist[n] = ""
st_bar = ""

temp = create_string_buffer(4)
b_obj = create_string_buffer(24)


advantage_calc_flag = 1


interval_time = 0
interval = 41
interval2 = 80

advantage_f = 0
anten = 0
anten_flag = 0
hitstop = 0
reset_flag = 0

debug_flag = 0
