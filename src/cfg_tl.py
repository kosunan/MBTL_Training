from mem_access_util import mem_util
import time
PLR_STRUCT_SIZE = 0xC14  # 3084
DAT_P1_AD = 0xB44ED0     # 1Pデータ開始位置
advantage_f = 0
advantage_calc_flag = 0
on_flag = 0
save_flag = 0
game_data = 0
characters_data = 0
characters_data_list = []
anten = 0
hitstop = 0
stop_flag = 0
debug_flag = 0
mem_index = 0

class Characters_Data_Class:
    def __init__(self):
        self.characters_data = [Character_Data_Class(0),
                                Character_Data_Class(1),
                                Character_Data_Class(2),
                                Character_Data_Class(3)]

        self.characters_elements = [self.characters_data[0].elements,
                                    self.characters_data[1].elements,
                                    self.characters_data[2].elements,
                                    self.characters_data[3].elements]


class Game_Data_Class:
    def __init__(self):
        self.cont_list = list = []
        self.timer = pack(list, 0x59DAE4, 4)
        self.tr_flag = pack(list, 0x6E0D4C, 4)
        self.damage = pack(list, 0x7164B0, 4)
        self.hosei = pack(list, self.damage.ad - 12, 4)
        self.ukemi = pack(list, self.damage.ad - 4, 2)  # 受け身不能時間補正
        self.cam = pack(list, 0x716D90, 1500)
        self.start_posi = pack(list, 0x732DC8, 1)
        self.max_damage_pointer = pack(list, 0x72DC74, 4)
        self.pause = pack(list, 0x72DA78, 1)


class Character_Data_Class:
    def __init__(self, p_num):

        size = DAT_P1_AD + (PLR_STRUCT_SIZE * p_num)
        self.cont_list = list = []
        self.motion_type = pack(list, 0x1C + size, 2)
        self.c_timer = pack(list, 0x4C + size, 2)
        self.motion = pack(list, 0x548 + size, 4)
        self.atk = pack(list, 0x60 + size, 1)
        self.inv = pack(list, 0x61 + size, 1)
        self.x_posi = pack(list, 0x64 + size, 4)
        self.y_posi = pack(list, self.x_posi.ad + 4 + size, 4)
        self.air = pack(list, 0x6B + size, 2)
        self.gauge = pack(list, 0xA0 + size, 4)
        self.hitstop = pack(list, 0x298 + size, 1)
        self.seeld = pack(list, 0x2A0 + size, 1)
        self.tag_flag = pack(list, 0x2A4 + size, 1)
        self.step_inv = pack(list, 0x2B8 + size, 1)
        self.air_ukemi_1 = pack(list, 0x2c2 + size, 1)
        self.air_ukemi_2 = pack(list, 0x230 + size, 1)
        self.hit = pack(list, 0x2D8 + size, 2)
        self.ukemi1 = pack(list, 0x2DC + size, 2)
        self.ukemi2 = pack(list, 0x2E4 + size, 2)
        self.anten_stop2 = pack(list, 0x6f0 + size, 4)
        self.moon = pack(list, 0x928 + size, 4)
        self.moon_st = pack(list, 0x924 + size, 1)
        self.noguard = pack(list, 0xB7C + size, 1)

        if size == DAT_P1_AD or size == DAT_P1_AD + (PLR_STRUCT_SIZE * 2):
            self.anten_stop = pack(list, 0xB46212, 1)

        elif size == DAT_P1_AD + (PLR_STRUCT_SIZE * 1) or size == DAT_P1_AD + (PLR_STRUCT_SIZE * 3):
            self.anten_stop = pack(list, 0xB46215, 1)

        # 処理用変数
        self.elements = list = []
        self.adv_element = element_cre(list, 0, G_adv)
        self.action_element = element_cre(list, 0, G_mot)
        self.inv_element = element_cre(list, 0, G_inv)
        self.grd_stun_element = element_cre(list, 0, G_grd_stun)
        self.hit_stun_element = element_cre(list, 0, G_hit_stun)
        self.jmp_element = element_cre(list, 0, G_jmp)
        self.seeld_element = element_cre(list, 0, G_seeld)
        self.bunker_element = element_cre(list, 0, G_bunker)

        self.air_element = element_cre(list, 1, G_air)
        self.atk_element = element_cre(list, 1, G_atk)

        self.ignore_flag = 0
        self.motion_chenge_flag = 0
        self.act_flag = 0
        self.first_active = 0
        self.active = 0
        self.overall = 0


class Element_Class:
    def __init__(self, line, coler):
        self.val = 0
        self.num = "  "
        self.line = line
        self.font_coler = coler


def pack(list, addres, len):
    temp = mem_util.Mem_Data_Class(len, addres)
    list.append(temp)
    return temp


def element_cre(list, line, coler):
    temp = Element_Class(line, coler)
    list.append(temp)
    return temp


def text_font(rgb):
    Text_font_str = "\x1b[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


G_atk = get_font((255, 255, 255), (255, 0, 0))
G_mot = get_font((255, 255, 255), (65, 200, 0))
G_mot2 = get_font((255, 255, 255), (35, 158, 0))

G_grd_stun = get_font((255, 255, 255), (170, 170, 170))
G_hit_stun = get_font((255, 255, 255), (170, 170, 170))
G_fre = get_font((92, 92, 92), (25, 25, 25))
G_jmp = get_font((177, 177, 177), (241, 224, 132))
G_seeld = get_font((255, 255, 255), (145, 194, 255))
G_inv = get_font((200, 200, 200), (255, 255, 255))
G_adv = get_font((255, 255, 255), (25, 25, 25))
G_bunker = get_font((255, 255, 255), (225, 184, 0))
G_air = get_font((255, 255, 255), (25, 25, 25))
G_hit_stop = get_font((255, 255, 255), (228, 94, 155))
