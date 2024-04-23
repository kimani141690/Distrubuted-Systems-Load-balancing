import math

class ConsistentHash:
    def __init__(self, num_slots=512, num_servers=3, num_vservers_per_server=None):
        self.num_slots = num_slots
        self.hash_map = [None] * num_slots
        self.num_servers = num_servers
        self.num_vservers_per_server = num_vservers_per_server or int(math.log2(num_slots))

