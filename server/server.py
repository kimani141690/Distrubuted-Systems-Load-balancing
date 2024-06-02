import logging
import os

from flask import Flask, jsonify, redirect

app = Flask(__name__)

SERVER_ID = os.getenv('SERVER_ID', 'default_id')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.basicConfig(
    filename=f'/var/log/server_logs/{SERVER_ID}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)