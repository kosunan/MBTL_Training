import psutil
import ctypes
from struct import unpack
import cfg_ml

wintypes = ctypes.wintypes
windll = ctypes.windll
sizeof = ctypes.sizeof
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref

OpenProcess = windll.kernel32.OpenProcess
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HMODULE),
        ("szModule",           ctypes.c_byte * 256),
        ("szExePath",          ctypes.c_byte * 260),
    ]

###########################################################################
# ベースアドレス取得
###########################################################################


dict_pids = {
    p.info["name"]: p.info["pid"]
    for p in psutil.process_iter(attrs=["name", "pid"])
}

cfg_ml.pid = dict_pids["MBTL.exe"]
cfg_ml.h_pro = OpenProcess(0x1F0FFF, False, cfg_ml.pid)

# MODULEENTRY32を取得
snapshot = CreateToolhelp32Snapshot(0x00000008, cfg_ml.pid)

lpme = MODULEENTRY32()
lpme.dwSize = sizeof(lpme)

res = Module32First(snapshot, byref(lpme))

while cfg_ml.pid != lpme.th32ProcessID:
    res = Module32Next(snapshot, byref(lpme))

b_baseAddr = create_string_buffer(8)
b_baseAddr.raw = lpme.modBaseAddr

base_ad = unpack('q', b_baseAddr.raw)[0]

###########################################################################
# 各種アドレス
###########################################################################
TIMER_AD = 0x59BA34 + base_ad
TR_FLAG_AD = 0x713700 + base_ad
DAMAGE_AD = 0x7144A0 + base_ad
HOSEI_AD = DAMAGE_AD - 12
UKEMI_AD = DAMAGE_AD - 4 # 始動受け身不能時間補正
CAM_AD = 0x714D80 + base_ad

STOP_AD = 0x72BA68 + base_ad
START_POSI_AD = 0x730D98 + base_ad
MAX_Damage_Pointer_AD = 0x731144 + base_ad

PLR_STRUCT_SIZE = 0xC14  # 3084

DAT_P1_AD = 0xB42EB0 + base_ad  # 1Pデータ開始位置
DAT_P2_AD = DAT_P1_AD + PLR_STRUCT_SIZE  # 2Pデータ開始位置
DAT_P3_AD = DAT_P2_AD + PLR_STRUCT_SIZE
DAT_P4_AD = DAT_P3_AD + PLR_STRUCT_SIZE

ATK_P1_AD = DAT_P1_AD + 0x60
ATK_P2_AD = ATK_P1_AD + PLR_STRUCT_SIZE

INV_P1_AD = DAT_P1_AD + 0x61 #AFE9F0
INV_P2_AD = INV_P1_AD + PLR_STRUCT_SIZE


X_P1_AD = DAT_P1_AD + 0x64
X_P2_AD = X_P1_AD + PLR_STRUCT_SIZE
X_P3_AD = X_P2_AD + PLR_STRUCT_SIZE
X_P4_AD = X_P3_AD + PLR_STRUCT_SIZE

#
# ATK_P1_AD = DAT_P1_AD + 0x6C8
# ATK_P2_AD = ATK_P1_AD + PLR_STRUCT_SIZE

MOTION_TYPE_P1_AD = DAT_P1_AD + 0x40
MOTION_TYPE_P2_AD = MOTION_TYPE_P1_AD + PLR_STRUCT_SIZE

MOTION_P1_AD = DAT_P1_AD + 0x548
MOTION_P2_AD = MOTION_P1_AD + PLR_STRUCT_SIZE

HITSTOP_P1_AD = DAT_P1_AD + 0x296
HITSTOP_P2_AD = HITSTOP_P1_AD + PLR_STRUCT_SIZE

HIT_P1_AD = DAT_P1_AD + 0x2D8
HIT_P2_AD = HIT_P1_AD + PLR_STRUCT_SIZE

NOGUARD_P1_AD = DAT_P1_AD + 0xB7C
NOGUARD_P2_AD = NOGUARD_P1_AD + PLR_STRUCT_SIZE

M_ST_P1_AD = DAT_P1_AD + 0x924
M_ST_P2_AD = M_ST_P1_AD + PLR_STRUCT_SIZE

M_GAUGE_P1_AD = DAT_P1_AD + 0x928
M_GAUGE_P2_AD = M_GAUGE_P1_AD + PLR_STRUCT_SIZE

GAUGE_P1_AD = DAT_P1_AD + 0xA0
GAUGE_P2_AD = GAUGE_P1_AD + PLR_STRUCT_SIZE

ANTEN_STOP_AD = DAT_P1_AD + 0x731
ANTEN2_STOP_AD = ANTEN_STOP_AD + PLR_STRUCT_SIZE

SEELD_P1_AD = DAT_P1_AD + 0x2A0
SEELD_P2_AD = SEELD_P1_AD + PLR_STRUCT_SIZE

STEP_INV_P1_AD = DAT_P1_AD + 0x2B8
STEP_INV_P2_AD = STEP_INV_P1_AD + PLR_STRUCT_SIZE


HI_KO_P1_AD = DAT_P1_AD + 0x2A4
HI_KO_P2_AD = HI_KO_P1_AD + PLR_STRUCT_SIZE

UKEMI1_P1_AD = DAT_P1_AD + 0x2DC  # のけぞり時間
UKEMI1_P2_AD = UKEMI1_P1_AD + PLR_STRUCT_SIZE

UKEMI2_P1_AD = DAT_P1_AD + 0x2E4  # 受け身不能時間
UKEMI2_P2_AD = UKEMI2_P1_AD + PLR_STRUCT_SIZE




SAVE_BASE_AD = 0x66A0E8 + base_ad
# SAVE_BASE_AD = 0x5634A0 + base_ad
SAVE_END_AD = 0x66B6DF + base_ad
