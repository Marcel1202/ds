"""
Discovery
"""
import socket
import threading
import time


class ElectionThread(threading.Thread):
	"""
	Election Thread
	"""

	def __init__(self, operation: str, message: str = None):
		threading.Thread.__init__(self)
		self.operation = operation
		self.message = message

	def run(self) -> None:
		"""
		Run
		"""
		if self.operation == "timer":
			time.sleep(7)
			if not ElectionThread.received:
				ElectionThread.election = False
				ElectionThread.has_leader = True
				ElectionThread.leader_IP = ElectionThread.IP
				ElectionThread.leader_port = ElectionThread.port
				ElectionThread("sender", "coordinator").start()
			if ElectionThread.received and not ElectionThread.has_leader:
				ElectionThread.election = False
				ElectionThread.received = False
				ElectionThread("sender", "election").start()
		elif self.operation == "receiver":
			recvsocket = socket.socket()
			recvsocket.bind(("0.0.0.0", ElectionThread.port))
			while True:
				recvsocket.listen()
				recvsocket2, source_address = recvsocket.accept()
				message, sender_port = tuple(recvsocket2.recv(1024).decode("UTF-8").split(","))
				if message == "election":
					ElectionThread.election_source_IP = source_address[0]
					ElectionThread.election_source_port = int(sender_port)
					if ElectionThread.port > ElectionThread.election_source_port:
						ElectionThread("sender", "ok").start()
					if not ElectionThread.election:
						ElectionThread("sender", "election").start()
						ElectionThread.election = True
						ElectionThread("timer").start()
				elif message == "ok":
					ElectionThread.received = True
				elif message == "coordinator":
					ElectionThread.election = False
					ElectionThread.has_leader = True
					ElectionThread.leader_IP = source_address[0]
					ElectionThread.leader_port = int(sender_port)
					ElectionThread.received = False

		elif self.operation == "sender":
			if self.message == "election":
				ElectionThread.send_election()
			elif self.message == "ok":
				ElectionThread.send_ok()
			elif self.message == "coordinator":
				ElectionThread.send_coordinator()

	# noinspection PyMethodParameters
	def send_election():
		ElectionThread.higher = 0
		for address in ElectionThread.network:
			if address[1] > ElectionThread.port:
				ElectionThread.higher += 1

		fails = 0
		for address in ElectionThread.network:
			if address[1] > ElectionThread.port:
				try:
					sersocket = socket.socket()
					sersocket.connect(address)
					sersocket.send(("election," + str(ElectionThread.port)).encode("UTF-8"))
				except:
					fails += 1
		if fails == ElectionThread.higher:
			if not ElectionThread.election:
				ElectionThread.election = True
				ElectionThread.received = False
				ElectionThread("timer").start()

	# noinspection PyMethodParameters
	def send_ok():
		try:
			sosocket = socket.socket()
			sosocket.connect((ElectionThread.election_source_IP, ElectionThread.election_source_port))
			sosocket.send(("ok," + str(ElectionThread.port)).encode("UTF-8"))
		except:
			pass

	# noinspection PyMethodParameters
	def send_coordinator():
		for address in ElectionThread.network:
			if address != (ElectionThread.IP, ElectionThread.port):
				try:
					scmsocket = socket.socket()
					scmsocket.connect(address)
					scmsocket.send(("ok," + str(ElectionThread.port)).encode("UTF-8"))
				except:
					pass


ElectionThread.election = False
ElectionThread.election_source_IP = None
ElectionThread.election_source_port = None
ElectionThread.IP = None
ElectionThread.leader_flag = False
ElectionThread.leader_port = -1
ElectionThread.network = None
ElectionThread.port = None
ElectionThread.received = False
