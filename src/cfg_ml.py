from ctypes import create_string_buffer
# バイナリデータ変数定義
b_anten_stop_p1 = create_string_buffer(1)
b_anten_stop_p2 = create_string_buffer(1)

b_atk_p1 = create_string_buffer(4)
b_atk_p2 = create_string_buffer(4)
b_cam = create_string_buffer(1500)
b_damage = create_string_buffer(4)
b_timer = create_string_buffer(4)
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
b_tr_flag = create_string_buffer(4)

b_ukemi1 = create_string_buffer(2)
b_ukemi2 = create_string_buffer(2)

b_dat_p1 = create_string_buffer(4)
b_dat_p2 = create_string_buffer(4)
b_dat_p3 = create_string_buffer(4)
b_dat_p4 = create_string_buffer(4)

b_x_p1 = create_string_buffer(4)
b_x_p2 = create_string_buffer(4)
b_x_p3 = create_string_buffer(4)
b_x_p4 = create_string_buffer(4)

b_y_p1 = create_string_buffer(4)
b_y_p2 = create_string_buffer(4)
b_y_p3 = create_string_buffer(4)
b_y_p4 = create_string_buffer(4)

b_s_x_p1 = create_string_buffer(4)
b_s_x_p2 = create_string_buffer(4)
b_s_x_p3 = create_string_buffer(4)
b_s_x_p4 = create_string_buffer(4)

b_s_y_p1 = create_string_buffer(4)
b_s_y_p2 = create_string_buffer(4)
b_s_y_p3 = create_string_buffer(4)
b_s_y_p4 = create_string_buffer(4)

damage = create_string_buffer(4)
b_m_gauge_p1 = create_string_buffer(4)
b_m_gauge_p2 = create_string_buffer(4)
b_dmy_timer = create_string_buffer(4)
b_dmyend_timer = create_string_buffer(4)
b_hi_ko_flag_p1 = create_string_buffer(1)
b_hi_ko_flag_p2 = create_string_buffer(1)
b_start_posi = create_string_buffer(1)

temp = create_string_buffer(4)

# 表示するパラメーター類
Bar_flag = 0
Bar_num = 1
DataFlag1 = 1
P1_Bar = ""
P1_b_c = ""
P2_Bar = ""
P2_b_c = ""
st_Bar = ""
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
m_gauge_p1 = 0
m_gauge_p2 = 0

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
mf_p1_2 = 0
mf_p2_2 = 0
mftp_p1 = 0
mftp_p2 = 0
mftp_p1_old = 0
mftp_p2_old = 0

mftp77_p1 = 0
mftp77_p2 = 0

flag_77_p1 = 0
flag_77_p2 = 0

moonchange_flag = 0
noguard_p1 = 0
noguard_p2 = 0
p1num = ""
p2num = ""
pid = 0
save_flag = 0
ukemi2 = 0
ukemi1 = 0
x_p1 = 0
x_p2 = 0
yuuriF = 0
zen_P1 = 0
zen_P2 = 0
dmy_timer = 0
dmyend_timer = 0
anten = 0
old_mftp = 0
reset_flag = 0
p1_barlist = list(range(80))
p2_barlist = list(range(80))
st_barlist = list(range(80))
Bar80_flag = 0
for n in range(len(p1_barlist)):
    p1_barlist[n] = ""
for n in range(len(p2_barlist)):
    p2_barlist[n] = ""
for n in range(len(st_barlist)):
    st_barlist[n] = ""

p1_index = 0
p2_index = 0
size_p1 = 0
size_p2 = 0
