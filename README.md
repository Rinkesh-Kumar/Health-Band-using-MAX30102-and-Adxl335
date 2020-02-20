# Health band using MAX30102 and ADXL335

<p align="center">
  <img  src="https://i.postimg.cc/d1VsTm2s/IMG-20200220-201516.jpg">
</p>

The idea behind the project is to prepare a wrist worn device which could read vital signs such as Heart Rate and SpO2 remotely and Physical state such as Resting,Walking and Running. The targeted audience for this would be elderly people who needs constant monitoring. In this project we have used MAX30102 for Heart Rate and SpO2 measurment and ADXL335 for physical state detection and the data will be sent to anyone with the help of **Blynk**.
<p align="center">
<img src="https://i.postimg.cc/25CxyZNw/Screenshot-20200220-221756-Blynk.jpg" width="200"/> <img src="https://i.postimg.cc/26Kd09bc/Screenshot-20200220-221813-Blynk.jpg" width="200" /> 
<br>Blynk Application
</p>
We have chosen to use the Raspberry pi because of it's high computational power over arduino. As we want to implement Machine learning algorithms for physical state detection and estimation of HeartRate and SpO2 during motion as ppg signals are highly prone to motion artifacts.
We have divided the project into five parts.
<br>1. Heart Rate and SpO2 measurment under normal condition
<br>2. Physical State detection
<br>3. Fall detection and Alert on detection
<br>4. Sleep Tracking
<br>5. Heart Rate and SpO2 measurment under motion artifacts.

Since the Raspberry Pi does not have a built in Analog to Digital Converter, So we have used ADS1115 ADC.
### Connection
|  ADS1115 |ADXL335   |MAX30102   |Raspberry Pi 3   |
| ------------ | ------------ | ------------ | ------------ |
|VDD  | VCC  | VCC  | GPIO 01  |
|  GND |GND   |   GND| GPIO 09  |
| SDA  |   |  SDA |  GPIO 03 |
| SCL  |   |  SCL |  GPIO 05 |
| A1  |  X |   |   |
|  A2 |  Y |   |   |
|  A3 |  Z |   |   |
|   |   |  INT |  GPIO 07  | 

For Classification amongst the Physical state we have used KNN classifier.

Till now we have completed the first two parts i.e Heart rate adn SpO2 estimation under normal condition and Physical State Detection
