import util
import requests
import json
import time
import base64
import datetime
BASE_URL = "http://127.0.0.1:8000/"
#BASE_URL = "https://devodsy.dynamyn.com/"
true = True
false = False
null = None

DEVICE_UID = '865796044530696'
SDK_TOKEN = ''
def get_authtoken():
    enc_sdk_client_secret = '*12345Abhishek'
    enc_sdk_token_expiry = '120'
    dt = datetime.datetime.now()
    delta_t = datetime.timedelta(seconds=120)
    exp_time = str(float((dt+delta_t).strftime('%s'))*1000)
    print(exp_time)
    dem_client_key = "pSm!x6wlzcInpH7szkqe"
    dem_client_secret = "h!kkvqtPB6PgJ*9tZtVT2bZ#k^"
    secret = encrypt(enc_sdk_client_secret,dem_client_secret).decode('utf-8')
    expiry = encrypt(exp_time,enc_sdk_client_secret).decode('utf-8')
    key = encrypt(dem_client_key,enc_sdk_client_secret).decode('utf-8')
    url = BASE_URL + "api/v1/dem/device_auth_view/"
    dic_payload = {'secret':secret,'expiry':expiry,'key':key}
    json_data = json.dumps(dic_payload)
    data = base64.b64encode(json_data.encode('utf-8'))
    payload = "{\"Content-Type\":\"application/json\",\"key\":\"%s\",\"imei1\":\"%s\"}" % (data.decode('utf-8'),DEVICE_UID)
    print(payload)

    headers = {
        'Content-Type': "application/json",
        'key':data.decode('utf-8'),
        'imei1':DEVICE_UID
    }

    res = requests.get(url, data={}, headers=headers)
    print(res.status_code)
    if res.status_code == 200:
        global SDK_TOKEN;
        print(dict(eval(res.text))['sdk-token'])
        SDK_TOKEN = dict(eval(res.text))['sdk-token']
        return res.text
    else:
        return res.text

def test_api():
    full_payload =  {
	"checksum":"0",
	"imei1":DEVICE_UID,"imei2":"362523432430703","device_type":"smartphone","model_name":"itel L5503","brand_name":"Itel","latitude":"null","longitude":"null","gaid":"null","mnc":"null","mcc":"23xyz","device_id":"731907db986ad9af","app_package_name":"com.datacultr.odyssey","app_version_name":"6.1.9.3","app_version_code":74,"suspicious_activity":"null","last_performed_activity":"{\"modified\":1579503003018,\"actions\":[{\"type\":\"knox\",\"action_tags\":[{\"action\":\"AB\",\"status\":\"unlock\",\"packages\":[\"com.datacultr.odyssey\",\"com.google.android.apps.photos\",\"com.samsung.android.messaging\",\"com.snapchat.android\",\"com.android.vending\",\"com.instagram.android\",\"com.Obhai.driver\",\"com.android.dialer\"]},{\"action\":\"DF\",\"status\":false},{\"action\":\"DAL\",\"status\":true}]}]}","actor_theme_change_status":false,"pwd_data_modified_status":false
    }

    syncing_payload =  {
	"checksum":"43E04950AA4959A0",
	"imei1":DEVICE_UID
    }
    payload = full_payload
    while True:
        dict_response = sendToServer(payload)
        if dict_response['_hash_'] == 'FFAA':
            print('token expired, sending again')
            continue
        elif dict_response['_hash_'] != full_payload['checksum']:
            full_payload['checksum'] = dict_response['_hash_']
            syncing_payload['checksum'] = dict_response['_hash_']
            payload = full_payload
            print("\n\n----device got new data----\n\n")
            if dict_response['data']['actor_theme_change_status']:
                print("actor_theme_change_status is True here\n sending true in response")
                full_payload['actor_theme_change_status'] = true
        else:
            if 'data' in dict_response.keys():
                if dict_response['data']['actor_theme_change_status']:
                    full_payload['actor_theme_change_status'] = true
                    payload = full_payload
                else:
                    payload = syncing_payload
            else:
                payload = syncing_payload
            print("\n\n----device is in sync with server----\n\n")
        #time.sleep(10)


def sendToServer(dic_payload):
    global SDK_TOKEN;
    url = BASE_URL + "api/v1/dem/device_sync_view/"
    payload = encrypt(json.dumps(dic_payload),util.dem_client_secret).decode("utf-8")
    print("length of payload",len(payload))
    print("request from device is:",dic_payload)
    payload = "{\"key\":\"%s\"}" % payload
    #print("after encryption data is:",payload)
    if SDK_TOKEN == '':
        sdk_token = get_authtoken()
    headers = {
        'Content-Type': "application/json",
	'sdk-token':SDK_TOKEN
    }
    print(headers)
    res = requests.post(url, data=payload, headers=headers)
    print(res.status_code)
    if res.status_code != 200:
        sdk_token = get_authtoken()
        sendToServer(dic_payload)
    print(res.text)
    #decode here
    try:
        res_dic = dict(eval(res.text))['response']
        dict_resp = decrypt(res_dic,util.dem_client_secret).decode("utf-8")
        dict_resp = dict(eval(dict_resp))
        print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
        print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dic_payload['checksum']," *~*~*~*~*~*~*~*~*~*~*~#")
        print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dict_resp['_hash_']," *~*~*~*~*~*~*~*~*~*~*~#")
        print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
        print("response from server is:",dict_resp)
        return dict_resp
    except:
        return {'_hash_':'FFAA'}

def encrypt(str,secret):
    return util.encrypt(str,secret)

def decrypt(str,secret):
    return util.decrypt(str,secret)

test_api()
