"""
Discovery
"""
import socket
import threading
import time
from typing import Any


class ElectionThread2(threading.Thread):
	def __init__(self, operation: str, reqtype: str = None):
		threading.Thread.__init__(self)
		self.operation = operation
		self.reqtype = reqtype

	def run(self) -> None:
		if self.operation == "timer":
			time.sleep(7)
			if not ElectionThread2.received:
				ElectionThread2.leader_id = ElectionThread2.self_id
				ElectionThread2.election = False
				ElectionThread2.leader_flag = True
				print("******I am the selected LEADER ! ", ElectionThread2.leader_id)
				ElectionThread2("sender", "coordinator").start()
			if ElectionThread2.received and not ElectionThread2.leader_flag:
				ElectionThread2.election = False
				ElectionThread2.received = False
				print("Received OK but LEADER HAS FAILED");
				ElectionThread2("sender", "election").start()
		elif self.operation == "timerok":
			while True:
				if not ElectionThread2.leader_flag and time.time() > (5000 + (5000 * (4570 - ElectionThread2.self_id))):
					ElectionThread2.ok_ctr = 0
					print("Higher Process Sent OK but Failed, so Start a new Election process")
					ElectionThread2("sender", "election").start()
					break
		elif self.operation == "receiver":
			recvsocket = socket.socket()
			recvsocket.bind(("0.0.0.0", ElectionThread2.self_id))
			while True:
				recvsocket.listen()
				recvsocket2 = recvsocket.accept()[0]
				print("Connection established.....")
				option, source = tuple(recvsocket2.recv(1024).decode("UTF-8").split(","))
				if option == "election":
					print("received election request")
					ElectionThread2.source_address = int(source)
					if ElectionThread2.self_id > ElectionThread2.source_address:
						ElectionThread2("sender", "ok").start()
					if not ElectionThread2.election:
						ElectionThread2("sender", "election").start()
						ElectionThread2.election = True
						ElectionThread2("timer").start()
				elif option == "ok":
					print("received ok")
					ElectionThread2.received = True
				elif option == "coordinator":
					print("received coordinator request")
					ElectionThread2.leader_id = int(source)
					ElectionThread2.leader_flag = True
					ElectionThread2.election_req = False
					ElectionThread2.received = False
					print("******LEADER selected is", ElectionThread2.leader_id)
			recvsocket.close()

		elif self.operation == "sender":
			if self.reqtype == "election":
				ElectionThread2.sendElectionRequest()
			elif self.reqtype == "ok":
				ElectionThread2.sendOK()
			elif self.reqtype == "coordinator":
				ElectionThread2.sendCoordinatorMsg()

	def sendCoordinatorMsg():
		for address in ElectionThread2.network:
			if address[1] != ElectionThread2.self_id:
				try:
					scmsocket = socket.socket()
					scmsocket.connect(address)
					scmsocket.send(("coordinator," + str(ElectionThread2.self_id)).encode("UTF-8"))
					print("Sent Leader ID to :", address)
				except:
					print("The process ", address, " has failed, won't get the new leader !")

	def sendOK():
		try:
			sosocket = socket.socket()
			sosocket.connect(("127.0.0.1", ElectionThread2.source_address))
			sosocket.send(("ok," + str(ElectionThread2.self_id)).encode("UTF-8"))
			print("Sent OK to : ", ElectionThread2.source_address)
		except:
			print("Process ", ElectionThread2.source_address, " has FAILED. OK Message cannot be sent !")

	def sendElectionRequest():
		fails = 0
		for address in ElectionThread2.network:
			if address[1] > ElectionThread2.self_id:
				try:
					sersocket = socket.socket()
					sersocket.connect(address)
					sersocket.send(("election," + str(ElectionThread2.self_id)).encode("UTF-8"))
					print("Sent Election Request to : " + address)
				except:
					print("The process :", address, " has FAILED, cannot send Election Request !")
					fails += 1
		if fails == ElectionThread2.higher:
			if not ElectionThread2.election:
				print("Inside if of sendElectionRequest")
				ElectionThread2.election = True
				ElectionThread2.received = False
				ElectionThread2("timer").start()


ElectionThread2.leader_id = -1
ElectionThread2.election = False
ElectionThread2.leader_flag = False
ElectionThread2.received = False
