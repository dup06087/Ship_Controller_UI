# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023

@author: USER
"""

#python C:\Users\USER\Desktop\STM32\upload_bin_func.py


import os
import sys
import serial
import time
import numpy as np


port = 'COM4'
#bin_file = "C:/Users/USER/Desktop/STM32/BIN.bin"
bin_file = "C:/Users/USER/Desktop/STM32/BIN2_F413ZH.bin"
#bin_file = os.path.join(sys.path[0], "BIN.bin")


def read_bin(bin_file):
    try:
        with open(bin_file, "rb") as f:
            contents = f.read()
        
        print("Found .bin file (%s)" % bin_file)    
        time.sleep(3.0)   
        
            
        #for i in range(len(contents) // 16):
        #    print('0x%08x: 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x 0x%02x%02x%02x%02x' % (16*i, contents[16*i + 3], contents[16*i + 2], contents[16*i + 1], contents[16*i + 0], contents[16*i + 7], contents[16*i + 6], contents[16*i + 5], contents[16*i + 4], contents[16*i + 11], contents[16*i + 10], contents[16*i + 9], contents[16*i + 8], contents[16*i + 15], contents[16*i + 14], contents[16*i + 13], contents[16*i + 12]))
        #if len(contents) % 16 != 0:
        #    temp = ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
        #    for i in range(16):
        #        if (len(contents) // 16) * 16 + i < len(contents):
        #            temp[i] = '%02x' % contents[(len(contents) // 16) * 16 + i]
        #    print('0x%08x: 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s 0x%02s%02s%02s%02s' % ((len(contents) // 16) * 16, temp[3], temp[2], temp[1], temp[0], temp[7], temp[6], temp[5], temp[4], temp[11], temp[10], temp[9], temp[8], temp[15], temp[14], temp[13], temp[12]))
        
        for i in range(len(contents) // 16):
            print('0x%08x: 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x' % (16*i, contents[16*i + 0], contents[16*i + 1], contents[16*i + 2], contents[16*i + 3], contents[16*i + 4], contents[16*i + 5], contents[16*i + 6], contents[16*i + 7], contents[16*i + 8], contents[16*i + 9], contents[16*i + 10], contents[16*i + 11], contents[16*i + 12], contents[16*i + 13], contents[16*i + 14], contents[16*i + 15]))
        if len(contents) % 16 != 0:
            temp = ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
            for i in range(16):
                if (len(contents) // 16) * 16 + i < len(contents):
                    temp[i] = '%02x' % contents[(len(contents) // 16) * 16 + i]
            print('0x%08x: 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s' % ((len(contents) // 16) * 16, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]))
        print("")
        
        
        #crc = 0x00000000
        #for i in range(len(contents)):
        #    crc = crc + int(('0x%02x' % contents[i]), 16)
        #    crc = crc & 0xffffffff       
        #print('Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, len(contents) - 1, crc, len(contents)))
            
        crc = np.uint32(0x00000000)
        for i in range(len(contents)):
            crc = crc + np.uint32(int(('0x%02x' % contents[i]), 16))     
        print('Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, len(contents) - 1, crc, len(contents)))
        
        
        if len(contents) % 128 == 0:
            num_128 = len(contents) // 128
        else:
            num_128 = (len(contents) // 128) + 1
            
        #crc_128 = 0x00000000
        #for i in range(num_128 * 128):
        #    if i < len(contents):
        #        crc_128 = crc_128 + int(('0x%02x' % contents[i]), 16)
        #    else:
        #        crc_128 = crc_128 + int(('0x%02x' % 0xff), 16)
        #    crc_128 = crc_128 & 0xffffffff  
        #print('Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))
        
        crc_128 = np.uint32(0x00000000)
        for i in range(num_128 * 128):
            if i < len(contents):
                crc_128 = crc_128 + np.uint32(int(('0x%02x' % contents[i]), 16))     
            else:
                crc_128 = crc_128 + np.uint32(int(('0x%02x' % 0xff), 16))     
        print('Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))

        print("")
        time.sleep(3.0)
        
        return True, contents, crc, num_128, crc_128
    except:
        print("Can not find .bin file (%s)" % bin_file)
        
        print("")
        time.sleep(3.0)
        
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


def close_serial(check_ser, ser):
    if check_ser == True:
        try:
            ser.close()
            
            print("Closed %s" % ser.port)
            
            print("")
            time.sleep(1.0)
        except:
            print("Can not close serial port")
            
            print("")
            time.sleep(1.0)
    else:
        print("Can not found serial port")
        
        print("")
        time.sleep(1.0)
        
    return check_ser
            

def check_hse_frequency(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
            request = b't079100\r'
            for i in range(10):
                ser.write(request) 
                time.sleep(0.1)
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
                if time.time() >= prev_time + 3.0:
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
            time.sleep(3.0)
        except:
            print("Can not check HSE frequency")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(3.0)
            
            check_check_hse_frequency = False
            check_check_hse_frequency_opt = False
    else:
        print("Can not check HSE frequency")
        print("Can not find serial port")
        
        print("")
        time.sleep(3.0)
        
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
                if time.time() >= prev_time + 3.0:
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
                            else:
                                print("Get ID Done (ID: 0x%03s)" % response[6:9].decode("utf-8"))
                                
                                chip_id = int(("0x%03s" % response[6:9].decode("utf-8")), 16)
                                
                                break
                        else:
                            print("Get ID Failed (Unknown)")
                            
                            chip_id = 0x000
                            
                            break
                if time.time() >= prev_time + 3.0:
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
                if time.time() >= prev_time + 3.0:
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
                print("Can not get ID")
            
            print("")
            time.sleep(3.0)
        except:
            print("Can not get Chip ID")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(3.0)
            
            check_id = False
            chip_id = 0x000
    else:
        print("Can not get Chip ID")
        print("Can not find serial port")
        
        print("")
        time.sleep(3.0)
        
        check_id = False
        chip_id = 0x000
                
    return check_id, chip_id    


def erase_memory(check_ser, ser):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
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
                            
                            check_erase = False
                            
                            break
                        else:
                            print("Erase Memory Request Failed (Unknown)")
                            
                            check_erase = False
                            
                            break
                if time.time() >= prev_time + 30.0:
                    print("Recv: %s" % response[0:].decode("utf-8"))
                    print("Erase Memory Request Failed (Timeout)")
                    
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
            
            if check_erase == True:
                print("Erased memory")
            else:
                print("Can not erase memory")
            
            print("")
            time.sleep(3.0)
        except:
            print("Can not erase memory")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(3.0)
            
            check_erase = False
    else:
        print("Can not erase memory")
        print("Can not find serial port")
        
        print("")
        time.sleep(3.0)
        
        check_erase = False
                
    return check_erase    
       
def upload_bin(check_ser, ser, check_bin, contents):
    if check_ser == True and check_bin == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
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
                                
                                check_upload_bin = False
                                
                                break
                            else:
                                print("Write Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_upload_bin = False
                                
                                break
                    if time.time() >= prev_time + 5.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        print("Write Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        
                        check_upload_bin = False
                        
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
                                    
                                    check_upload_bin = False
                                    
                                    break
                                else:
                                    print("Write Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                                    
                                    check_upload_bin = False
                                    
                                    break
                        if time.time() >= prev_time + 5.0:
                            print("Recv: %s" % response[0:].decode("utf-8"))
                            
                            check_upload_bin = False
                            
                            print("Write Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
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
                                
                                check_upload_bin = False
                                
                                break
                            else:
                                print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_upload_bin = False
                                
                                break
                    if time.time() >= prev_time + 5.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        
                        check_upload_bin = False
                        
                        break
                
                time.sleep(0.01)
                
            if check_upload_bin == True:
                print("Uploaded .bin file")
            else:
                print("Can not upload .bin file")
            
            print("")
            time.sleep(3.0)
        except:
            print("Can not upload .bin file")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(3.0)
            
            check_upload_bin = False
    elif check_ser == True and check_bin == False:
        print("Can not upload .bin file")
        print("Can not find .bin file")
        
        print("")
        time.sleep(3.0)
        
        check_upload_bin= False
    elif check_ser == False and check_bin == True:
        print("Can not upload .bin file")
        print("Can not find serial port")
         
        print("")
        time.sleep(3.0)
         
        check_upload_bin= False
    else:
        print("Can not upload .bin file")
        print("Can not find both .bin file and serial port")
         
        print("")
        time.sleep(3.0)
         
        check_upload_bin= False
               
    return check_upload_bin  


def get_checksum(check_ser, ser, num_128):
    if check_ser == True:
        try:
            while ser.in_waiting > 0:
                data_dummy = ser.read()
                
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
                                
                                check_get_checksum = False
                                
                                break
                            else:
                                print("Read Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_get_checksum = False
                                
                                break
                    if time.time() >= prev_time + 5.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
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
                                        crc_128_ack = crc_128_ack + np.uint32(int(('0x%02s' % response[5+2*j:5+2*j+2].decode("utf-8")), 16))
                                    
                                    check_get_checksum = True
                                    
                                    print("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done, %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8"), num + 1, num_128))
                                else:
                                    check_get_checksum = False
                                    
                                    print("Read Memory 0x%08x - 0x%08x Failed (Missing data), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            else:
                                check_get_checksum = False
                                
                                print("Read Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                            response = b''
                            i = i + 1
                            if i == 16:
                                break
                    if time.time() >= prev_time + 5.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
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
                                
                                check_get_checksum = False
                                
                                break
                            else:
                                print("Read Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                                
                                check_get_checksum = False
                                
                                break
                    if time.time() >= prev_time + 5.0:
                        print("Recv: %s" % response[0:].decode("utf-8"))
                        
                        check_get_checksum = False
                        
                        print("Read Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                        break
                    
                time.sleep(0.01)
            
            if check_get_checksum == True:
                print('got checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack, (num_128 * 128)))
            else:
                print("Can not get checksum")
            
            print("")
            time.sleep(3.0)         
        except:
            print("Can not get checksum")
            print("Can not use %s" % ser.port)
            
            print("")
            time.sleep(3.0)
            
            check_get_checksum = False
            crc_128_ack = np.uint32(0x00000000)
    else:
        print("Can not get checksum")
        print("Can not find serial port")
        
        print("")
        time.sleep(3.0)
        
        check_get_checksum = False
        crc_128_ack = np.uint32(0x00000000)
                
    return check_get_checksum, crc_128_ack       
 
    
check_ser, ser = open_serial(port)

check_check_hse_frequency, check_check_hse_frequency_opt = check_hse_frequency(check_ser, ser)

check_get_id, chip_id = get_ID(check_ser, ser)

check_erase_memory = erase_memory(check_ser, ser)

check_bin, contents, crc, num_128, crc_128 = read_bin(bin_file)

check_upload_bin = upload_bin(check_ser, ser, check_bin, contents)
check_get_checksum, crc_128_ack = get_checksum(check_ser, ser, num_128)

print('.bin file Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, len(contents) - 1, crc, len(contents)))
print('.bin file Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x00000000, (num_128 * 128) - 1, crc_128, (num_128 * 128)))
print('Memory Checksum (0x%08x - 0x%08x): 0x%08x, %d bytes' % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack, (num_128 * 128)))
print('')

check_ser = close_serial(check_ser, ser)
