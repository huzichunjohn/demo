import time

class IDGenerator(object):
    def __init__(self):
	self.worker_id = 1
	self.sequence = 0
	self.timestamp = 0
	self._last_key = 0
	self._last_timestamp = 0

    def _prime_timestamp(self):
	timestamp = int(time.time() * 1000)
	if timestamp < self.timestamp:
	    raise Exception
	self._last_timestamp, self.timestamp = self.timestamp, timestamp

    def _generate_key(self, collision=False):
	if collision:
	    self.sequence += (self.sequence % 4096) + 1
	self._prime_timestamp()

	key = self.timestamp << (64 - 41)
	key |= self.worker_id << (64 - 41 - 11)
	key |= self.sequence
	return key

    def key(self):
	key = self._generate_key()
	while key <= self._last_key:  # wait for milliseconds to change, then re-gen the key
	    key = self._generate_key(collision=True)
	self._last_key = key
	return key
