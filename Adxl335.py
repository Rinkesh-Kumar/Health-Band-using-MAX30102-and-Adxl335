
# Import the ADS1x15 module.
import Adafruit_ADS1x15
import numpy as np
import pandas as pd
import time
import joblib
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

class Physical_Detection():
    def __init__(self):
        pass
    def estimate_physical_state(self):
        value = []
        X = adc.read_adc(1, gain=GAIN)
        Y = adc.read_adc(2, gain=GAIN)
        Z = adc.read_adc(3, gain=GAIN)
        value=[X,Y,Z]
        value=np.array(value)
        df=pd.DataFrame(value.reshape(1,-1),columns=['X','Y','Z'])
        scaler=joblib.load('Scaler.pkl')
        scaled_f=scaler.transform(df)
        knn=joblib.load('Model.pkl')
        pred=knn.predict(scaled_f)
        return [X,Y,Z,pred]
