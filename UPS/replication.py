import threading


class ReplicationThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self) -> None:
		pass
