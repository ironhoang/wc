import fxcmpy
import socketio
api_token = "0a31f1932b787b42404efffcda918d26b1ec9440"

def check_crc():
    print("hello")
    # print(fxcmpy.version)
    # print(socketio.version)
    # con = fxcmpy.fxcmpy(access_token=api_token, log_level='debug')
    con = fxcmpy.fxcmpy(access_token=api_token, config_file='fxcm.cfg')
    instruments = con.get_instruments()
    print(instruments[:5])['EUR/USD', 'USD/JPY']
    print("ok")

check_crc()