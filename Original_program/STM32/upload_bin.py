# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023

@author: USER
"""

#python C:\Users\USER\Desktop\STM32\upload_bin.py


import os
import sys
import serial
import time
import numpy as np


with open("C:/Users/USER/Desktop/STM32/BIN.bin", "rb") as f:
#with open(os.path.join(sys.path[0], "BIN.bin"), "rb") as f:
    contents = f.read()
   
    
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
      

#crc = 0x00000000
#for i in range(len(contents)):
#    crc = crc + int(('0x%02x' % contents[i]), 16)
#    crc = crc & 0xffffffff       
#print('Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, len(contents) - 1, crc))
    
crc = np.uint32(0x00000000)
for i in range(len(contents)):
    crc = crc + np.uint32(int(('0x%02x' % contents[i]), 16))     
print('Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, len(contents) - 1, crc))


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
#print('Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, (num_128 * 128) - 1, crc_128))

crc_128 = np.uint32(0x00000000)
for i in range(num_128 * 128):
    if i < len(contents):
        crc_128 = crc_128 + np.uint32(int(('0x%02x' % contents[i]), 16))     
    else:
        crc_128 = crc_128 + np.uint32(int(('0x%02x' % 0xff), 16))     
print('Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, (num_128 * 128) - 1, crc_128))

print("")
time.sleep(1.0)


ser = serial.Serial('COM7')
ser.baudrate = 115200


request = b't07980000000000000000\r'
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
            if response == b't079179\r':
                print("Check HSE frequency Response Done (ACK)") 
                break
            elif response == b't07911f\r':
                print("Check HSE frequency Response Failed (NACK)")
                break
            else:
                print("Check HSE frequency Response Failed (Unknown)")
                break
    if time.time() >= prev_time + 3.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Check HSE frequency Response Failed (Timeout)")
        break
    
print("")
time.sleep(1.0)


request = b't00280000000000000000\r'
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
                break
            elif response == b't00211f\r':
                print("Get ID Request Failed (NACK)")
                break
            else:
                print("Get ID Request Failed (Unknown)")
                break
    if time.time() >= prev_time + 3.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Get ID Request Failed (Timeout)")
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
                    break
                else:
                    print("Get ID Done (ID: 0x%03s)" % response[6:9].decode("utf-8"))
                    break
            else:
                print("Get ID Failed (Unknown)")
                break
    if time.time() >= prev_time + 3.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Get ID Failed (Timeout)")
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
                break
            elif response == b't00211f\r':
                print("Get ID Response Failed (NACK)")
                break
            else:
                print("Get ID Response Failed (Unknown)")
                break
    if time.time() >= prev_time + 3.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Get ID Response Failed (Timeout)")
        break

print("")
time.sleep(1.0)


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
                break
            elif response == b't04311f\r':
                print("Erase Memory Request Failed (NACK)")
                break
            else:
                print("Erase Memory Request Failed (Unknown)")
                break
    if time.time() >= prev_time + 20.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Erase Memory Request Failed (Timeout)")
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
                break
            elif response == b't04311f\r':
                print("Erase Memory Response Failed (NACK)")
                break
            else:
                print("Erase Memory Response Failed (Unknown)")
                break
    if time.time() >= prev_time + 20.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Erase Memory Response Failed (Timeout)")
        break

print("")
time.sleep(1.0)


for num in range(num_128):
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
                    break
                elif response == b't03111f\r':
                    print("Write Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
                else:
                    print("Write Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
            print("Write Memory 0x%08x - 0x%08x Request Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
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
                        break
                    elif response == b't03111f\r':
                        print("Write Memory 0x%08x - 0x%08x Failed (NACK), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                        break
                    else:
                        print("Write Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                        break
            if time.time() >= prev_time + 5.0:
                print("Recv: %s" % response[0:].decode("utf-8"))
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
                    break
                elif response == b't03111f\r':
                    print("Write Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
                else:
                    print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
            print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
            break
    
    time.sleep(0.01)
    
print("")
time.sleep(1.0)


crc_128_ack = np.uint32(0x00000000)
for num in range(num_128):
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
                    break
                elif response == b't01111f\r':
                    print("Read Memory 0x%08x - 0x%08x Request Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
                else:
                    print("Read Memory 0x%08x - 0x%08x Request Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
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
                        print("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done, %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8"), num + 1, num_128))
                    else:
                        print("Read Memory 0x%08x - 0x%08x Failed (Missing data), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                else:
                    print("Read Memory 0x%08x - 0x%08x Failed (Unknown), %04d / %04d" % (addr + (i*8), addr + ((i+1)*8) - 1, num + 1, num_128))
                response = b''
                i = i + 1
                if i == 16:
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
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
                    break
                elif response == b't01111f\r':
                    print("Read Memory 0x%08x - 0x%08x Response Failed (NACK), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
                else:
                    print("Read Memory 0x%08x - 0x%08x Response Failed (Unknown), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
            print("Read Memory 0x%08x - 0x%08x Response Failed (Timeout), %04d / %04d" % (addr, addr + 128 - 1, num + 1, num_128))
            break
        
    time.sleep(0.01)
    
print("")
time.sleep(1.0)


print('BIN file Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, len(contents) - 1, crc))
print('BIN file Checksum (0x%08x - 0x%08x): 0x%08x' % (0x00000000, (num_128 * 128) - 1, crc_128))
print('Flash Memory Checksum (0x%08x - 0x%08x): 0x%08x' % (0x08000000, 0x08000000 + (num_128 * 128) - 1, crc_128_ack))


ser.close()