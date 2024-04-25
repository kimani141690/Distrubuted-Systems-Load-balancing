import os
import random

from flask import Flask, jsonify, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/home')


@app.route('/home')
def home():
    no = random.randint(1, 3)
    server_id = os.getenv('PORT', f'Server-{no}')
    return jsonify(message=f"Hello from : {server_id}", status="successful")


@app.route('/heartbeat')
def heartbeat():
    return 'OK', 200


if __name__ == '__main__':
    app.run()
