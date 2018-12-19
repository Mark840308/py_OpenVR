import triad_openvr
import time
import sys
import socket
import threading

host, port = "127.0.0.1", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	v = triad_openvr.triad_openvr()
	if(len(v.object_names["Controller"]) >= 2):
		break
	print("\r" + "沒有找到足夠的tracker, 5秒後重試")
	time.sleep(5)
v.print_discovered_objects()
sock.bind((host, port))
sock.listen(5)

mylist = list()

def subThreadIn(conn, connNumber):
	mylist.append(conn)
	print("start thread")
	while True:
		try:
			txt = ""
			for each in v.devices["controller_1"].get_pose_euler():
				txt += "%.4f" % each
				txt += " "
			txt += "\n"
			for each in v.devices["controller_2"].get_pose_euler():
				txt += "%.4f" % each
				txt += " "
			txt += "\n"
			event = list()
			if(v.checkEvent(event)):
				txt += " ".join(event)
			print("\r" + txt, end="")
			conn.sendall(txt.encode("utf-8"))
			sleep_time = 1/60
			if sleep_time > 0:
				time.sleep(sleep_time)
		except (OSError, ConnectionResetError):
			try:
				mylist.remove(conn)
			except:
				pass
			conn.close()
			return

def main():
	while True:
		conn, addr = sock.accept()
		print('Connected with ' + addr[0] + ':' + str(addr[1]))
		try:
			mythread = threading.Thread(target=subThreadIn, args=(conn, conn.fileno()))
			mythread.setDaemon(True)
			mythread.start()
		except:
			pass

if __name__ == "__main__":
	main()