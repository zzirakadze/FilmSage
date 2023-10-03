import os
import psutil
import subprocess

from icecream import ic
from loguru import logger
from tqdm import tqdm


def get_memory_info():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s" % (
        phymem.percent,
        str(int(phymem.used / 1024 / 1024)) + "M",
        str(int(phymem.total / 1024 / 1024)) + "M",
    )
    return line


def get_cpu_info():
    return "CPU: " + str(psutil.cpu_percent(interval=1)) + "%"


def get_computer_info():
    return get_cpu_info() + " " + get_memory_info()


def get_video_info():
    return "Video: " + str(psutil.virtual_memory().percent) + "%"


def check_process(process_name):
    return process_name in (p.name() for p in psutil.process_iter())


def get_process_info(process_name):
    return process_name + ": " + str(check_process(process_name))


def get_process_info_list(process_name_list):
    info_list = []
    for process_name in process_name_list:
        info_list.append(get_process_info(process_name))
    return info_list


def check_video_card_exist_or_not():
    return os.path.exists("/dev/dri")


def check_internet_connection():
    return os.system("ping -c 1 www.google.com") == 0


def get_internet_protocol_address():
    return os.system("ifconfig | grep inet")


def get_internet_provider_name():
    return os.system("curl ipinfo.io/org")


def get_available_disk_space():
    return os.system("df -h")


def get_available_wifi_networks():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "network"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def return_my_name(name: str):
    return name


ic(get_available_wifi_networks())

# ic(return_my_name("Zura"))
# logger.info(return_my_name("Zura"))
