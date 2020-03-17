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
    payload = "{\"Content-Type\":\"application/json\",\"key\":\"%s\",\"imei1\":\"%s\"}" % (data.decode('utf-8'),'865796044530696')
    print(payload)

    headers = {
        'Content-Type': "application/json",
        'key':data.decode('utf-8'),
        'imei1':'865796044530696'
    }

    res = requests.get(url, data={}, headers=headers)
    if res.status_code == 200:
        return res.text
    else:
        return res.text


def test_api():
    full_payload =  {
	"checksum":"AF057A4488A6D482",
	"imei1":"865796044530696","imei2":"362523432430703","device_type":"smartphone","model_name":"itel L5503","brand_name":"Itel","latitude":"null","longitude":"null","gaid":"null","mnc":"null","mcc":"null","device_id":"731907db986ad9af","app_package_name":"com.datacultr.odyssey","app_version_name":"6.1.9.3","app_version_code":74,"suspicious_activity":"null","last_performed_activity":"{\"modified\":1579503003018,\"actions\":[{\"type\":\"knox\",\"action_tags\":[{\"action\":\"AB\",\"status\":\"unlock\",\"packages\":[\"com.datacultr.odyssey\",\"com.google.android.apps.photos\",\"com.samsung.android.messaging\",\"com.snapchat.android\",\"com.android.vending\",\"com.instagram.android\",\"com.Obhai.driver\",\"com.android.dialer\"]},{\"action\":\"DF\",\"status\":false},{\"action\":\"DAL\",\"status\":true}]}]}","actor_theme_change_status":false,"pwd_data_modified_status":false
    }

    syncing_payload =  {
	"checksum":"43E04950AA4959A0",
	"imei1":"911655450002265"
    }
    payload = full_payload
    dict_response = sendToServer(payload)
    print("dict_response")

def sendToServer(dic_payload):
    url = BASE_URL + "api/v1/dem/device_sync_view/"
    payload = encrypt(json.dumps(dic_payload),util.dem_client_secret).decode("utf-8")
    print("length of payload",len(payload))
    print("request from device is:",dic_payload)
    payload = "{\"key\":\"%s\"}" % payload
    #print("after encryption data is:",payload)
    sdk_token = get_authtoken()
    print(dict(eval(sdk_token))['sdk-token'])
    headers = {
        'Content-Type': "application/json",
        'sdk-token':dict(eval(sdk_token))['sdk-token']
    }
    res = requests.post(url, data=payload, headers=headers)
    print(res.status_code)
    #decode here
    res_dic = dict(eval(res.text))['response']
    dict_resp = decrypt(res_dic,util.dem_client_secret).decode("utf-8")
    dict_resp = dict(eval(dict_resp))
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dic_payload['checksum']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dict_resp['_hash_']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("response from server is:",dict_resp)
    return dict_resp

def encrypt(str,secret):
    return util.encrypt(str,secret)

def decrypt(str,secret):
    return util.decrypt(str,secret)

#get_authtoken()
test_api()
