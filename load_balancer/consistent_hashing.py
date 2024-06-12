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

        # Add server to the hash ring


def add_server_to_ring(self, server_id, hostname):
    if server_id in [value[0] for value in self.hash_ring.values()]:

        for key, value in self.hash_ring.items():
            if value[0] == server_id:
                self.hash_ring[key] = (server_id, hostname)
                print(f"Updated server {server_id} with hostname {hostname}")
                break
        raise ValueError(f"Server ID '{server_id}' already exists in the hash ring")

    else:
        for i in range(self.virtual_servers):
            server_hash_value = self.virtual_hashing(server_id, i)
            self.hash_ring[server_hash_value] = (server_id, hostname)
        self.no_of_servers += 1
        print(f"Added server {server_id} with hostname {hostname}")

    def place_server(self, server_id, virtual_id, start_slot):
        slot = start_slot
        while self.hash_map[slot] is not None:
            # Linear probing
            slot = (slot + 1) % self.num_slots
        self.hash_map[slot] = (server_id, virtual_id)

    def remove_server_from_ring(self, hostname):
        server_id = None
        for key, value in self.hash_ring.items():
            if value[1] == hostname:
                server_id = value[0]
                break
        if server_id is None:
            return {"message": f"Error: Server with hostname {hostname} not found or may have been removed",
                    "status": "failure"}, 404

        to_remove = [slot for slot, value in self.hash_ring.items() if value[0] == server_id]
        for slot in to_remove:
            del self.hash_ring[slot]

        return {"message": f"Server {hostname} removed successfully", "status": "successful"}, 200

            # Remove the server from the servers dictionary
            del self.servers[server_id]
            self.num_servers -= 1
            print(f"Removed server {server_id}")
            print(f"All remaining servers: {', '.join(str(x) for x in self.servers.values())}")


def map_request_to_server(self, request_id):
    request_hash_value = self.request_hash_fn(request_id)
    # Find the server with the next highest hash value
    for server_hash, server_id in self.hash_ring.items():
        if server_hash >= request_hash_value:
            return server_id
    # If the request hash value is greater than all server hash values wrap around to the first server
    return self.hash_ring.peekitem(0)[1]

    # in case a server does not respond to heartbeat and needs to be updated


def update_servers(self, server_id, hostname):
    self.remove_server_from_ring(server_id)
    self.add_server_to_ring(server_id, hostname)
    return self.hash_ring


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
