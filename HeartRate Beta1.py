#Importing Libraries

import numpy as np
from scipy.signal import butter,lfilter
from scipy.signal import find_peaks
import max301021
import datetime
import RPi.GPIO as GPIO
import Adxl335
state=Adxl335.Physical_Detection()
import blynklib
auth_tokken='9AWNZz9pwrE_RpQq8hrX_moi_g1spJzk'
#auth_tokken='jd2eASXMvWd16IAUBJW9KKH15SImdMVQ'
blynk=blynklib.Blynk(auth_tokken)
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
    blynk.run()
    params=state.estimate_physical_state()
    print(params[3][0])
    while(GPIO.input(m.interrupt) == 1):
    # wait for interrupt signal, which means the data is available
    # do nothing here
        pass
    blynk.virtual_write(2,params[3][0])
    red, ir = m.read_fifo()
    if red<=3000 and ir<=3000 or (params[3]=='Running' or params[3]=='Walking'):
        red1=[]
        ir1=[]
        print("No Heart beat detected")
        blynk.virtual_write(1,'No beats')
    elif red > 3000 and ir > 3000 and len(red1)<250 and len(ir1)<250 and (params[3]=='Resting'):
        red1.append(red)
        ir1.append(ir)
        print("Wait I am calculating")
        blynk.virtual_write(1,'Calculating')

    elif len(red1)==250 and len(ir1)==250:
        print("Calculating")
        #Filtering
        red_sample=butter_bandpass_filter(red1[:],0.83,3.3,25,6)
        ir_sample=butter_bandpass_filter(ir1[:],0.83,3.3,25,6)

        #Finding the Heart Rate peaks
        peaks_red=find_peaks(red_sample)
        print("Red Light HR is:->")
        print(len(peaks_red[0])*6)
        peaks_ir=find_peaks(ir_sample)
        print("IR Light HR is -->")
        print(len(peaks_ir[0])*6)
        hr=str(len(peaks_ir[0])*6)+'bpm'
        blynk.virtual_write(1,hr)
    elif len(red1)>250 and len(ir1)>250:
        print('Exceeded')
        ir1.pop(0)
        red1.pop(0)