import time

from DobotSerialInterface import DobotSerialInterface

#sudo chmod 777 /dev/ttyACM0
# run line above in terminal before running this code

port='/dev/ttyACM0'

dobot_interface = DobotSerialInterface(port)
dobot_interface.set_speed()
dobot_interface.set_playback_config()



time.sleep(0.1)
readangle=dobot_interface.current_status.angles
print(readangle)

time.sleep(1)
dobot_interface.send_absolute_angles(0,0,0,0)
time.sleep(3)
dobot_interface.send_absolute_angles(-30,0,0,0)
time.sleep(3)
# for i in range(100):
#     dobot_interface.send_absolute_angles(30,0,0,0)
#     time.sleep(0.1)
# time.sleep(5)
dobot_interface.send_absolute_angles(0,0,0,0)
time.sleep(3)
dobot_interface.send_absolute_angles(0,20,20,0)
time.sleep(3)
dobot_interface.send_absolute_angles(0,0,0,0)


time.sleep(5)
