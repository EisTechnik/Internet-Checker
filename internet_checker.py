import socket
import time
from math import floor
from winsound import Beep

from win10toast import ToastNotifier


class LogMgr:
    def __init__(self):
        self.toaster = ToastNotifier()

    def show_toast(self, message: str):
        self.toaster.show_toast("Internet Monitor", message)

    def get_cur_time_str(self) -> str:
        return time.strftime("%Y-%m-%d %I:%M:%S%p EST")

    def log(self, raw_message):
        message = f"[{self.get_cur_time_str()}]\n{raw_message}\n\n"
        print(message)
        self.show_toast(message)
        with open("log.txt", "a+") as f:
            f.write(message)


def get_duration(time_var: float | int) -> str:
    # TODO: Improve this duration format code I keep reusing from 2017
    original_time = time_var
    seconds_in_minute = 60
    seconds_in_hour = 60 * seconds_in_minute
    seconds_in_day = 24 * seconds_in_hour
    days = floor(time_var / seconds_in_day)
    time_var -= days * seconds_in_day
    hours = floor(time_var / seconds_in_hour)
    time_var -= hours * seconds_in_hour
    minutes = floor(time_var / seconds_in_minute)
    time_var -= minutes * seconds_in_minute
    seconds = round(time_var)
    hours = floor(original_time / seconds_in_hour) % 24
    if days > 0:
        return "{}d:{}h:{}m:{}s".format(days, hours, minutes, seconds)
    elif hours > 0:
        return "{}h:{}m:{}s".format(hours, minutes, seconds)
    elif minutes > 0:
        return "{}m:{}s".format(minutes, seconds)
    else:
        return "{}s".format(seconds)


def is_online() -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 Second Timeout
        result = sock.connect_ex(("google.com", 80))
        # print(result)
        if result != 10035:
            return True
    except Exception as e:
        return False


def get_label(status: bool) -> str:
    return "Online" if status else "Offline"


def main():
    previous_switch = time.time()
    status = is_online()
    log_mgr = LogMgr()
    log_mgr.log(f"Monitoring started ({get_label(status)})")
    while True:
        time.sleep(1)
        new_status = is_online()
        if new_status != status:
            latest_switch = time.time()
            log_mgr.log(
                f"Now {get_label(new_status)} ({get_label(not(new_status))} for {get_duration(latest_switch-previous_switch)})"
            )
            previous_switch = latest_switch
            status = new_status
            try:
                Beep(600, 500)
            except RuntimeError as e:
                print(e)


if __name__ == "__main__":
    main()
