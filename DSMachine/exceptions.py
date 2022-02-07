"""
exceptions
"""


class FRSUnreachableException(Exception):
	"""
	thrown when one of the servers can no longer be reached by the client
	"""
	pass

class ASUnreachableException(Exception):
	pass


class UPSTimeOut(Exception):
	pass

class UPS_Timeout(Exception):
	pass