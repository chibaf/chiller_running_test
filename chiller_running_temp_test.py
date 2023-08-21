#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import matplotlib.pyplot as plt
import serial
import sys

ser = serial.Serial(
    port='/dev/ttyUSB0',  # ポート名は環境に合わせて変更
    baudrate=9600,
    timeout=1  # タイムアウトの設定
)

if len(sys.argv) ==2: # open an output file as name=sys.argv[1]
  f = open(sys.argv[1], "w")
temps=[0]*10
x=range(0, 10, 1)
request_00M1 = b'\x04\x30\x30\x4D\x31\x05'
while True:
  try:
    ser.write(request_00M1)
    time.sleep(1)
    line = ser.readline()  
    line2 = line.strip().decode("utf-8")
    line3 = line2.split( )    # split string
    temp=line3[1]
    temp=temp[:-2]   # remove the last two character
    temps.pop(-1)    # remove the last element
    temps.insert(0,float(temp)) # add element to the first position
    if len(sys.argv) ==2: # write data to file
      f.write(str(temps[0])+"\n")    
    print(str(temps[0]))      
    plt.clf()
    plt.plot(x,temps)
    plt.pause(0.1)
  except KeyboardInterrupt:
    print ('exiting')
    ser.close()
    if len(sys.argv) ==2: 
      f.close()
    break
exit()