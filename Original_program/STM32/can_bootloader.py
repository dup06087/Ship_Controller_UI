# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 22:31:21 2022

@author: USER
"""

#python C:\Users\USER\Desktop\STM32\can_bootloader.py


import serial
import time


ser = serial.Serial('COM5')
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
        print(data_rx)
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


addr = 0x08000000
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
                print("Read Memory 0x%08x - 0x%08x Request Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't01111f\r':
                print("Read Memory 0x%08x - 0x%08x Request Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Read Memory 0x%08x - 0x%08x Request Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Request Failed (Timeout)" % (addr, addr + 128 - 1))
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
                    print("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8")))
                else:
                    print("Read Memory 0x%08x - 0x%08x Failed (Missing data)" % (addr + (i*8), addr + ((i+1)*8) - 1))
            else:
                print("Read Memory 0x%08x - 0x%08x Failed (Unknown)" % (addr + (i*8), addr + ((i+1)*8) - 1))
            response = b''
            i = i + 1
            if i == 16:
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Failed (Timeout)" % (addr, addr + 128 - 1))
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
                print("Read Memory 0x%08x - 0x%08x Response Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't01111f\r':
                print("Read Memory 0x%08x - 0x%08x Response Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Read Memory 0x%08x - 0x%08x Response Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Response Failed (Timeout)" % (addr, addr + 128 - 1))
        break
    
print("")
time.sleep(1.0)


addr = 0x08000080
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
                print("Read Memory 0x%08x - 0x%08x Request Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't01111f\r':
                print("Read Memory 0x%08x - 0x%08x Request Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Read Memory 0x%08x - 0x%08x Request Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Request Failed (Timeout)" % (addr, addr + 128 - 1))
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
                    print("Read Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done" % (addr + (i*8), addr + ((i+1)*8) - 1, response[5:7].decode("utf-8"), response[7:9].decode("utf-8"), response[9:11].decode("utf-8"), response[11:13].decode("utf-8"), response[13:15].decode("utf-8"), response[15:17].decode("utf-8"), response[17:19].decode("utf-8"), response[19:21].decode("utf-8")))
                else:
                    print("Read Memory 0x%08x - 0x%08x Failed (Missing data)" % (addr + (i*8), addr + ((i+1)*8) - 1))
            else:
                print("Read Memory 0x%08x - 0x%08x Failed (Unknown)" % (addr + (i*8), addr + ((i+1)*8) - 1))
            response = b''
            i = i + 1
            if i == 16:
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Failed (Timeout)" % (addr, addr + 128 - 1))
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
                print("Read Memory 0x%08x - 0x%08x Response Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't01111f\r':
                print("Read Memory 0x%08x - 0x%08x Response Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Read Memory 0x%08x - 0x%08x Response Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Read Memory 0x%08x - 0x%08x Response Failed (Timeout)" % (addr, addr + 128 - 1))
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


addr = 0x08000000
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
                print("Write Memory 0x%08x - 0x%08x Request Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't03111f\r':
                print("Write Memory 0x%08x - 0x%08x Request Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Write Memory 0x%08x - 0x%08x Request Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Write Memory 0x%08x - 0x%08x Request Failed (Timeout)" % (addr, addr + 128 - 1))
        break
    
for i in range(0,16,1):
    request = b't0048'
    for j in range(8):
        request = request + (b'%02x' % (16*(0+(i//2)) + 8*(i%2) + j))
    request = request + b'\r'    
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
                    print("Write Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done (ACK)" % (addr + (i*8), addr + ((i+1)*8) - 1, request[5:7].decode("utf-8"), request[7:9].decode("utf-8"), request[9:11].decode("utf-8"), request[11:13].decode("utf-8"), request[13:15].decode("utf-8"), request[15:17].decode("utf-8"), request[17:19].decode("utf-8"), request[19:21].decode("utf-8")))
                    break
                elif response == b't03111f\r':
                    print("Write Memory 0x%08x - 0x%08x Failed (NACK)" % (addr + (i*8), addr + ((i+1)*8) - 1))
                    break
                else:
                    print("Write Memory 0x%08x - 0x%08x Failed (Unknown)" % (addr + (i*8), addr + ((i+1)*8) - 1))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
            print("Write Memory 0x%08x - 0x%08x Failed (Timeout)" % (addr + (i*8), addr + ((i+1)*8) - 1))
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
                print("Write Memory 0x%08x - 0x%08x Response Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't03111f\r':
                print("Write Memory 0x%08x - 0x%08x Response Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout)" % (addr, addr + 128 - 1))
        break

print("")
time.sleep(1.0)


addr = 0x08000080
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
                print("Write Memory 0x%08x - 0x%08x Request Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't03111f\r':
                print("Write Memory 0x%08x - 0x%08x Request Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Write Memory 0x%08x - 0x%08x Request Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Write Memory 0x%08x - 0x%08x Request Failed (Timeout)" % (addr, addr + 128 - 1))
        break
        
for i in range(0,16,1):
    request = b't0048'
    for j in range(8):
        request = request + (b'%02x' % (16*(8+(i//2)) + 8*(i%2) + j))
    request = request + b'\r'    
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
                    print("Write Memory 0x%08x - 0x%08x (0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s 0x%02s) Done (ACK)" % (addr + (i*8), addr + ((i+1)*8) - 1, request[5:7].decode("utf-8"), request[7:9].decode("utf-8"), request[9:11].decode("utf-8"), request[11:13].decode("utf-8"), request[13:15].decode("utf-8"), request[15:17].decode("utf-8"), request[17:19].decode("utf-8"), request[19:21].decode("utf-8")))
                    break
                elif response == b't03111f\r':
                    print("Write Memory 0x%08x - 0x%08x Failed (NACK)" % (addr + (i*8), addr + ((i+1)*8) - 1))
                    break
                else:
                    print("Write Memory 0x%08x - 0x%08x Failed (Unknown)" % (addr + (i*8), addr + ((i+1)*8) - 1))
                    break
        if time.time() >= prev_time + 5.0:
            print("Recv: %s" % response[0:].decode("utf-8"))
            print("Write Memory 0x%08x - 0x%08x Failed (Timeout)" % (addr + (i*8), addr + ((i+1)*8) - 1))
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
                print("Write Memory 0x%08x - 0x%08x Response Done (ACK)" % (addr, addr + 128 - 1))
                break
            elif response == b't03111f\r':
                print("Write Memory 0x%08x - 0x%08x Response Failed (NACK)" % (addr, addr + 128 - 1))
                break
            else:
                print("Write Memory 0x%08x - 0x%08x Response Failed (Unknown)" % (addr, addr + 128 - 1))
                break
    if time.time() >= prev_time + 5.0:
        print("Recv: %s" % response[0:].decode("utf-8"))
        print("Write Memory 0x%08x - 0x%08x Response Failed (Timeout)" % (addr, addr + 128 - 1))
        break

print("")
time.sleep(1.0)


ser.close()