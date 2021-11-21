from ctypes import create_string_buffer
# バイナリデータ変数定義
b_anten_stop = create_string_buffer(1)
b_anten2_stop = create_string_buffer(1)

b_atk_p1 = create_string_buffer(4)
b_atk_p2 = create_string_buffer(4)
b_cam = create_string_buffer(1500)
b_damage = create_string_buffer(4)
b_f_timer = create_string_buffer(4)
b_gauge_p1 = create_string_buffer(4)
b_gauge_p2 = create_string_buffer(4)
b_hit_p1 = create_string_buffer(2)
b_hit_p2 = create_string_buffer(2)
b_hitstop_p1 = create_string_buffer(4)
b_hitstop_p2 = create_string_buffer(4)
b_hosei = create_string_buffer(4)
b_m_st_p1 = create_string_buffer(1)
b_m_st_p2 = create_string_buffer(1)
b_mf_p1 = create_string_buffer(4)
b_mf_p2 = create_string_buffer(4)
b_mftp_p1 = create_string_buffer(2)
b_mftp_p2 = create_string_buffer(2)
b_noguard_p1 = create_string_buffer(1)
b_noguard_p2 = create_string_buffer(1)
b_tr_flag = create_string_buffer(1)
b_ukemi = create_string_buffer(2)
b_ukemi2 = create_string_buffer(2)
b_dat_p1 = create_string_buffer(4)
b_dat_p2 = create_string_buffer(4)
b_dat_p3 = create_string_buffer(4)
b_dat_p4 = create_string_buffer(4)

b_x_p1 = create_string_buffer(4)
b_x_p2 = create_string_buffer(4)
b_x_p3 = create_string_buffer(4)
b_x_p4 = create_string_buffer(4)
damage = create_string_buffer(4)
b_m_gauge_p1 = create_string_buffer(4)
b_m_gauge_p2 = create_string_buffer(4)
b_dmy_timer = create_string_buffer(4)
b_dmyend_timer = create_string_buffer(4)



b_dat_1 = create_string_buffer(4619)#補正　カメラ
b_dat_2 = create_string_buffer(2000)#pouse

b_dat_p1 = create_string_buffer(3060)
b_dat_p2 = create_string_buffer(3060)
b_dat_p3 = create_string_buffer(3060)
b_dat_p4 = create_string_buffer(3060)


# 表示するパラメーター類
Bar_flag = 0
Bar_num = 1
DataFlag1 = 1
P1_Bar = ""
P1_b_c = ""
P2_Bar = ""
P2_b_c = ""
act_P1 = 0
act_P2 = 0
act_flag_P1 = 0
act_flag_P2 = 0
anten_stop = 0
anten2_stop = 0

atk_p1 = 0
atk_p2 = 0
bar_ini_flag = 0
bar_ini_flag2 = 0
damage = 0
f_timer2 = 0
f_timer = 0
gauge_p1 = 0
gauge_p2 = 0
h_pro = 0
hit_p1 = 0
hit_p2 = 0
hitstop_p1 = 0
hitstop_p2 = 0
hosei = 0
interval_time = 0
interval = 41
interval2 = 80

kaisuu = 0
lng_flag = 1
mf_p1 = 0
mf_p2 = 0
mftp_p1 = 0
mftp_p2 = 0
moonchange_flag = 0
noguard_p1 = 0
noguard_p2 = 0
p1num = ""
p2num = ""
pid = 0
save_flag = 0
ukemi2 = 0
ukemi = 0
x_p1 = 0
x_p2 = 0
yuuriF = 0
zen_P1 = 0
zen_P2 = 0
dmy_timer = 0
dmyend_timer = 0
anten=0
old_mftp=0
p1_barlist = list(range(81))
p2_barlist = list(range(81))
for n in range(len(p1_barlist)):
    p1_barlist[n] =""

for n in range(len(p2_barlist)):
    p2_barlist[n] =""

p1_index = 0
p2_index = 0

# print(mylist)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
