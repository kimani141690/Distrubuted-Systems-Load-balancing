import math

class ConsistentHash:
    def __init__(self, num_slots=512, num_servers=3, num_vservers_per_server=None):
        self.num_slots = num_slots
        self.hash_map = [None] * num_slots
        self.num_servers = num_servers
        self.servers = {}
        self.num_vservers_per_server = num_vservers_per_server or int(math.log2(num_slots))
        self.initialize_servers(num_servers)

    def initialize_servers(self, num_servers):
        for server_id in range(1, num_servers + 1):
            hostname = f"Server {server_id}"
            port = 5000 + server_id
            self.add_server(server_id, hostname,port)

    def hash_request_mapping(self, i):
        return (i ** 2 + 2 * (i ** 2) + 17 ** 2) % self.num_slots

    def hash_virtual_server(self, i, j):
        return (i + j + 2 * j + 25) % self.num_slots

    def add_server(self, server_id, hostname, port):
        self.servers[server_id] = (hostname, port)
        self.num_servers += 1
        print(f"Added server {server_id} with hostname: {hostname} and port: {port}")
        print(f"All servers are: {', '.join(f'{h}:{p}' for h, p in self.servers.values())}")

        for j in range(self.num_vservers_per_server):
            slot = self.hash_virtual_server(server_id, j)
            self.place_server(server_id, j, slot)


    def place_server(self, server_id, virtual_id, start_slot):
        slot = start_slot
        while self.hash_map[slot] is not None:
            # Linear probing
            slot = (slot + 1) % self.num_slots
        self.hash_map[slot] = (server_id, virtual_id)

    def remove_server(self, server_id):
        if server_id in self.servers:
            # Clear each virtual server's slot in the hash map
            for j in range(self.num_vservers_per_server):
                slot = self.hash_virtual_server(server_id, j)
                # Ensure the correct server and virtual server are removed
                if self.hash_map[slot] == (server_id, j):
                    self.hash_map[slot] = None

            # Remove the server from the servers dictionary
            del self.servers[server_id]
            self.num_servers -= 1
            print(f"Removed server {server_id}")
            print(f"All remaining servers: {', '.join(str(x) for x in self.servers.values())}")

    def get_server(self, request_id):
        slot = self.hash_request_mapping(request_id)
        while self.hash_map[slot] is None:
            # This shouldn't happen in a properly initialized map, but just in case:
            slot = (slot + 1) % self.num_slots
        return self.hash_map[slot]


# Initialize the consistent hash map
consistent_hash = ConsistentHash()
# consistent_hash.add_server(4,"S4")

consistent_hash.remove_server(2)
print(consistent_hash.hash_map)

for i in range(1, 10):
    request_id = i + 225
    server_info = consistent_hash.get_server(request_id)
    print(f"Request {request_id} is handled by server container {server_info[0]}, virtual server {server_info[1]}")
