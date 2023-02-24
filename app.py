import time

import redis
from flask import Flask, request
import requests
import json
import websocket
import _thread
import time
import rel

import requests
import xmltodict

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
    signature = request.args.get('signature')
    nonce = request.args.get('nonce')
    timestamp = request.args.get('timestamp')
    dt = [timestamp, 'Iron@zzz', nonce]
    dt.sort()
    str_check = ''.join(dt)
    data = request.data
    print(data, flush=True)
    import hashlib
    hash_object = hashlib.sha1(str_check.encode('utf-8'))
    pbHash = hash_object.hexdigest()
    data_indict = xmltodict.parse(data)
    if pbHash == signature:
        return format_instant_reply(data_indict, "Xin cam on")
    return "0"

@app.route('/login', methods=["POST"])
def login():
    secret = request.args.get('secret')
    appid = request.args.get('appid')
    timestamp = request.args.get('timestamp')
    data = request.json
    print(data, flush=True)

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={data['appid']}&secret={data['secret']}"
    response = requests.get(url)
    print(response.json(), flush=True)
    return response.content


@app.route('/get-file', methods=["POST"])
def get_file():
    access_token = request.args.get('access_token')
    media_id = request.args.get('media_id')
    timestamp = request.args.get('timestamp')

    url = f"https://api.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id={media_id}"
    response = requests.get(url)
    print(response)
    return response.content


@app.route('/get-user', methods=["POST"])
def get_user():
    access_token = request.args.get('access_token')
    user_id = request.args.get('user_id')
    timestamp = request.args.get('timestamp')
    data = request.json
    url = f"https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={access_token}"
    response = requests.get(url)
    print(response.content, flush=True)
    url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={data['access_token']}&openid={data['user_id']}"
    response = requests.get(url)
    print(response)
    return response.content


def format_instant_reply(message, response_content):
    return (
        "<xml>"
        "<ToUserName><![CDATA[%s]]></ToUserName>"
        "<FromUserName><![CDATA[%s]]></FromUserName>"
        "<CreateTime>%s</CreateTime>"
        "<MsgType><![CDATA[text]]></MsgType>"
        "<Content><![CDATA[%s]]></Content>"
        "</xml>") % (
        message['xml']['FromUserName'],  # From and To must be inverted in replies ;)
        message['xml']['ToUserName'],  # Same as above!
        time.gmtime(),
        response_content)
