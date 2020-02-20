import blynklib

BLYNK_AUTH = '9AWNZz9pwrE_RpQq8hrX_moi_g1spJzk'
blynk = blynklib.Blynk(BLYNK_AUTH)
a=[1,2,3,'564']

# register handler for virtual pin V4 write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    blynk.virtual_write(1,a[1])
    blynk.virtual_write(2,a[3])
###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()


###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()