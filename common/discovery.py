"""
Discovery
"""
import socket
import threading
from typing import Any, Tuple

from UPS.election import ElectionThread


class DiscoveryServerThread(threading.Thread):
	"""
	Listens for incoming discovery requests
	"""

	def __init__(self, host: str, port: int, tcp_port: int):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.tcp_port = tcp_port
		self.socket = None

	def run(self) -> None:
		"""
		Run thread
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.bind((self.host, self.port))
		while True:
			data, address = self.socket.recvfrom(1024)
			if data == b"discovery":
				self.socket.sendto(bytes(str(self.tcp_port), 'utf-8'), address)


class DiscoveryClient:
	"""
	Sends discovery requests
	"""

	def __init__(self, host: str, port: int):
		self.host = host
		self.port = port
		self.socket = None

	def discover(self) -> tuple[Any, int]:
		"""
		Run thread
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.bind((self.host, 0))
		self.socket.settimeout(5)
		while True:
			try:
				self.socket.sendto(b"discovery", ('<broadcast>', self.port))
				data, address = self.socket.recvfrom(1024)
				self.socket.close()
				break
			except socket.timeout:
				print("Timed out")
		return address[0], int(str(data, 'utf-8'))


class UPSDiscoveryServerThread(threading.Thread):
	"""
	Listens for incoming discovery requests
	"""

	def __init__(self, host: str, port: int, tcp_port: int, network: []):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.tcp_port = tcp_port
		self.network = network
		self.socket = None

	def run(self) -> None:
		"""
		Run thread
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.bind((self.host, self.port))
		while True:
			data, address = self.socket.recvfrom(1024)
			if data == b"discovery" and ElectionThread.leader_port == self.port:
				self.network.append(address)
				self.socket.sendto(bytes(str(self.tcp_port), 'utf-8'), address)


class UPSDiscoveryClient:
	"""
	Sends discovery requests
	"""

	def __init__(self, host: str, port: int, own_port: int):
		self.host = host
		self.port = port
		self.own_port = own_port
		self.socket = None

	def discover(self) -> tuple[Any, int]:
		"""
		Run thread
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.bind((self.host, self.own_port))
		self.socket.settimeout(5)
		while True:
			try:
				self.socket.sendto(b"discovery", ('<broadcast>', self.port))
				data, address = self.socket.recvfrom(1024)
				self.socket.close()
				break
			except socket.timeout:
				self.socket.close()
				return '127.0.0.1', self.own_port
		return address[0], int(str(data, 'utf-8'))
