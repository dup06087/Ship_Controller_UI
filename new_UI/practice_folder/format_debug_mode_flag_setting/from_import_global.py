import time

import upload_bin_func_and_debug_func
import threading

firmware_file = upload_bin_func_and_debug_func
a = threading.Thread(target = firmware_file.main_func2, args=("COM6",))
a.start()

while True:
    time.sleep(1)
    print(firmware_file.exit_debug_mode_flag)
    firmware_file.exit_debug_mode_flag = True
    time.sleep(1)
    print(firmware_file.exit_debug_mode_flag)