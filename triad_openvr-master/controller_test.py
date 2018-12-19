import triad_openvr
import time
import sys

while True:
    v = triad_openvr.triad_openvr()
    if(len(v.object_names["Controller"]) >= 2):
        break
    print("\r" + "沒有找到足夠的tracker, 5秒後重試")
    time.sleep(5)
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    while(True):
        start = time.time()
        txt = ""
        for each in v.devices["controller_1"].get_pose_euler():
                txt += "%.4f" % each
                txt += " "
        txt += "\n"
        for each in v.devices["controller_2"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "
        print("\n" + txt, end="")
        event = list()
        if(v.checkEvent(event)):
            print(event)
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)