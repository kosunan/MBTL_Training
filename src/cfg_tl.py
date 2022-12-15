from mem_access_util import mem_util
import time

advantage_f = 0

advantage_calc_flag = 0
on_flag = 0
save_flag = 0
game_data = 0

characters_data_list = []
anten = 0
hitstop = 0
stop_flag = 0
stop_view_flag = 0
debug_flag = 0
light_mode_flag = 0
mem_index = 0
template_view_flag = 0
loop_num = 0


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

        self.characters_debug_elements = [self.characters_data[0].debug_elements,
                                          self.characters_data[1].debug_elements,
                                          self.characters_data[2].debug_elements,
                                          self.characters_data[3].debug_elements]


class Game_Data_Class:
    def __init__(self):
        self.cont_list = list = []
        self.timer = pack(list, 0x6607D0, 4)
        self.timer_2 = pack(list, 0x6607D0, 4)
        self.tr_flag = pack(list, 0x8707E4, 4)
        self.damage = pack(list, 0x8A6020, 4)
        self.hosei = pack(list, self.damage.ad - 12, 4)
        self.ukemi = pack(list, self.damage.ad - 4, 2)  # 受け身不能時間補正
        self.cam = pack(list, 0x8A6910, 1500)
        self.cam_1 = pack(list, self.cam.ad + 0xc8, 4)
        self.start_posi = pack(list, 0x8C52E4, 1)
        self.max_damage_pointer = pack(list, 0x8C578C, 4)
        self.pause = pack(list, 0x8BEDA8, 1)

class Character_Data_Class:
    def __init__(self, p_num):
        PLR_STRUCT_SIZE = 0xC34  #
        DAT_P1_AD = 0xCEC560     # 1Pデータ開始位置

        size = DAT_P1_AD + (PLR_STRUCT_SIZE * p_num)
        self.cont_list = list = []
        self.motion_type = pack(list, 0x1C + size, 2)
        self.c_timer = pack(list, 0x4C + size, 2)
        self.motion = pack(list, 0x570 + size, 4)
        self.atk = pack(list, 0x60 + size, 1)
        self.inv = pack(list, 0x61 + size, 1)
        self.x_posi = pack(list, 0x64 + size, 4)
        self.y_posi = pack(list, self.x_posi.ad + 4, 4)
        self.x_speed = pack(list, 0x1E0 + size, 4)
        self.y_speed = pack(list, 0x1E4 + size, 4)
        self.health = pack(list, 0x8C + size, 4)
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
        self.heat_inv = pack(list, 0x5E4 + size, 1)
        self.armor_1 = pack(list, 0x614 + size, 1)
        self.armor_2 = pack(list, 0xC0 + size, 1)

        # self.anten_stop2 = pack(list, 0x6f0 + size, 4)
        self.moon = pack(list, 0x950 + size, 4)
        self.moon_st = pack(list, 0x94C + size, 1)
        self.noguard2 = pack(list, 0xBA4 + size, 1)
        self.noguard = pack(list, 0xB9C + size, 1)
        self.bunker = pack(list, 0x6E4 + size, 1)
        self.bunker_pointer = pack(list, 0x6EC + size, 4)

        if p_num == 0 or p_num == 2:
            self.anten_stop = pack(list, 0xCED8EA, 1)

        elif p_num == 1 or p_num == 3:
            self.anten_stop = pack(list, 0xCED8ED, 1)

        # 処理用変数
        self.elements = list = []
        self.adv_element = element_cre(list, 0, G_adv)
        self.action_element = element_cre(list, 0, G_mot)
        self.koutyoku_element = element_cre(list, 0, G_mot2)
        self.inv_element = element_cre(list, 0, G_inv)
        self.grd_stun_element = element_cre(list, 0, G_grd_stun)
        self.hit_stun_element = element_cre(list, 0, G_hit_stun)
        self.jmp_element = element_cre(list, 0, G_jmp)
        self.seeld_element = element_cre(list, 0, G_seeld)
        self.bunker_element = element_cre(list, 0, G_bunker)
        self.armor_element = element_cre(list, 0, G_armor)
        self.hitstop_element = element_cre(list, 0, G_hit_stop)
        self.wake_up_element = element_cre(list, 0, G_wake_up)

        self.air_element = element_cre(list, 1, G_air)
        self.atk_element = element_cre(list, 1, G_atk)

        self.debug_elements = list = []

        self.line_3_element = element_cre(list, 2, G_adv)
        self.line_4_element = element_cre(list, 3, G_adv)
        self.line_5_element = element_cre(list, 4, G_adv)
        self.line_6_element = element_cre(list, 5, G_adv)
        self.line_7_element = element_cre(list, 6, G_adv)
        self.line_8_element = element_cre(list, 7, G_adv)
        self.line_9_element = element_cre(list, 8, G_adv)
        self.line_10_element = element_cre(list, 9, G_adv)

        self.ignore_flag = 0
        self.noguard_flag = 0

        self.motion_chenge_flag = 0
        self.act_flag = 0
        self.first_active = 0
        self.active = 0
        self.koutyoku_f = 0
        self.stun_f = 0
        self.jmp_f = 0
        self.inv_f = 0
        self.hitstop_f = 0
        self.overall = 0
        self.seeld_f = 0
        self.armor_f = 0
        self.bunker_f = 0
        self.stop_flag = 0


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
    Text_font_str = "\x1b[38;2;" + str(rgb[0]).rjust(3, "0")[-3:] + ";" + str(rgb[1]).rjust(3, "0")[-3:] + ";" + str(rgb[2]).rjust(3, "0")[-3:] + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]).rjust(3, "0")[-3:] + ";" + str(rgb[1]).rjust(3, "0")[-3:] + ";" + str(rgb[2]).rjust(3, "0")[-3:] + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


G_atk = get_font((255, 255, 255), (240, 0, 0))
G_mot = get_font((255, 255, 255), (65, 200, 0))
G_mot2 = get_font((255, 255, 255), (35, 158, 0))
G_mot3 = get_font((255, 255, 255), (123, 184, 193))

G_grd_stun = get_font((255, 255, 255), (170, 170, 170))
G_hit_stun = get_font((255, 255, 255), (170, 170, 170))
G_fre = get_font((92, 92, 92), (25, 25, 25))
G_jmp = get_font((255, 255, 255), (241, 224, 132))
G_seeld = get_font((255, 255, 255), (145, 194, 255))
G_inv = get_font((200, 200, 200), (255, 255, 255))
G_adv = get_font((255, 255, 255), (25, 25, 25))
G_bunker = get_font((255, 255, 255), (255, 122, 33))
G_armor = get_font((255, 255, 255), (255, 122, 33))

G_air = get_font((255, 255, 255), (25, 25, 25))
G_hit_stop = get_font((255, 255, 255), (59, 69, 129))
G_wake_up = get_font((255, 255, 255), (85, 33, 79))
