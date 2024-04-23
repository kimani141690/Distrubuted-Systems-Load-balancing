import math

class ConsistentHash:
    def __init__(self, num_slots=512, num_servers=3, num_vservers_per_server=None):
        self.num_slots = num_slots
        self.hash_map = [None] * num_slots
        self.num_servers = num_servers
        self.num_vservers_per_server = num_vservers_per_server or int(math.log2(num_slots))

    def hash_request_mapping(self, i):
        return (i**2 + 2*(i**2) + 17**2) % self.num_slots

    def hash_virtual_server(self, i, j):
        return (i + j + 2*j + 25) % self.num_slots

    def add_servers(self):
        for i in range(1, self.num_servers + 1):
            for j in range(self.num_vservers_per_server):
                slot = self.hash_virtual_server(i, j)
                self.place_server(i, j, slot)

    def place_server(self, server_id, virtual_id, start_slot):
        slot = start_slot
        while self.hash_map[slot] is not None:
            # Linear probing
            slot = (slot + 1) % self.num_slots
        self.hash_map[slot] = (server_id, virtual_id)

    def get_server(self, request_id):
        slot = self.hash_request_mapping(request_id)
        while self.hash_map[slot] is None:
            # This shouldn't happen in a properly initialized map, but just in case:
            slot = (slot + 1) % self.num_slots
        return self.hash_map[slot]

# Initialize the consistent hash map
consistent_hash = ConsistentHash()
consistent_hash.add_servers()

request_id = 7890
server_info = consistent_hash.get_server(request_id)
print(f"Request {request_id} is handled by server container {server_info[0]}, virtual server {server_info[1]}")
