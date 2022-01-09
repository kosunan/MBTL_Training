from ctypes import create_string_buffer

m_st_p1 = create_string_buffer(1)
m_st_p2 = create_string_buffer(1)

m_gauge_p1 = create_string_buffer(4)
m_gauge_p2 = create_string_buffer(4)

mf_p1 = create_string_buffer(4)
mf_p2 = create_string_buffer(4)

mftp_p1 = create_string_buffer(2)
mftp_p2 = create_string_buffer(2)

ukemi1_p1 = create_string_buffer(2)
ukemi1_p2 = create_string_buffer(2)

ukemi2_p1 = create_string_buffer(2)
ukemi2_p2 = create_string_buffer(2)

x_p1 = create_string_buffer(4)
x_p2 = create_string_buffer(4)
x_p3 = create_string_buffer(4)
x_p4 = create_string_buffer(4)

y_p1 = create_string_buffer(4)
y_p2 = create_string_buffer(4)
y_p3 = create_string_buffer(4)
y_p4 = create_string_buffer(4)

s_x_p1 = create_string_buffer(4)
s_x_p2 = create_string_buffer(4)
s_x_p3 = create_string_buffer(4)
s_x_p4 = create_string_buffer(4)

s_y_p1 = create_string_buffer(4)
s_y_p2 = create_string_buffer(4)
s_y_p3 = create_string_buffer(4)
s_y_p4 = create_string_buffer(4)

damage = create_string_buffer(4)
hosei = create_string_buffer(4)

gauge_p1 = create_string_buffer(4)
gauge_p2 = create_string_buffer(4)

hitstop_p1 = create_string_buffer(4)
hitstop_p2 = create_string_buffer(4)

data_size = 3060
P1_data1= create_string_buffer(data_size)
P2_data1= create_string_buffer(data_size)

data_size2 = 0x15F7
save_data = create_string_buffer(data_size2)
