# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 14:38:33 2023

@author: USER
"""

#python C:\Users\USER\Desktop\STM32\read_bin.py


import os, sys
import numpy as np


#with open("C:/Users/USER/Desktop/STM32/BIN.bin", "rb") as f:
with open("C:/Users/USER/Desktop/STM32/BIN_F413ZH.bin", "rb") as f:
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