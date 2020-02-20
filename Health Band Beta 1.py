''' The Sampling rate is 8 '''
#Importing Libraries

import numpy as np
from scipy.signal import butter,lfilter
from scipy.signal import find_peaks,argrelextrema
import max301021
from datetime import datetime
import RPi.GPIO as GPIO
import Adxl335
state=Adxl335.Physical_Detection()
import blynklib
import Temperature
import time
#defining Token for Blynk
auth_tokken='9AWNZz9pwrE_RpQq8hrX_moxxxxxxxx'
blynk=blynklib.Blynk(auth_tokken)
temp=Temperature.Temperature()
#Defining the Butter Bandpass filter
def butter_bandpass(lowcut,highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high= highcut/ nyq
    b, a = butter(order,[low,high], btype='bandpass')
    return b, a

def butter_bandpass_filter(data, lowcut,highcut, fs, order=5):
    b, a = butter_bandpass(lowcut,highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
m=max301021.MAX30102()
red1=[]
ir1=[]
i=0
while(True):
    # Getting the temperature
    temp_c=temp.getTemperature()
    temp_f=temp_c*1.8+32
    print(temp_c)
    temp_c=round(temp_c,2)
    temp_f=round(temp_f,2)
    temp_r=str(temp_c)+'°C/'+str(temp_f)+'°F'
    # Establishing connection with Blynk server
    blynk.run()
    blynk.virtual_write(2,temp_r)
    params=state.estimate_physical_state()
    print(params[3][0])
    while(GPIO.input(m.interrupt) == 1):
    # wait for interrupt signal, which means the data is available
    # do nothing here
        pass
    blynk.virtual_write(1,params[3][0])
    red, ir = m.read_fifo()
    #Checking for no finger or motion 
    if red<=3000 or ir<=3000 or (params[3][0]=='Walking' or params[3][0]=='Running):
        red1=[]
        ir1=[]
        print("No Heart beat detected")
        blynk.virtual_write(3,'Waiting')
        blynk.virtual_write(4,'Waiting')
    elif red > 3000 and ir > 3000 and len(red1)<80 and len(ir1)<80 and params[3][0]=='Resting':
        red1.append(red)
        ir1.append(ir)
        print("Wait I am calculating")

    elif len(red1)==80 and len(ir1)==80:
        print("Calculating")
        red1=np.array(red1)
        ir1=np.array(ir1)
        #Filtering
        red_sample=butter_bandpass_filter(red1[:],0.83,2.2,8,6)
        ir_sample=butter_bandpass_filter(ir1[:],0.83,2.2,8,6)

        #Finding the Heart Rate peaks
        peaks_red=find_peaks(red_sample)
        peaks_ir=find_peaks(ir_sample)
        print("Heart Rate is --->")
        # Taking the average of both LEDs
        print((len(peaks_ir[0])*6+len(peaks_red[0])*6)//2)
        hr=str((len(peaks_ir[0])*6+len(peaks_red[0])*6)//2)+' bpm'
        blynk.virtual_write(3,hr)
        #Estimating SPO2
        # Calculating the AC values of IR and Red PPG signal
        red_locmax=argrelextrema(red1,np.greater)
        red_locmin=argrelextrema(red1,np.less)
        ir_locmax=argrelextrema(ir1,np.greater)
        ir_locmin=argrelextrema(ir1,np.less)
        red_locmax=red_locmax[0][7:]
        red_locmin=red_locmin[0][7:]
        ir_locmax=ir_locmax[0][7:]
        ir_locmin=ir_locmin[0][7:]
        red_ac=0
        ir_ac=0
        for i in range (min(len(red_locmax),len(red_locmin))):
            if red1[red_locmax[i]]-red1[red_locmin[i]] > red_ac:
                red_ac=red1[red_locmax[i]]-red1[red_locmin[i]]
        for i in range (min(len(ir_locmax),len(ir_locmin))):
            if ir1[ir_locmax[i]]-ir1[ir_locmin[i]] > ir_ac:
                ir_ac=ir1[ir_locmax[i]]-ir1[ir_locmin[i]]
        # Calculating the DC value of IR and Red PPG signal
        red_dc=np.mean(red1)
        ir_dc=np.mean(ir1)
        num=red_ac*ir_dc
        den=ir_ac*red_dc
        r=num/den
        # Formula for conversion of ratio to SpO2 percentage as given by MAX30102 Official Arduino Library
        spo2=(-45.060)*(r**2)+(30.054)*r+94.845
        print("Oxygen Content in blood is :")
        print(round(spo2,2))
        sp=str(round(spo2,2))+' % Oxygen'
        blynk.virtual_write(4,sp)
        ir1=ir1.tolist()
        red1=red1.tolist()
        ir1.pop(0)
        red1.pop(0)
        
