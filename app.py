import time

import redis
from flask import Flask, request

import websocket
import _thread
import time
import rel

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/wechat', methods=["GET"])
def wechat():
    # count = get_hit_count()
    echostr = request.args.get('echostr')
    signature = request.args.get('signature')
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    # dt = [echostr, nonce, timestamp]
    # dt = [echostr, timestamp, nonce]
    # dt = [nonce, timestamp, echostr]
    # dt = [nonce, echostr, timestamp]
    # dt = [timestamp, nonce, echostr]
    dt = [timestamp, 'Iron@zzz', nonce]
    print("dt----5")
    print(dt)
    # print(echostr)
    # print(dt)
    dt.sort()
    # print("dt")
    print(dt)
    str_check = ''.join(dt)
    print('str_check')
    print(str_check)
    print("str_check.encode('utf-8')")
    print(str_check.encode('utf-8'))
    data = request.data
    print(data, flush=True)
    import hashlib
    hash_object = hashlib.sha1(str_check.encode('utf-8'))
    print("hash_object")
    print(hash_object)
    pbHash = hash_object.hexdigest()
    # length = len(pbHash.decode("hex"))
    print("pbHash")
    print(pbHash)
    # print(pbHash.decode("hex"))
    if pbHash == signature:
        return echostr

    return 'Hello World! you have been seen {} times.\n'.format(pbHash)


@app.route('/wechat', methods=["POST"])
def hello():
    echostr = request.args.get('echostr')
    signature = request.args.get('signature')
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    # dt = [echostr, nonce, timestamp]
    # dt = [echostr, timestamp, nonce]
    # dt = [nonce, timestamp, echostr]
    # dt = [nonce, echostr, timestamp]
    # dt = [timestamp, nonce, echostr]
    dt = [timestamp, 'Iron@zzz', nonce]
    print("dt----5")
    # print(dt)
    # print(echostr)
    # print(dt)
    dt.sort()
    # print("dt")
    # print(dt)
    str_check = ''.join(dt)
    # print('str_check')
    # print(str_check)
    # print("str_check.encode('utf-8')")
    # print(str_check.encode('utf-8'))
    data = request.data
    print(data, flush=True)
    import hashlib
    hash_object = hashlib.sha1(str_check.encode('utf-8'))
    # print("hash_object")
    # print(hash_object)
    pbHash = hash_object.hexdigest()
    # length = len(pbHash.decode("hex"))
    # print("pbHash")
    # print(pbHash)
    # print(pbHash.decode("hex"))
    if pbHash == signature:
        return echostr
    return 'Hello World! you have been seen {} times.\n'.format(count)
