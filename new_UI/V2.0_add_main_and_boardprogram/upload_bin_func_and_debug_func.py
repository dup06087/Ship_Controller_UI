# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023

@author: USER
"""

#python C:\Users\USER\Desktop\STM32\upload_bin_func_and_debug_func.py
#python C:\Users\USER\Documents\STM32\upload_bin_func_and_debug_func.py

import os
import sys
import serial
import time
from datetime import datetime
import numpy as np
import _thread

from contextlib import redirect_stdout

#bin_file = "C:/Users/USER/Desktop/STM32/BIN.bin"
from PyQt5.QtCore import pyqtSignal, QObject

bin_file = "vcu_f413zh_mbed.NUCLEO_F413ZH.bin"
#bin_file = "C:/Users/USER/Documents/STM32/BIN3_F413ZH.bin"
#bin_file = os.path.join(sys.path[0], "BIN.bin")
port = "COM6"
skip_checksum = True
exit_debug_mode_flag = False


debug_bytearray_list = [b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'']
for i in range(16):
    debug_bytearray_list[i] = b'0000000000000000' 

ds3231_time_u32 = 0
ds3231_date_str = str(datetime.fromtimestamp(ds3231_time_u32))
test_module1_u8_B0, test_module1_u8_B1, test_module1_u8_B7 = 0, 0, 0
test_module2_u8_B0, test_module2_u8_B1, test_module2_u8_B7 = 0, 0, 0

'''바꾼부분'''
class PrintEmitter(QObject):
    textEmitted = pyqtSignal(str)

    def write(self, text):
        self.textEmitted.emit(str(text))

    def flush(self):
        pass

sys.stdout = PrintEmitter()

usb_state = False
'''바꾼부분 끝'''
def read_bin(bin_file):
    try:
        with open(bin_file, "rb") as f:
            contents = f.read()
        print("Found .bin file (%s)" % bin_file)    
        
        #for i in range(len(contents) // 16):
        #    print("0x%08x: 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x" % (16*i, contents[16*i + 3], contents[16*i + 2], contents[16*i + 1], contents[16*i + 0], contents[16*i + 7], contents[16*i + 6], contents[16*i + 5], contents[16*i + 4], contents[16*i + 11], contents[16*i + 10], contents[16*i + 9], contents[16*i + 8], contents[16*i + 15], contents[16*i + 14], contents[16*i + 13], contents[16*i + 12]))
        #if len(contents) % 16 != 0:
        #    temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
        #    for i in range(16):
        #        if (len(contents) // 16) * 16 + i < len(contents):
        #            temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
        #    print("0x%08x: 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s" % ((len(contents) // 16) * 16, temp[3], temp[2], temp[1], temp[0], temp[7], temp[6], temp[5], temp[4], temp[11], temp[10], temp[9], temp[8], temp[15], temp[14], temp[13], temp[12]))
        
        for i in range(len(contents) // 16):
            print("0x%08x: 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x" % (16*i, contents[16*i + 0], contents[16*i + 1], contents[16*i + 2], contents[16*i + 3], contents[16*i + 4], contents[16*i + 5], contents[16*i + 6], contents[16*i + 7], contents[16*i + 8], contents[16*i + 9], contents[16*i + 10], contents[16*i + 11], contents[16*i + 12], contents[16*i + 13], contents[16*i + 14], contents[16*i + 15]))
        if len(contents) % 16 != 0:
            temp = ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]
            for i in range(16):
                if (len(contents) // 16) * 16 + i < len(contents):
                    temp[i] = "%02x" % contents[(len(contents) // 16) * 16 + i]
            print("0x%08x: 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s" % ((len(contents) // 16) * 16, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]))
        
        #crc = 0x00000000
        #for i in range(len(contents)):
        #    crc = crc + int(("0x%02x" % contents[i]), 16)
        #    crc = crc & 0xffffffff       
        #print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))
            
        crc = np.uint32(0x00000000)
        for i in range(len(contents)):
            crc = crc + np.uint32(int(("0x%02x" % contents[i]), 16))     
        print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, len(contents) - 1, crc, len(contents)))
        
        if len(contents) % 128 == 0:
            num_128 = len(contents) // 128
        else:
            num_128 = (len(contents) // 128) + 1
            
        #crc_128 = 0x00000000
        #for i in range(num_128 * 128):
        #    if i < len(contents):
        #        crc_128 = crc_128 + int(("0x%02x" % contents[i]), 16)
        #    else:
        #        crc_128 = crc_128 + int(("0x%02x" % 0xff), 16)
        #    crc_128 = crc_128 & 0xffffffff  
        #print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))
        
        crc_128 = np.uint32(0x00000000)
        for i in range(num_128 * 128):
            if i < len(contents):
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % contents[i]), 16))     
            else:
                crc_128 = crc_128 + np.uint32(int(("0x%02x" % 0xff), 16))     
        print("Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))

        print("")
        time.sleep(1.0)
        
        return True, contents, crc, num_128, crc_128
    except:
        print("Can not find .bin file (%s)" % bin_file)
        
        print("")
        time.sleep(1.0)
        
        return False, b'', np.uint32(0x00000000), 0, np.uint32(0x00000000)


def open_serial(port):
    try:
        ser = serial.Serial(port)
        ser.baudrate = 115200
        
        print("Opened %s" % port)
        
        print("")
        time.sleep(1.0)
        
        check_ser = True
        #ser = ser
    except:
        print("Can not open %s" % port)
        
        print("")
        time.sleep(1.0)
        
        check_ser = False
        ser = False
        
    return check_ser, ser


def check_serial(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
            
            print("%s is alive" % port)
            
            print("")
            time.sleep(1.0)
            
            check_ser = True
        except:
            print("%s is dead" % port)
            
            print("")
            time.sleep(1.0)
            
            check_ser = False
    else:
        print("Can not found serial port")
        
        print("")
        time.sleep(1.0)
        
        #check_ser = False
        
    return check_ser


def close_serial(check_ser, ser):
    if check_ser == True:
        try:
            ser.close()
            
            print("Closed %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_ser = False
        except:
            print("Can not close serial port")
            
            print("")
            time.sleep(1.0)
            
            check_ser = False
    else:
        print("Can not found serial port")
        
        print("")
        time.sleep(1.0)
        
        #check_ser = False
        
    return check_ser
          
  
def enter_bootloader_mode(check_ser, ser):
    if check_ser == True:
        try:
            data_dummy = b't09780000000000000000\r'
            for i in range(4):
                ser.write(data_dummy) 
                time.sleep(0.05)
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()

            request = b't09780100000000000000\r'
            for i in range(10):
                ser.write(request) 
                time.sleep(0.05)
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()
    
            check_enter_bootloader_mode = True

            print("Entered Bootloader mode")

            print("")
            time.sleep(1.0)
        except:
            print("Can not enter Bootloader mode")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_enter_bootloader_mode = False
    else:
        print("Can not enter Bootloader mode")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_enter_bootloader_mode = False
                
    return check_enter_bootloader_mode


def check_hse_frequency(check_ser, ser):
    if check_ser == True:
        try:
            data_dummy = b't0048ffffffffffffffff\r'
            for i in range(16):
                ser.write(data_dummy) 
                time.sleep(0.05)
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            request = b't079100\r'
            for i in range(40):
                ser.write(request) 
                time.sleep(0.025)
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't079179\r':
                            print("Check HSE frequency Response Done (ACK)") 

                            
                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = True
                            
                            break
                        elif response == b't07911f\r':
                            print("Check HSE frequency Response Failed (NACK)")

                            check_check_hse_frequency = True
                            check_check_hse_frequency_opt = False

                            break
                        else:
                            print("Check HSE frequency Response Failed (Missing data)")
                        
                            check_check_hse_frequency = False
                            check_check_hse_frequency_opt = True

                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Check HSE frequency Response Failed (Timeout)")
                    
                    check_check_hse_frequency = False
                    check_check_hse_frequency_opt = False
                    
                    break
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()
    
            if check_check_hse_frequency == True:
                if check_check_hse_frequency_opt == True:
                    print("Checked HSE frequency")
                else:
                    print("Already checked HSE frequency")
            else:
                print("Can not check HSE frequency")
                
            print("")
            time.sleep(1.0)
        except:
            print("Can not check HSE frequency")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_check_hse_frequency = False
            check_check_hse_frequency_opt = False
    else:
        print("Can not check HSE frequency")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_check_hse_frequency = False
        check_check_hse_frequency_opt = False
                
    return check_check_hse_frequency, check_check_hse_frequency_opt    


def get_ID(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            request = b't002100\r'
            ser.write(request) 
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            print("Get ID Request Done (ACK)") 
                            
                            check_id = True
                            
                            break
                        elif response == b't00211f\r':
                            print("Get ID Request Failed (NACK)")
                            
                            check_id = False
                            
                            break
                        else:
                            print("Get ID Request Failed (Unknown)")
                            
                            check_id = False
                            
                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Get ID Request Failed (Timeout)")
                    
                    check_id = False
                    
                    break
                    
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response[0:5] == b't0022':
                            if response[5:10] == b'0421\r':
                                print("Get ID Done (ID: 0x%03s (STM32F446xx))" % response[6:9].decode("utf-8"))
                                
                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)
                                
                                break
                            elif response[5:10] == b'0463\r':
                                print("Get ID Done (ID: 0x%03s (STM32F413xx))" % response[6:9].decode("utf-8"))
                                
                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)
                                
                                break
                            else:
                                print("Get ID Done (ID: 0x%03s)" % response[6:9].decode("utf-8"))
                                
                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)
                                
                                break
                        else:
                            print("Get ID Failed (Unknown)")
                            
                            chip_id = 0x000
                            
                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Get ID Failed (Timeout)")
                    
                    chip_id = 0x000
                    
                    break
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't002179\r':
                            print("Get ID Response Done (ACK)")
                            
                            check_id = True
                            
                            break
                        elif response == b't00211f\r':
                            print("Get ID Response Failed (NACK)")
                            
                            check_id = False
                            
                            break
                        else:
                            print("Get ID Response Failed (Unknown)")
                            
                            check_id = False
                            
                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Get ID Response Failed (Timeout)")
                    
                    check_id = False
                    
                    break
            
            if check_id == True:
                if chip_id == 0x421:
                    print("Got ID: 0x%03x (STM32F446xx)" % chip_id)
                elif chip_id == 0x463:
                    print("Got ID: 0x%03x (STM32F413xx)" % chip_id)
                else:
                    print("Got ID: 0x%03x" % chip_id)
            else:
                print("Can not get Chip ID")
            
            print("")
            time.sleep(1.0)
        except:
            print("Can not get Chip ID")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_id = False
            chip_id = 0x000
    else:
        print("Can not get Chip ID")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_id = False
        chip_id = 0x000
                
    return check_id, chip_id    


def erase_sector(check_ser, ser, sector):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            while_break = False
                
            request = b't043100\r' 
            ser.write(request) 
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            print("Erase Sector Request Done (ACK)") 
                            
                            check_erase_sector = True
                            
                            break
                        elif response == b't04311f\r':
                            print("Erase Sector Request Failed (NACK)")
                            
                            while_break = True
                            check_erase_sector = False
                            
                            break
                        else:
                            print("Erase Sector Request Failed (Unknown)")
                            
                            while_break = True
                            check_erase_sector = False
                            
                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Sector Request Failed (Timeout)")
                    
                    while_break = True
                    check_erase_sector = False
                    
                    break

            if while_break == False:
                request = b't0431%02x\r' % sector
                ser.write(request) 
                print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)

            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            print("Erase Sector %02d Done (ACK)" % sector) 
                            
                            check_erase_sector = True
                            
                            break
                        elif response == b't04311f\r':
                            print("Erase Sector %02d Failed (NACK)" % sector)
                            
                            check_erase_sector = False
                            
                            break
                        else:
                            print("Erase Sector %02d Failed (Unknown)" % sector)
                            
                            check_erase_sector = False
                            
                            break
                if time.time() >= prev_time + 5.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Sector %02d Failed (Timeout)" % sector)
                    
                    check_erase_sector = False
                    
                    break
                
                if while_break == True:
                    break
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            print("Erase Sector %02d Response Done (ACK)" % sector) 
                            
                            check_erase_sector = True
                            
                            break
                        elif response == b't04311f\r':
                            print("Erase Sector %02d Response Failed (NACK)" % sector)
                            
                            check_erase_sector = False
                            
                            break
                        else:
                            print("Erase Sector %02d Response Failed (Unknown)" % sector)
                            
                            check_erase_sector = False
                            
                            break
                if time.time() >= prev_time + 5.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Sector %02d Response Failed (Timeout)" % sector)
                    
                    check_erase_sector = False
                    
                    break
                
                if while_break == True:
                    break
            
            if check_erase_sector == True:
                print("Erased sector %02d" % sector)
            else:
                print("Can not erase sector %02d" % sector)
            
            print("")
            time.sleep(1.0)
        except:
            print("Can not erase sector %02d" % sector)
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_erase_sector = False
    else:
        print("Can not erase sector %02d" % sector)
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_erase_sector = False
                
    return check_erase_sector


def erase_memory(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            while_break = False
                
            request = b't0431ff\r'
            ser.write(request) 
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            print("Erase Memory Request Done (ACK)") 
                            
                            check_erase = True
                            
                            break
                        elif response == b't04311f\r':
                            print("Erase Memory Request Failed (NACK)")
                            
                            while_break = True
                            check_erase = False
                            
                            break
                        else:
                            print("Erase Memory Request Failed (Unknown)")
                            
                            while_break = True
                            check_erase = False
                            
                            break
                if time.time() >= prev_time + 1.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Memory Request Failed (Timeout)")
                    
                    while_break = True
                    check_erase = False
                    
                    break
            
            response = b''
            prev_time = time.time()
            while True:
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if response == b't043179\r':
                            print("Erase Memory Response Done (ACK)") 
                            
                            check_erase = True
                            
                            break
                        elif response == b't04311f\r':
                            print("Erase Memory Response Failed (NACK)")
                            
                            check_erase = False
                            
                            break
                        else:
                            print("Erase Memory Response Failed (Unknown)")
                            
                            check_erase = False
                            
                            break
                if time.time() >= prev_time + 30.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Memory Response Failed (Timeout)")
                    
                    check_erase = False
                    
                    break
                
                if while_break == True:
                    break
            
            if check_erase == True:
                print("Erased memory")
            else:
                print("Can not erase memory")

            data_dummy = b't079100\r'
            for i in range(4):
                ser.write(data_dummy) 
                time.sleep(0.05)
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()
            
            print("")
            time.sleep(1.0)
        except:
            print("Can not erase memory")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_erase = False
    else:
        print("Can not erase memory")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_erase = False
                
    return check_erase    
    
   
def upload_bin(check_ser, ser, check_bin, contents, num_128):
    if check_ser == True and check_bin == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            for_break = False
            for num in range(num_128):
                while ser.in_waiting > 0:
                    data_dummy = ser.read()
                    
                addr = 0x08000000 + (128 * num)
                request = b't0315%08x7f\r' % addr
                ser.write(request) 
                print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)
                    
                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        #print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                print("Write Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_upload_bin = True
                                
                                break
                            elif response == b't03111f\r':
                                print("Write Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_upload_bin = False
                                
                                break
                            else:
                                print("Write Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_upload_bin = False
                                
                                break
                    if time.time() >= prev_time + 1.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        print("Write Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        
                        for_break = True
                        check_upload_bin = False
                        
                        break
                    
                if for_break == True:
                    break
                 
                for i in range(16):
                    temp = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
                    for j in range(8):
                        if ((128 * num) + (8 * i) + j) < len(contents):
                            temp[j] = contents[(128 * num) + (8 * i) + j]  
                            
                    request = b't0048%02x%02x%02x%02x%02x%02x%02x%02x\r' % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
                    ser.write(request)
                    print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                    time.sleep(0.001)
                    
                    response = b''
                    prev_time = time.time()  
                    while True:
                        if ser.in_waiting > 0:
                            data_rx = ser.read()
                            #print(data_rx)
                            response = response + data_rx
                            if data_rx == b'\r':
                                print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                                if response == b't031179\r':
                                    print("Write Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done (ACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, request[5:7].decode("utf-8"), request[7:9].decode("utf-8"), request[9:11].decode("utf-8"), request[11:13].decode("utf-8"), request[13:15].decode("utf-8"), request[15:17].decode("utf-8"), request[17:19].decode("utf-8"), request[19:21].decode("utf-8"), num + 1, num_128))
                                    
                                    check_upload_bin = True
                                    
                                    break
                                elif response == b't03111f\r':
                                    print("Write Memory 0x%08x - 0x%08x Failed (NACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                                    
                                    for_break = True
                                    check_upload_bin = False
                                    
                                    break
                                else:
                                    print("Write Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                                    
                                    for_break = True
                                    check_upload_bin = False
                                    
                                    break
                        if time.time() >= prev_time + 1.0:
                            print("Recv: %s" % response[0:].decode("utf-8"))
                            
                            for_break = True
                            check_upload_bin = False
                            
                            print("Write Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            break   
                        
                    if for_break == True:
                        break
                        
                if for_break == True:
                    break
                    
                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        #print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't031179\r':
                                print("Write Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_upload_bin = True
                                
                                break
                            elif response == b't03111f\r':
                                print("Write Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_upload_bin = False
                                
                                break
                            else:
                                print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_upload_bin = False
                                
                                break
                    if time.time() >= prev_time + 1.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        
                        for_break = True
                        check_upload_bin = False
                        
                        break
                    
                if for_break == True:
                    break
                
                time.sleep(0.01)
                
            if check_upload_bin == True:
                print("Uploaded .bin file")
            else:
                print("Can not upload .bin file")
            
            print("")
            time.sleep(1.0)
        except:
            print("Can not upload .bin file")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_upload_bin = False
    elif check_ser == True and check_bin == False:
        print("Can not upload .bin file")
        print("Can not find .bin file")
        
        print("")
        time.sleep(1.0)
        
        check_upload_bin = False
    elif check_ser == False and check_bin == True:
        print("Can not upload .bin file")
        print("Can not find serial port")
         
        print("")
        time.sleep(1.0)
         
        check_upload_bin = False
    else:
        print("Can not upload .bin file")
        print("Can not find both .bin file and serial port")
         
        print("")
        time.sleep(1.0)
         
        check_upload_bin = False
               
    return check_upload_bin  


def get_checksum(check_ser, ser, num_128):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            for_break = False
            crc_128_ack = np.uint32(0x00000000)
            for num in range(num_128):
                while ser.in_waiting > 0:
                    data_dummy = ser.read()
                    
                addr = 0x08000000 + (128 * num)
                request = b't0115%08x7f\r' % addr
                ser.write(request) 
                print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
                time.sleep(0.01)
                
                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        #print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                print("Read Memory 0x%08x - 0x%08x Request Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_get_checksum = True
                                
                                break
                            elif response == b't01111f\r':
                                print("Read Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_get_checksum = False
                                
                                break
                            else:
                                print("Read Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_get_checksum = False
                                
                                break
                    if time.time() >= prev_time + 1.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        for_break = True
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break
                    
                if for_break == True:
                    break
                    
                i = 0
                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        #print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response[0:5] == b't0118':
                                if len(response) == 22:
                                    for j in range(8):
                                        crc_128_ack = crc_128_ack + np.uint32(int(("0x%02s" % response[5+2*j:5+2*j+2].decode("utf-8")), 16))
                                    
                                    check_get_checksum = True
                                    
                                    print("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done, %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8"), num + 1, num_128))
                                else:
                                    for_break = True
                                    check_get_checksum = False
                                    
                                    print("Read Memory 0x%08x - 0x%08x Failed (Missing data), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            else:
                                for_break = True
                                check_get_checksum = False
                                
                                print("Read Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            
                            response = b''
                            prev_time = time.time()
                            
                            i = i + 1
                            if i == 16:
                                break
                    if time.time() >= prev_time + 1.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        for_break = True
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break
                    
                if for_break == True:
                    break
                
                response = b''
                prev_time = time.time()
                while True:
                    if ser.in_waiting > 0:
                        data_rx = ser.read()
                        #print(data_rx)
                        response = response + data_rx
                        if data_rx == b'\r':
                            print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                            if response == b't011179\r':
                                print("Read Memory 0x%08x - 0x%08x Response Done (ACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_get_checksum = True
                                
                                break
                            elif response == b't01111f\r':
                                print("Read Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_get_checksum = False
                                
                                break
                            else:
                                print("Read Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                for_break = True
                                check_get_checksum = False
                                
                                break
                    if time.time() >= prev_time + 1.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        for_break = True
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break
                    
                if for_break == True:
                    break
                    
                time.sleep(0.01)
            
            if check_get_checksum == True:
                print("Got checksum (0x%08x - 0x%08x): 0x%08x, %d bytes" % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack, (num_128 * 128)))
            else:
                print("Can not get checksum")
            
            print("")
            time.sleep(1.0)         
        except:
            print("Can not get checksum")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
    else:
        print("Can not get checksum")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_get_checksum = False
        crc_128_ack = np.uint32(0x00000000)
                
    return check_get_checksum, crc_128_ack       
 
    
def verify_checksum(crc_128, crc_128_ack):
    if crc_128 == crc_128_ack:
        print("Checksum matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))
        
        print("")
        time.sleep(1.0)
     
        check_verify_checksum = True
    else:
        print("Checksum not matched (.bin file: 0x%08x, Memory: 0x%08x)" % (crc_128, crc_128_ack))
        
        print("")
        time.sleep(1.0)
        
        check_verify_checksum = False
        
    return check_verify_checksum


def exit_bootloader_mode(check_ser, ser):
    if check_ser == True:
        try:
            request = b't09780000000000000000\r'
            for i in range(10):
                ser.write(request) 
                time.sleep(0.05)
            print("Sent: %s\\r" % request[0:-1].decode("utf-8"))
            time.sleep(0.01)
                
            while ser.in_waiting > 0:
                data_dummy = ser.read()
    
            check_exit_bootloader_mode = True

            print("Exited Bootloader mode")

            print("")
            time.sleep(1.0)
        except:
            print("Can not exit Bootloader mode")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_exit_bootloader_mode = False
    else:
        print("Can not exit Bootloader mode")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_exit_bootloader_mode = False
                
    return check_exit_bootloader_mode


def input_exit_debug_mode():
    global exit_debug_mode_flag
    
    while True:
        if exit_debug_mode_flag == False:
            dummy_integer = input()
            exit_debug_mode_flag = True
            break
        
        
def get_debug_message(check_ser, ser):
    global exit_debug_mode_flag
    global debug_bytearray_list
    global ds3231_time_u32, ds3231_date_str
    global test_module1_u8_B0, test_module1_u8_B1, test_module1_u8_B7
    global test_module2_u8_B0, test_module2_u8_B1, test_module2_u8_B7
    exit_debug_mode_flag = False
    
    print("Press Enter to exit Debug mode")
    _thread.start_new_thread(input_exit_debug_mode, ())
    
    if check_ser == True:
        try:  
            check_get_debug_message = False
            
            response = b''
            prev_time = time.time()
            while True:
                if exit_debug_mode_flag == True:
                    print("Exited Debug mode")
                    
                    break
                
                if ser.in_waiting > 0:
                    data_rx = ser.read()
                    #print(data_rx)
                    response = response + data_rx
                    if data_rx == b'\r':
                        #print("Recv: %s\\r" % response[0:-1].decode("utf-8"))
                        if (response[0:4] == b't100') and (response[4:5] == b'8'):
                            if response[5:21] == b'0000000000000000':
                                print("Get Debug Message Done (Alive Message (ID 0x100))") 
                                prev_time = time.time()
                            else:
                                print("Get Debug Message Done (Unknown Alive Message (ID 0x100))")        
                            check_get_debug_message = True
                        elif (response[0:2] == b't2') and (response[4:5] == b'8'):
                            if (0x200 <= int("0x%s" % response[1:4].decode("utf-8"), 16)) and ((int("0x%s" % response[1:4].decode("utf-8"), 16) <= 0x20F)):
                                debug_bytearray_list[int("0x%s" % response[2:4].decode("utf-8"), 16)] = response[5:21]
                                if response[1:4] == b'200':
                                    ds3231_time_u32 = int("0x000000%s" % debug_bytearray_list[0][0:2].decode("utf-8"), 16) + int("0x0000%s00" % debug_bytearray_list[0][2:4].decode("utf-8"), 16) + int("0x00%s0000" % debug_bytearray_list[0][4:6].decode("utf-8"), 16) + int("0x%s000000" % debug_bytearray_list[0][6:8].decode("utf-8"), 16)
                                    ds3231_date_str = str(datetime.fromtimestamp(ds3231_time_u32))
                                    print("Get Debug Message Done (Data Message: Got DS3231 Data (ID 0x%s))" % response[1:4].decode("utf-8"))
                                    print("DS3231 Data: time_u32 = %d (%s)" % (ds3231_time_u32, ds3231_date_str))
                                elif response[1:4] == b'201':
                                    test_module1_u8_B0, test_module1_u8_B1, test_module1_u8_B7 = int("0x%s" % debug_bytearray_list[1][0:2].decode("utf-8"), 16), int("0x%s" % debug_bytearray_list[1][2:4].decode("utf-8"), 16), int("0x%s" % debug_bytearray_list[1][14:16].decode("utf-8"), 16)
                                    print("Get Debug Message Done (Data Message: Got TEST MODULE 1 Data (ID 0x%s))" % response[1:4].decode("utf-8"))
                                    print("TEST MODULE 1: B0 = %.3d, B1 = %.3d, B7 = %.3d" % (test_module1_u8_B0, test_module1_u8_B1, test_module1_u8_B7))
                                elif response[1:4] == b'202':
                                    test_module2_u8_B0, test_module2_u8_B1, test_module2_u8_B7 = int("0x%s" % debug_bytearray_list[2][0:2].decode("utf-8"), 16), int("0x%s" % debug_bytearray_list[2][2:4].decode("utf-8"), 16), int("0x%s" % debug_bytearray_list[2][14:16].decode("utf-8"), 16)
                                    print("Get Debug Message Done (Data Message: Got TEST MODULE 2 Data (ID 0x%s))" % response[1:4].decode("utf-8"))
                                    print("TEST MODULE 2: B0 = %.3d, B1 = %.3d, B7 = %.3d" % (test_module2_u8_B0, test_module2_u8_B1, test_module2_u8_B7))
                                else:
                                    print("Get Debug Message Done (Unknown Data Message (ID 0x%s))" % response[1:4].decode("utf-8"))    
                            else:
                                print("Get Debug Message Done (Unknown Data Message (ID 0x%s))" % response[1:4].decode("utf-8"))    
                            check_get_debug_message = True
                        elif (response[0:2] == b't3') and (response[4:5] == b'0'):
                            if (0x300 <= int("%s" % response[1:4].decode("utf-8"), 16)) and (int("%s" % response[1:4].decode("utf-8"), 16) <= 0x37F):
                                if response[1:4] == b'300':
                                    print("Get Debug Message Done (Instant Message: DS3231 said Hello! (ID 0x%s))" % response[1:4].decode("utf-8")) 
                                elif response[1:4] == b'301':
                                    print("Get Debug Message Done (Instant Message: TEST MODULE 1 said Hello (ID 0x%s))" % response[1:4].decode("utf-8")) 
                                elif response[1:4] == b'302':
                                    print("Get Debug Message Done (Instant Message: TEST MODULE 2 said Hello! (ID 0x%s))" % response[1:4].decode("utf-8")) 
                                else:
                                    print("Get Debug Message Done (Unknown Instant Message (ID 0x%s))" % response[1:4].decode("utf-8"))                                   
                            else:
                                print("Get Debug Message Done (Unknown Instant Message (ID 0x%s))" % response[1:4].decode("utf-8"))    
                            check_get_debug_message = True
                        else:
                            print("Get Debug Message Failed (Incorrect Message Format (ID 0x%s))" % response[1:4].decode("utf-8"))
                            check_get_debug_message = False
                            
                        response = b''
                            
                if time.time() >= prev_time + 5.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Get Debug Message Failed (Timeout)")

                    check_get_debug_message = False
                                        
                    break
            
            print("")
            time.sleep(1.0)

        except:
            print("Can not get Debug Message")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(1.0)
            
            check_get_debug_message = False
    else:
        print("Can not get Debug Message")
        print("Can not find serial port")
        
        print("")
        time.sleep(1.0)
        
        check_get_debug_message = False
    
    exit_debug_mode_flag = True
            
    return check_get_debug_message    


def main_func(bin_file, port, skip_checksum):
    check_bin, contents, crc, num_128, crc_128 = read_bin(bin_file)
    global usb_state
    usb_state = True

    if check_bin == False:
        print("Failed to upload .bin file (read_bin)") 
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    check_ser, ser = open_serial(port)

    if check_ser == False:
        print("Failed to upload .bin file (open_serial)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    check_ser = check_serial(check_ser, ser)
    if check_ser == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to upload .bin file (check_serial)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False

    check_enter_bootloader_mode = enter_bootloader_mode(check_ser, ser)
    if check_enter_bootloader_mode == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to enter Bootloader mode")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    check_check_hse_frequency, check_check_hse_frequency_opt = check_hse_frequency(check_ser, ser)
    if check_check_hse_frequency == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to upload .bin file (check_hse_frequency)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    check_get_id, chip_id = get_ID(check_ser, ser)
    if check_get_id == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to upload .bin file (check_get_id)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    #check_erase_memory = erase_memory(check_ser, ser)
    #if check_erase_memory == False:
    #    check_ser = close_serial(check_ser, ser)
    #    
    #    print("Failed to upload .bin file (erase_memory)")
    #    
    #    print("")
    #    time.sleep(1.0)
    #    
    #    return False

    for sector in range(8):
        check_erase_sector = erase_sector(check_ser, ser, sector)
        if check_erase_sector == False:
            check_ser = close_serial(check_ser, ser)
        
            print("Failed to upload .bin file (erase_sector %02d)" % sector)
        
            print("")
            time.sleep(1.0)

            usb_state = False
            return False

    check_upload_bin = upload_bin(check_ser, ser, check_bin, contents, num_128)
    if check_upload_bin == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to upload .bin file (upload_bin)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    if skip_checksum == False:
        check_get_checksum, crc_128_ack = get_checksum(check_ser, ser, num_128)
        if check_get_checksum == False:
            check_ser = close_serial(check_ser, ser)
            
            print("Failed to verify checksum (get_checksum)")
            
            print("")
            time.sleep(1.0)

            usb_state = False
            return False
        
        check_verify_checksum = verify_checksum(crc_128, crc_128_ack)
    else:
        print("Skipped checksum verification")
        
        print("")
        time.sleep(1.0)

    if skip_checksum == False:
        if check_verify_checksum == True:
            print("Successfully uploaded .bin file (Checksum matched)")
            
            print("")
            time.sleep(1.0)
        else:            
            print("Failed to upload .bin file (Checksum unmatched)")
            
            print("")
            time.sleep(1.0)
    else:        
        print("Successfully uploaded .bin file (Checksum verification skipped)")
        
        print("")
        time.sleep(1.0)

    check_exit_bootloader_mode = exit_bootloader_mode(check_ser, ser)
    if check_exit_bootloader_mode == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to exit Bootloader mode")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
        
    check_ser = close_serial(check_ser, ser)
    
    if skip_checksum == False:
        if check_verify_checksum == True:
            return True
        else:
            usb_state = False
            return False
    else:        
        return True
        



def main_func2(port):
    global exit_debug_mode_flag
    global usb_state
    usb_state = True

    check_ser, ser = open_serial(port)

    if check_ser == False:
        print("Failed to get debug message (open_serial)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False
    
    check_ser = check_serial(check_ser, ser)
    if check_ser == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to get debug message (check_serial)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False


    check_get_debug_message = get_debug_message(check_ser, ser)
    if check_get_debug_message == False:
        check_ser = close_serial(check_ser, ser)
        
        print("Failed to get debug message (get_debug_message)")
        
        print("")
        time.sleep(1.0)

        usb_state = False
        return False

    check_ser = close_serial(check_ser, ser)
    
    return True
        
    
# check_main_func = main_func(bin_file, port, skip_checksum)
# check_main_func2 = main_func2(port)