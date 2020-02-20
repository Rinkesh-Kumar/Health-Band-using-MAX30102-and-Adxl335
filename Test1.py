import Adxl335
state=Adxl335.Physical_Detection()
a=state.estimate_physical_state()
print(a)