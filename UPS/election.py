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
				ElectionThread2("sender", "coordinator").start()
			if ElectionThread2.received and not ElectionThread2.leader_flag:
				ElectionThread2.election = False
				ElectionThread2.received = False
				ElectionThread2("sender", "election").start()
		elif self.operation == "timerok":
			while True:
				if not ElectionThread2.leader_flag and time.time() > (5000 + (5000 * (4570 - ElectionThread2.port))):
					ElectionThread2.ok_ctr = 0
					ElectionThread2("sender", "election").start()
					break
		elif self.operation == "receiver":
			recvsocket = socket.socket()
			while True:
				recvsocket.listen()
				recvsocket.accept()
				print("Connection established.....")
				option = recvsocket.recv(1024)
				if option == b"election":
					ElectionThread2.source_address = int(recvsocket.recv())
					if ElectionThread2.port > ElectionThread2.source_address:
						ElectionThread2("sender", "ok").start()
					if not ElectionThread2.election:
						ElectionThread2("sender", "election").start()
						ElectionThread2.election = True
						ElectionThread2("timer").start()
				elif option == b"ok":
					ElectionThread2.received = True
					recvsocket.recv()
				elif option == b"cordinator":
					ElectionThread2.leader_id = recvsocket.recv()
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
					scmsocket.send(b"coordinator")
					scmsocket.send(ElectionThread2.port)
					print("Sent Leader ID to :", address)
				except:
					print("The process ", address, " has failed, won't get the new leader !")

	def sendOK():
		try:
			sosocket = socket.socket()
			sosocket.connect(ElectionThread2.source_address)
			sosocket.send(b"ok")
			sosocket.send(ElectionThread2.port)
			print("sendOK succeeded")
		except:
			print("sendOK failed")

	def sendElectionRequest():
		fails = 0
		for address in ElectionThread2.network:
			if address[1] > ElectionThread2.self_id:
				try:
					sersocket = socket.socket()
					sersocket.connect(address)
					sersocket.send(b"election")
					sersocket.send(ElectionThread2.port)
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
