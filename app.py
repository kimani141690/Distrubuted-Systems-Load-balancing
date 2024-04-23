import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/home')
def home():
    # Retrieve the server ID from the environment variable
    server_id = os.getenv('SERVER_ID', 'Unknown')
    return jsonify(message=f"Hello from Server: {server_id}", status="successful")


@app.route('/heartbeat')
def heartbeat():
    # Heartbeat endpoint to check server health
    return '', 200


if __name__ == '__main__':
    app.run()
