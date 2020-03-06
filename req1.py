import util
import requests
import json
import time
#BASE_URL = "http://127.0.0.1:8000/"
BASE_URL = "https://devodsy.dynamyn.com/"
true = True
false = False
null = None

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
    url = BASE_URL + "api/dem/device_sync_view/"
    payload = encrypt(json.dumps(dic_payload)).decode("utf-8")
    print("length of payload",len(payload))
    print("request from device is:",dic_payload)
    payload = "{\"key\":\"%s\"}" % payload
    #print("after encryption data is:",payload)

    headers = {
        'Content-Type': "application/json",
    }
    res = requests.post(url, data=payload, headers=headers)
    print(res.status_code)
    #decode here
    res_dic = dict(eval(res.text))['response']
    dict_resp = decrypt(res_dic).decode("utf-8")
    dict_resp = dict(eval(dict_resp))
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dic_payload['checksum']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dict_resp['_hash_']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("response from server is:",dict_resp)
    return dict_resp

def encrypt(str):
    return util.encrypt(str,util.dem_client_secret)

def decrypt(str):
    return util.decrypt(str,util.dem_client_secret)

test_api()
