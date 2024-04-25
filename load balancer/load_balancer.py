from flask import Flask, request, jsonify
import json
from consistent_hashing import ConsistentHash  # Importing the hashing module
import requests

app = Flask(__name__)

# Initialize the consistent hash map with default servers
consistent_hash = ConsistentHash()

@app.route('/rep', methods=['GET'])
def get_replicas():
    # Gather detailed status from consistent_hash instance
    replicas = [hostnames for server_id, hostnames in consistent_hash.servers.items()]
    return jsonify(message={"N": len(replicas), "replicas": replicas}, status="successful"), 200


@app.route('/add', methods=['POST'])
def add_servers():
#     url = "http://localhost:5000"
#     data = {
#         'n': '3',
#         'hostnames': ['S4, S5, S6']
#     }
#     headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#     r = requests.post(url, data=json.dumps(data), headers=headers)
#     process_add_servers()
#
# def process_add_servers():
    data = request.get_json()
    hostnames = data.get('hostnames', [])

    # Validating input
    if len(hostnames) != data['n']:
        return jsonify(message={"error": "Mismatch between number of servers and number of hostnames"}), 400

    # Adding new servers
    for hostname in hostnames:
        new_server_id = consistent_hash.num_servers + 1
        consistent_hash.add_server(new_server_id, hostname)

    return (
        jsonify(message={"Added servers": data['n'], "total_servers": consistent_hash.num_servers}, status="successful"),
        get_replicas(),
        200
    )


@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.get_json()
    num_servers = data.get('n')
    hostnames = data.get('hostnames', [])

    # Validate input
    if len(hostnames) != num_servers:
        return jsonify(message={"error": "Mismatch between number of servers to remove and number of hostnames provided"},status="failure"), 400

    # Check if all hostnames are valid
    invalid_hosts = [host for host in hostnames if
                     host not in [server['hostname'] for server in consistent_hash.servers.values()]]
    if invalid_hosts:
        return jsonify(message={"error": "Some hostnames do not exist", "invalid_hostnames": invalid_hosts}), 404

    # Remove servers with specified hostnames
    for hostname in hostnames:
        server_id = next((sid for sid, details in consistent_hash.servers.items() if details['hostname'] == hostname),
                         None)
        if server_id:
            consistent_hash.remove_server(server_id)

    return jsonify(message={"Removed servers": {num_servers}, "total_servers": len(consistent_hash.servers)}, status="successful"), 200


@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    try:
        request_id = hash(path)  # Simple hash to simulate request ID based on path
        server_info = consistent_hash.get_server(request_id)
        if server_info:
            server_id, virtual_id = server_info
            # Simulate forwarding the request to the determined server
            return jsonify(message={f"Request {request_id} has been routed to server {server_id}, virtual server {virtual_id}"}, status="successful"), 200
    except Exception as e:
        return jsonify(message={"error": "No available server to handle the request", "error message": str(e)},status="failure"), 404


if __name__ == '__main__':
    app.run()

