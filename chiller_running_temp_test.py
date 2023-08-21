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
temps=[0]*100
settemp=[25]*100
x=range(0, 100, 1)
S1_25=b'\x04\x30\x30\x02\x53\x31\x20\x20\x20\x20\x32\x35\x2E\x30\x03\x70'
S1_35=b'\x04\x30\x30\x02\x53\x31\x20\x20\x20\x20\x33\x35\x2E\x30\x03\x70'
request_00M1 = b'\x04\x30\x30\x4D\x31\x05'
flag=0
itime=0
temp0=25
while True:
  try:
    ser.write(request_00M1)
    if itime==20:
      if flag==0:
        temp0=25
        flag=1
        ser.write(S1_25)
      else:
        flag=0
        temp0=35
        ser.write(S1_35)
      itime=0
    else:
      itime=itime+1
    time.sleep(1)
    line = ser.readline()  
    line2 = line.strip().decode("utf-8")
    line3 = line2.split( )    # split string
    temp=line3[1]
    temp=temp[:-2]   # remove the last two character
    temps.pop(-1)    # remove the last element
    settemp.pop(-1)
    temps.insert(0,float(temp)) # add element to the first position
    settemp.insert(0,float(temp0))
    if len(sys.argv) ==2: # write data to file
      f.write(str(temps[0])+"\n")    
    print(str(temp0)+", "+str(temps[0]))      
    plt.clf()
    plt.plot(x,temps)
    plt.plot(x,settemp)
    plt.pause(0.1)
  except KeyboardInterrupt:
    print ('exiting')
    ser.close()
    if len(sys.argv) ==2: 
      f.close()
    break
exit()