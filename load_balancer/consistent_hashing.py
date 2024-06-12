import math

class ConsistentHash:



        def __init__(self, slots=512, no_of_servers=3):
            self.no_of_servers = no_of_servers
            self.slots = slots
            self.virtual_servers = int(math.log2(slots))
            self.hash_ring = SortedDict()
            self.registered_paths = {'home', 'heartbeat', 'server_status'}
            self.init_servers()
            self.server_hash_map = {}

        # j => is the number of virtual servers per server
        # Hash function to map requests to slots
        def request_hash_fn(self, i):
            # return int(hashlib.md5(str(i).encode()).hexdigest(), 16) % self.slots
            # value = (i + (2 * i) + 17) // 2
            value = (i ** 2 + 2 * (i ** 2) + 17 ** 2)
            hash_value = value % self.slots
            return hash_value

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


    # initiating default servers
    def init_servers(self):
        try:
            client = docker.from_env()  # Connect to the Docker daemon
            containers = client.containers.list(filters={"name": "server"})  # Get server containers

            for container in containers:
                env_vars = container.attrs['Config']['Env']  # Get container's environment variables
                server_id = next((var.split('=')[1] for var in env_vars if var.startswith('SERVER_ID=')), None)
                if server_id:
                    self.add_server_to_ring(server_id, container.name)  # Add to hash ring

        except docker.errors.APIError as e:
            print(f"Error communicating with Docker daemon: {e}")
