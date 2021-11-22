
import psutil
import ctypes
from ctypes import *
from struct import unpack
import cfg_ml

OpenProcess = windll.kernel32.OpenProcess
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next

# constant
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

PLR_STRUCT_SIZE = 0xBF4  # 3060

DAT_P1_AD = 0xA8F120 + base_ad  # 1Pデータ開始位置
DAT_P2_AD = DAT_P1_AD + PLR_STRUCT_SIZE  # 2Pデータ開始位置
DAT_P3_AD = DAT_P2_AD + PLR_STRUCT_SIZE
DAT_P4_AD = DAT_P3_AD + PLR_STRUCT_SIZE

# ST_AD = 0x0155C150  # 状況データ開始位置 6032
# STOP_ST_AD = 0x0059B390  # 停止状況データ開始位置

X_P1_AD = DAT_P1_AD + 0x84
X_P2_AD = X_P1_AD + PLR_STRUCT_SIZE
X_P3_AD = X_P2_AD + PLR_STRUCT_SIZE
X_P4_AD = X_P3_AD + PLR_STRUCT_SIZE

ATK_P1_AD = DAT_P1_AD + 0x6D8
ATK_P2_AD = ATK_P1_AD + PLR_STRUCT_SIZE

MOTION_TYPE_P1_AD = DAT_P1_AD + 0x3C
MOTION_TYPE_P2_AD = MOTION_TYPE_P1_AD + PLR_STRUCT_SIZE

MOTION_P1_AD = DAT_P1_AD + 0x568
MOTION_P2_AD = MOTION_P1_AD + PLR_STRUCT_SIZE

HITSTOP_P1_AD = DAT_P1_AD + 0x2B6
HITSTOP_P2_AD = HITSTOP_P1_AD + PLR_STRUCT_SIZE

HIT_P1_AD = DAT_P1_AD + 0x2F8
HIT_P2_AD = HIT_P1_AD + PLR_STRUCT_SIZE

NOGUARD_P1_AD = DAT_P1_AD + 0xB8C
NOGUARD_P2_AD = NOGUARD_P1_AD + PLR_STRUCT_SIZE

M_ST_P1_AD = DAT_P1_AD + 0x934
M_ST_P2_AD = M_ST_P1_AD + PLR_STRUCT_SIZE

M_GAUGE_P1_AD = DAT_P1_AD + 0x938
M_GAUGE_P2_AD = M_GAUGE_P1_AD + PLR_STRUCT_SIZE

GAUGE_P1_AD = DAT_P1_AD + 0xC0
GAUGE_P2_AD = GAUGE_P1_AD + PLR_STRUCT_SIZE

ANTEN_STOP_AD = DAT_P1_AD + 0x741
ANTEN2_STOP_AD = ANTEN_STOP_AD + PLR_STRUCT_SIZE

HI_KO_P1_AD = DAT_P1_AD + 0x2C2
HI_KO_P2_AD = HI_KO_P1_AD + PLR_STRUCT_SIZE

HOSEI_AD = 0x669514 + base_ad
UKEMI_AD =  DAT_P1_AD + 0xEF8
UKEMI2_AD = 0x66951C + base_ad

TR_FLAG_AD = 0x633E64 + base_ad

CAM_AD = 0x669E00 + base_ad
CAM_1_AD = 0x669EC8 + base_ad
CAM_2_AD = 0x669EE0 + base_ad
CAM_3_AD = 0x669EF8 + base_ad

STOP_AD = 0x680AE8 + base_ad
DAMAGE_AD = 0x669520 + base_ad

TIMER_AD = 0x563994 + base_ad
DMY_TIMER_AD = 0x154AF9C + base_ad
DMYEND_TIMER_AD = 0x154AFA0 + base_ad
